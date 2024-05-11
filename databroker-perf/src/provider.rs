/********************************************************************************
* Copyright (c) 2022 Contributors to the Eclipse Foundation
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

use databroker_proto::sdv::databroker::v1 as proto;
use log::{debug, error};

use std::{collections::HashMap, time::Duration};
use thiserror::Error;
use tokio::{
    sync::mpsc::{self, Receiver, Sender},
    time::Instant,
};
use tokio_stream::wrappers::ReceiverStream;
use tonic::transport::Channel;

use crate::{config::Signal, sampler};

pub(crate) struct Provider {
    // signals: Vec<Signal>,
    metadata: HashMap<String, proto::Metadata>,
    tx: Sender<proto::StreamDatapointsRequest>,
}

#[derive(Error, Debug)]
pub(crate) enum Error {
    #[error("failed to register signals: {0}")]
    RegistrationError(String),
    #[error("publish error")]
    PublishError(#[from] PublishError),
}

#[derive(Error, Debug)]
pub enum PublishError {
    // #[error("the signal has not been registered")]
    // NotRegistered,
    #[error("failed to send new value: {0}")]
    SendFailure(String),
    #[error("unsupported data type: {0}")]
    UnsupportedDataType(String),
}
// pub(crate) struct ProviderConfig {}

impl Provider {
    pub(crate) async fn new(
        channel: Channel,
        signals: impl Iterator<Item = Signal>,
    ) -> Result<Self, Error> {
        // let path_to_id = register_signals(channel, &signals).await?;

        let metadata = get_metadata(channel.clone(), signals).await?;

        let (tx, rx) = mpsc::channel(10);

        tokio::spawn(Provider::run(rx, channel));
        Ok(Provider {
            // signals,
            metadata,
            tx,
        })
    }

    async fn run(
        rx: Receiver<proto::StreamDatapointsRequest>,
        channel: Channel,
    ) -> Result<(), Error> {
        let mut client = proto::collector_client::CollectorClient::new(channel);

        match client.stream_datapoints(ReceiverStream::new(rx)).await {
            Ok(response) => {
                let mut stream = response.into_inner();

                while let Ok(message) = stream.message().await {
                    match message {
                        Some(message) => {
                            for error in message.errors {
                                println!(
                                    "Error setting datapoint {}: {:?}",
                                    error.0,
                                    proto::DatapointError::from_i32(error.1)
                                )
                            }
                        }
                        None => {
                            debug!("stream to databroker closed");
                            break;
                        }
                    }
                }
            }
            Err(err) => {
                error!("failed to setup provider stream: {}", err.message());
            }
        }
        debug!("provider::run() exiting");
        Ok(())
    }

    pub async fn publish(
        &self,
        datapoints: HashMap<i32, proto::Datapoint>,
    ) -> Result<(), PublishError> {
        // let id = self
        //     .metadata
        //     .get(path)
        //     .ok_or(PublishError::NotRegistered)?
        //     .id;
        // let payload = proto::StreamDatapointsRequest {
        //     datapoints: HashMap::from([(
        //         id,
        //         proto::Datapoint {
        //             timestamp: None,
        //             value: Some(value),
        //         },
        //     )]),
        // };

        let payload = proto::StreamDatapointsRequest { datapoints };
        self.tx
            .send(payload)
            .await
            .map_err(|err| PublishError::SendFailure(err.to_string()))
    }
}

async fn get_metadata(
    channel: Channel,
    signals: impl Iterator<Item = Signal>,
) -> Result<HashMap<String, proto::Metadata>, Error> {
    let mut client = proto::broker_client::BrokerClient::new(channel);

    let response = client
        .get_metadata(tonic::Request::new(proto::GetMetadataRequest {
            names: signals.map(|signal| signal.path).collect(),
        }))
        .await
        .map_err(|err| {
            Error::RegistrationError(format!("failed to fetch metadata: {}", err.to_string()))
        })?;

    let metadata = HashMap::from_iter(
        response
            .into_inner()
            .list
            .into_iter()
            .map(|entry| (entry.name.clone(), entry)),
    );
    debug!("{} number of signals in metadata", metadata.len());
    Ok(metadata)
}

pub(crate) async fn provide(sampler: sampler::Sampler, provider: Provider) {
    let mut n = 0;
    let mut interval = tokio::time::interval(Duration::from_millis(1));
    loop {
        let sample_size = sampler.sample_size;
        let mut samples = Vec::with_capacity(sample_size.try_into().unwrap());
        for _ in 0..sample_size {
            n += 1;
            if n > sampler.iterations {
                break;
            }
            interval.tick().await;
            let now = Instant::now();
            let sample = sampler::Sample {
                cycle: n,
                timestamp: now,
            };

            let datapoints = HashMap::from_iter(provider.metadata.iter().map(|entry| {
                let data_type = proto::DataType::from_i32(entry.1.data_type)
                    .expect("enum i32 should always be valid enum");
                (
                    entry.1.id,
                    proto::Datapoint {
                        timestamp: None,
                        value: Some(n_to_value(&data_type, n).unwrap()),
                    },
                )
            }));

            match provider.publish(datapoints).await {
                Ok(_) => samples.push(sample),
                Err(err) => {
                    error!("provider failed to publish: {err}");
                    let _ = sampler.abort(sampler::Error::FatalError(err.to_string()));
                    return;
                }
            };
        }

        match sampler.send(samples).await {
            Ok(_) => {
                if n > sampler.iterations {
                    break;
                }
            }
            Err(_) => break,
        }
    }

    // match stream.await {
    //     Ok(_) => {}
    //     Err(err) => eprint!("{err}"),
    // };
}

fn n_to_value(
    data_type: &proto::DataType,
    n: u64,
) -> Result<proto::datapoint::Value, PublishError> {
    match data_type {
        proto::DataType::String => Ok(proto::datapoint::Value::StringValue(n.to_string())),
        proto::DataType::Bool => match n % 2 {
            0 => Ok(proto::datapoint::Value::BoolValue(true)),
            _ => Ok(proto::datapoint::Value::BoolValue(false)),
        },
        proto::DataType::Int8 => Ok(proto::datapoint::Value::Int32Value((n % 128) as i32)),
        proto::DataType::Int16 => Ok(proto::datapoint::Value::Int32Value((n % 128) as i32)),
        proto::DataType::Int32 => Ok(proto::datapoint::Value::Int32Value((n % 128) as i32)),
        proto::DataType::Int64 => Ok(proto::datapoint::Value::Int32Value((n % 128) as i32)),
        proto::DataType::Uint8 => Ok(proto::datapoint::Value::Int32Value((n % 128) as i32)),
        proto::DataType::Uint16 => Ok(proto::datapoint::Value::Int32Value((n % 128) as i32)),
        proto::DataType::Uint32 => Ok(proto::datapoint::Value::Int32Value((n % 128) as i32)),
        proto::DataType::Uint64 => Ok(proto::datapoint::Value::Uint64Value(n % 128)),
        proto::DataType::Float => Ok(proto::datapoint::Value::FloatValue(n as f32)),
        proto::DataType::Double => Ok(proto::datapoint::Value::DoubleValue(n as f64)),
        _ => Err(PublishError::UnsupportedDataType(
            data_type.as_str_name().to_owned(),
        )),
    }
}
