/********************************************************************************
* Copyright (c) 2024 Contributors to the Eclipse Foundation
*
* See the NOTICE file(s) distributed with this work for additional
* information regarding copyright ownership.
*
* This program and the accompanying materials are made available under the
* terms of the Apache License 2.0 which is available at
* http://www.apache.org/licenses/LICENSE-2.0
*
* SPDX-License-Identifier: Apache-2.0
********************************************************************************/

use std::{collections::HashMap, time::SystemTime};

use anyhow::{Context, Result};
use clap::Parser;
use hdrhistogram::Histogram;
use log::error;
use sampler::Sampler;
use tokio::{join, sync::mpsc};

mod config;
mod provider;
mod sampler;
mod subscriber;

#[derive(Parser)]
#[clap(author, version, about)]
struct Args {
    #[clap(long, display_order = 1, default_value_t = 1000)]
    iterations: u64,
    // #[clap(long, display_order = 2, default_value_t = 32)]
    // sample_size: u64,
    #[clap(long, display_order = 3, default_value = "http://127.0.0.1")]
    host: String,
    #[clap(long, display_order = 4, default_value_t = 55555)]
    port: u64,
    #[clap(long = "config", display_order = 5, value_name = "CONFIG_FILE")]
    config_file: Option<String>,
    #[clap(long = "verbosity", short, display_order = 6, default_value_t = log::Level::Warn)]
    verbosity_level: log::Level,
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = Args::parse();

    // Setup logging
    stderrlog::new()
        .module(module_path!())
        .verbosity(args.verbosity_level)
        .init()
        .unwrap();

    let iterations = args.iterations;
    let sample_size = 1; //args.sample_size;
    let databroker_address = format!("{}:{}", args.host, args.port);

    let signals = match args.config_file {
        Some(ref filename) => {
            let config_file = std::fs::OpenOptions::new()
                .read(true)
                .open(filename)
                .with_context(|| format!("Failed to open configuration file '{}'", filename))?;
            let config: config::Config = serde_json::from_reader(config_file)
                .with_context(|| format!("Failed to parse configuration file '{}'", filename))?;

            Ok::<Vec<config::Signal>, anyhow::Error>(config.signals)
        }
        None => {
            // Default set of signals
            Ok(vec![config::Signal {
                path: "Vehicle.Cabin.Infotainment.Media.Played.Track".to_owned(),
            }])
        }
    }?;

    let endpoint = tonic::transport::Channel::from_shared(databroker_address.clone())
        .with_context(|| "Failed to parse server url")?;
    let provider_channel = endpoint
        .connect()
        .await
        .with_context(|| "Failed to connect to server")?;

    let provider = provider::Provider::new(provider_channel.clone(), signals.into_iter())
        .await
        .with_context(|| "Failed to setup provider")?;

    let (subscriber_tx, mut subscriber_rx) = mpsc::channel(100);
    let (provider_tx, mut provider_rx) = mpsc::channel(100);
    let subscriber_sampler = Sampler::new(iterations, sample_size, subscriber_tx);
    let provider_sampler = Sampler::new(iterations, sample_size, provider_tx);

    let subscriber_channel = endpoint
        .connect()
        .await
        .with_context(|| "Failed to connect to server")?;

    let start_time = SystemTime::now();
    let subscriber_task = tokio::spawn(async move {
        match subscriber::subscribe(subscriber_sampler, subscriber_channel).await {
            Ok(_) => {}
            Err(err) => {
                error!("failed to subscribe: {}", err);
            }
        }
    });

    let provider_task = tokio::spawn(async move {
        provider::provide(provider_sampler, provider).await;
    });

    let mut hist = Histogram::<u64>::new_with_bounds(1, 60 * 60 * 1000 * 1000, 3).unwrap();

    let mut samples = HashMap::with_capacity(sample_size.try_into().unwrap());

    loop {
        match join!(provider_rx.recv(), subscriber_rx.recv()) {
            (Some(Ok(provided_samples)), Some(Ok(received_samples))) => {
                for sample in received_samples {
                    samples.insert(sample.cycle, sample.timestamp);
                }

                for sample in provided_samples {
                    match samples.get(&sample.cycle) {
                        Some(end_time) => {
                            let start_time = sample.timestamp;
                            let latency = end_time.duration_since(start_time);
                            // println!("({}) latency: {}", sample.cycle, latency.as_nanos());
                            hist.record(latency.as_micros().try_into().unwrap())
                                .unwrap();
                            samples.remove(&sample.cycle);
                        }
                        None => {
                            // eprintln!("missing sample {}", sample.cycle);
                        }
                    }
                }
            }
            (None, None) => {
                // Done
                break;
            }
            (_p, _s) => {
                error!("recieved non-ok message from subscriber / provider");
                break;
            }
        }
    }
    let _ = join!(provider_task, subscriber_task);

    let end_time = SystemTime::now();
    let total_duration = end_time.duration_since(start_time)?;
    println!("Summary:");
    println!("  Count: {}", hist.len());
    println!(
        "  Total: {:.2} s",
        total_duration.as_millis() as f64 / 1000.0
    );
    println!("  Fastest: {:>7.2} ms", hist.min() as f64 / 1000.0);
    println!("  Slowest: {:>7.2} ms", hist.max() as f64 / 1000.0);
    println!("  Average: {:>7.2} ms", hist.mean() as f64 / 1000.0);
    println!(
        "  Requests / s: {:.2}",
        hist.len() as f64 / total_duration.as_secs_f64()
    );
    println!("\nResponse time histogram:");
    let step_size = (hist.max() - hist.min()) / 11;

    for v in hist.iter_linear(step_size) {
        let mean = v.value_iterated_to() + 1 - step_size / 2; // +1 to make range inclusive
        let count = v.count_since_last_iteration();
        let bars = count as f64 / iterations as f64 * 100.0;
        let bar = std::iter::repeat("∎")
            .take(bars as usize)
            .collect::<String>();
        println!("  {:>7.2} ms [{:<5}] |{}", mean as f64 / 1000.0, count, bar);
    }

    println!("\nLatency distribution:");

    for q in &[10, 25, 50, 75, 90, 95, 99] {
        println!(
            "  {q}% in < {:.2} ms",
            hist.value_at_quantile(*q as f64 / 100.0) as f64 / 1000.0
        );
    }

    Ok(())
}
