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

use databroker_proto::sdv::databroker::v1 as proto;
use std::{collections::HashMap, sync::Arc};
use thiserror::Error;

use log::{error, info};
use tokio::{
    sync::broadcast::{self, Receiver, Sender},
    time::Instant,
};
use tonic::transport::Channel;

use crate::config;

pub struct Subscriber {
    metadata: HashMap<String, proto::Metadata>,
    signals: Arc<HashMap<String, Sender<Instant>>>,
}

#[derive(Error, Debug)]
pub enum Error {
    #[error("subscription failed: {0}")]
    SubscriptionError(String),

    #[error("waiting for a signal update failed: {0}")]
    RecvError(String),

    #[error("signal '{0}' not found")]
    SignalNotFound(String),
}

impl Subscriber {
    pub fn new(
        channel: Channel,
        signals: Vec<config::Signal>,
        metadata: HashMap<String, proto::Metadata>,
    ) -> Self {
        let query = Self::query_from_signals(signals.clone().into_iter());

        let signals = Arc::new(HashMap::from_iter(signals.into_iter().map(|signal| {
            let (sender, _) = broadcast::channel(32);
            (signal.path, sender)
        })));
        tokio::spawn(Subscriber::run(channel, query, signals.clone()));

        Self { metadata, signals }
    }

    fn query_from_signals(signals: impl Iterator<Item = config::Signal>) -> String {
        format!(
            "SELECT {}",
            signals
                .map(|signal| signal.path)
                .collect::<Vec<String>>()
                .as_slice()
                .join(",")
        )
    }

    pub async fn wait_for(&self, path: String) -> Result<Instant, Error> {
        match self.signals.get(&path) {
            Some(sender) => {
                let mut subscription = sender.subscribe();
                Ok(subscription
                    .recv()
                    .await
                    .map_err(|err| Error::RecvError(err.to_string()))?)
            }
            None => Err(Error::SignalNotFound(path.to_string())),
        }
    }

    pub fn wait_for2(&self, path: &str) -> Result<Receiver<Instant>, Error> {
        match self.signals.get(path) {
            Some(sender) => Ok(sender.subscribe()),
            None => Err(Error::SignalNotFound(path.to_string())),
        }
    }

    async fn run(
        channel: Channel,
        query: String,
        signals: Arc<HashMap<String, Sender<Instant>>>,
    ) -> Result<(), Error> {
        let mut client = proto::broker_client::BrokerClient::new(channel);

        let args = tonic::Request::new(proto::SubscribeRequest { query });

        match client.subscribe(args).await {
            Ok(response) => {
                let mut stream = response.into_inner();

                // Ignore first message as the first notification is not triggered by a provider
                // but instead contains the current value.
                let _ = stream
                    .message()
                    .await
                    .map_err(|err| Error::SubscriptionError(err.to_string()))?;

                loop {
                    if let Some(update) = stream
                        .message()
                        .await
                        .map_err(|err| Error::SubscriptionError(err.to_string()))?
                    {
                        let now = Instant::now();
                        for (path, _datapoint) in update.fields {
                            if let Some(sender) = signals.get(&path) {
                                // If no one is subscribed the send fails, which is fine.
                                let _ = sender.send(now);
                            }
                        }
                    } else {
                        info!("Server gone. Subscription stopped");
                        break;
                    }
                }
                Ok(())
            }
            Err(err) => Err(Error::SubscriptionError(err.to_string())),
        }
    }
}

#[cfg(test)]
mod test {
    use crate::config::Signal;

    use super::*;

    #[test]
    fn test_query_from_signal() {
        let query = Subscriber::query_from_signals(vec![Signal::new("Vehicle.Speed")].into_iter());
        assert_eq!(query, "SELECT Vehicle.Speed")
    }

    #[test]
    fn test_query_from_signals() {
        let query = Subscriber::query_from_signals(
            vec![Signal::new("Vehicle.Speed"), Signal::new("Vehicle.Width")].into_iter(),
        );
        assert_eq!(query, "SELECT Vehicle.Speed,Vehicle.Width")
    }
}
