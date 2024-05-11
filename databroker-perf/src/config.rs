use serde::Deserialize;

#[derive(Deserialize)]
pub struct Config {
    pub signals: Vec<Signal>,
}

#[derive(Deserialize, Clone)]
pub struct Signal {
    pub path: String,
}
