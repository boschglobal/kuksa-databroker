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
use log::{debug, error, info};

use std::collections::HashMap;
use thiserror::Error;
use tokio::{
    sync::mpsc::{self, Receiver, Sender},
    time::Instant,
};
use tokio_stream::wrappers::ReceiverStream;
use tonic::transport::Channel;

use crate::config::Signal;

pub(crate) struct Provider {
    // signals: Vec<Signal>,
    metadata: HashMap<String, proto::Metadata>,
    tx: Sender<proto::StreamDatapointsRequest>,
}

#[derive(Error, Debug)]
pub(crate) enum Error {
    #[error("failed to fetch signal metadata: {0}")]
    MetadataError(String),
    #[error("publish error")]
    PublishError(#[from] PublishError),
}

#[derive(Error, Debug)]
pub enum PublishError {
    // #[error("the signal has not been registered")]
    // NotRegistered,
    #[error("failed to send new value: {0}")]
    SendFailure(String),
}
// pub(crate) struct ProviderConfig {}

impl Provider {
    pub(crate) fn new(
        channel: Channel,
        metadata: HashMap<String, proto::Metadata>,
    ) -> Result<Self, Error> {
        let (tx, rx) = mpsc::channel(10);

        tokio::spawn(Provider::run(rx, channel));
        Ok(Provider { metadata, tx })
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
                                let error_code = match proto::DatapointError::from_i32(error.1) {
                                    Some(error_code) => error_code.as_str_name(),
                                    None => "unknown error",
                                };
                                let id = error.0;
                                error!("{}: error setting datapoint {}", error_code, id)
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
    ) -> Result<Instant, PublishError> {
        let payload = proto::StreamDatapointsRequest { datapoints };

        let now = Instant::now();
        self.tx
            .send(payload)
            .await
            .map_err(|err| PublishError::SendFailure(err.to_string()))?;
        Ok(now)
    }
}

pub async fn get_metadata(
    channel: Channel,
    signals: impl Iterator<Item = Signal>,
) -> Result<HashMap<String, proto::Metadata>, Error> {
    let mut client = proto::broker_client::BrokerClient::new(channel);

    let signals = signals.map(|signal| signal.path).collect::<Vec<_>>();
    let response = client
        .get_metadata(tonic::Request::new(proto::GetMetadataRequest {
            names: signals.clone(),
        }))
        .await
        .map_err(|err| {
            Error::MetadataError(format!("failed to fetch metadata: {}", err.to_string()))
        })?;

    let metadata = HashMap::from_iter(
        response
            .into_inner()
            .list
            .into_iter()
            .map(|entry| (entry.name.clone(), entry)),
    );

    debug!("received {} number of signals in metadata", metadata.len());
    if metadata.len() < signals.len() {
        Err(Error::MetadataError(
            "not all signals available in databroker".into(),
        ))
    } else {
        Ok(metadata)
    }
}

pub fn n_to_value(
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
        proto::DataType::Int64 => Ok(proto::datapoint::Value::Int64Value((n % 128) as i64)),
        proto::DataType::Uint8 => Ok(proto::datapoint::Value::Uint32Value((n % 128) as u32)),
        proto::DataType::Uint16 => Ok(proto::datapoint::Value::Uint32Value((n % 128) as u32)),
        proto::DataType::Uint32 => Ok(proto::datapoint::Value::Uint32Value((n % 128) as u32)),
        proto::DataType::Uint64 => Ok(proto::datapoint::Value::Uint64Value(n % 128)),
        proto::DataType::Float => Ok(proto::datapoint::Value::FloatValue(n as f32)),
        proto::DataType::Double => Ok(proto::datapoint::Value::DoubleValue(n as f64)),
        proto::DataType::StringArray => {
            Ok(proto::datapoint::Value::StringArray(proto::StringArray {
                values: vec![n.to_string()],
            }))
        }
        proto::DataType::BoolArray => Ok(proto::datapoint::Value::BoolArray(proto::BoolArray {
            values: vec![match n % 2 {
                0 => true,
                _ => false,
            }],
        })),
        proto::DataType::Int8Array => Ok(proto::datapoint::Value::Int32Array(proto::Int32Array {
            values: vec![(n % 128) as i32],
        })),
        proto::DataType::Int16Array => Ok(proto::datapoint::Value::Int32Array(proto::Int32Array {
            values: vec![(n % 128) as i32],
        })),
        proto::DataType::Int32Array => Ok(proto::datapoint::Value::Int32Array(proto::Int32Array {
            values: vec![(n % 128) as i32],
        })),
        proto::DataType::Int64Array => Ok(proto::datapoint::Value::Int64Array(proto::Int64Array {
            values: vec![(n % 128) as i64],
        })),
        proto::DataType::Uint8Array => {
            Ok(proto::datapoint::Value::Uint32Array(proto::Uint32Array {
                values: vec![(n % 128) as u32],
            }))
        }
        proto::DataType::Uint16Array => {
            Ok(proto::datapoint::Value::Uint32Array(proto::Uint32Array {
                values: vec![(n % 128) as u32],
            }))
        }
        proto::DataType::Uint32Array => {
            Ok(proto::datapoint::Value::Uint32Array(proto::Uint32Array {
                values: vec![(n % 128) as u32],
            }))
        }
        proto::DataType::Uint64Array => {
            Ok(proto::datapoint::Value::Uint64Array(proto::Uint64Array {
                values: vec![n % 128],
            }))
        }
        proto::DataType::FloatArray => Ok(proto::datapoint::Value::FloatArray(proto::FloatArray {
            values: vec![n as f32],
        })),
        proto::DataType::DoubleArray => {
            Ok(proto::datapoint::Value::DoubleArray(proto::DoubleArray {
                values: vec![n as f64],
            }))
        }
    }
}
