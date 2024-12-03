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

use crate::{broker, permissions};

use crate::broker::AuthorizedAccess;
use databroker_proto::kuksa::val::v2::{
    self as proto,
    open_provider_stream_request::Action::{
        BatchActuateStreamResponse, ProvideActuationRequest, PublishValuesRequest,
    },
    open_provider_stream_response, OpenProviderStreamResponse, PublishValuesResponse,
};

use prost::Message;
use serde_json::json;
use zenoh::{config::WhatAmI, key_expr::KeyExpr};

async fn publish_values(
    broker: &AuthorizedAccess<'_, '_>,
    request: &databroker_proto::kuksa::val::v2::PublishValuesRequest,
) -> Option<OpenProviderStreamResponse> {
    let ids: Vec<(i32, broker::EntryUpdate)> = request
        .datapoints
        .iter()
        .map(|(id, datapoint)| {
            (
                *id,
                broker::EntryUpdate {
                    path: None,
                    datapoint: Some(broker::Datapoint::from(datapoint)),
                    actuator_target: None,
                    entry_type: None,
                    data_type: None,
                    description: None,
                    allowed: None,
                    min: None,
                    max: None,
                    unit: None,
                },
            )
        })
        .collect();

    // TODO check if provider is allowed to update the entries for the provided signals?
    match broker.update_entries(ids).await {
        Ok(_) => None,
        Err(err) => Some(OpenProviderStreamResponse {
            action: Some(
                open_provider_stream_response::Action::PublishValuesResponse(
                    PublishValuesResponse {
                        request_id: request.request_id,
                        status: err
                            .iter()
                            .map(|(id, error)| (*id, proto::Error::from(error)))
                            .collect(),
                    },
                ),
            ),
        }),
    }
}

pub async fn serve(broker: broker::DataBroker) -> Result<(), Box<dyn std::error::Error>> {
    let mut config = zenoh::config::Config::default();

    let _ = config.insert_json5("mode", &json!(WhatAmI::Router.to_str()).to_string());

    let endpoint = vec![format!("tcp/127.0.0.1:{}", 17447)];

    let _ = config.insert_json5("listen/endpoints", &json!(endpoint).to_string());

    let session = zenoh::open(config).await.unwrap();

    let mut tasks = Vec::new();

    for i in 1..=50 {
        // Specify the topic to subscribe to
        let topic = i.to_string();
        let pub_key = KeyExpr::try_from(topic.clone()).unwrap();

        let subscriber = session.declare_subscriber(&pub_key).await.unwrap();

        println!("Subscribing to topic: {}", topic);

        let local_broker = broker.clone();
        // Process messages using the stream

        let task = tokio::spawn(async move {
            let local_broker = local_broker.authorized_access(&permissions::ALLOW_ALL);
            while let Ok(payload) = subscriber.recv_async().await {
                let request =
                    proto::OpenProviderStreamRequest::decode(&*payload.payload().to_bytes())
                        .unwrap();

                match request.action {
                    Some(ProvideActuationRequest(_)) => {}
                    Some(PublishValuesRequest(publish_values_request)) => {
                        //Ignore response for now
                        let _response =
                            publish_values(&local_broker, &publish_values_request).await;
                    }
                    Some(BatchActuateStreamResponse(_)) => {}
                    None => {}
                }
            }
        });
        tasks.push(task);
    }

    for task in tasks {
        task.await.unwrap();
    }
    Ok(())
}
