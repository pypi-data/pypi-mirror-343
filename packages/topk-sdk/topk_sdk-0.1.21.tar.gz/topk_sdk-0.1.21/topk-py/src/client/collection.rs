use crate::client::Runtime;
use crate::data::value::RawValue;
use crate::error::RustError;
use crate::query::{ConsistencyLevel, Query};
use pyo3::prelude::*;
use std::{collections::HashMap, sync::Arc};

#[pyclass]
pub struct CollectionClient {
    runtime: Arc<Runtime>,
    client: Arc<topk_rs::Client>,
    collection: String,
}

impl CollectionClient {
    pub fn new(runtime: Arc<Runtime>, client: Arc<topk_rs::Client>, collection: String) -> Self {
        Self {
            runtime,
            client,
            collection,
        }
    }
}

#[pymethods]
impl CollectionClient {
    #[pyo3(signature = (id, fields=vec![], lsn=None, consistency=None))]
    pub fn get(
        &self,
        py: Python<'_>,
        id: String,
        fields: Vec<String>,
        lsn: Option<u64>,
        consistency: Option<ConsistencyLevel>,
    ) -> PyResult<HashMap<String, RawValue>> {
        let document = self
            .runtime
            .block_on(
                py,
                self.client.collection(&self.collection).get(
                    id,
                    fields,
                    lsn,
                    consistency.map(|c| c.into()),
                ),
            )
            .map_err(RustError)?;

        Ok(document
            .fields
            .into_iter()
            .map(|(k, v)| (k, RawValue(v.into())))
            .collect())
    }

    #[pyo3(signature = (lsn=None, consistency=None))]
    pub fn count(
        &self,
        py: Python<'_>,
        lsn: Option<u64>,
        consistency: Option<ConsistencyLevel>,
    ) -> PyResult<u64> {
        let count = self
            .runtime
            .block_on(
                py,
                self.client
                    .collection(&self.collection)
                    .count(lsn, consistency.map(|c| c.into())),
            )
            .map_err(RustError)?;

        Ok(count)
    }

    #[pyo3(signature = (query, lsn=None, consistency=None))]
    pub fn query(
        &self,
        py: Python<'_>,
        query: Query,
        lsn: Option<u64>,
        consistency: Option<ConsistencyLevel>,
    ) -> PyResult<Vec<HashMap<String, RawValue>>> {
        let docs = self
            .runtime
            .block_on(
                py,
                self.client.collection(&self.collection).query(
                    query.into(),
                    lsn,
                    consistency.map(|c| c.into()),
                ),
            )
            .map_err(RustError)?;

        Ok(docs
            .into_iter()
            .map(|d| {
                d.fields
                    .into_iter()
                    .map(|(k, v)| (k, RawValue(v.into())))
                    .collect()
            })
            .collect())
    }

    pub fn upsert(
        &self,
        py: Python<'_>,
        documents: Vec<HashMap<String, RawValue>>,
    ) -> PyResult<u64> {
        let documents = documents
            .into_iter()
            .map(|d| topk_protos::v1::data::Document {
                fields: d.into_iter().map(|(k, v)| (k, v.into())).collect(),
            })
            .collect();

        Ok(self
            .runtime
            .block_on(
                py,
                self.client.collection(&self.collection).upsert(documents),
            )
            .map_err(RustError)?)
    }

    pub fn delete(&self, py: Python<'_>, ids: Vec<String>) -> PyResult<u64> {
        Ok(self
            .runtime
            .block_on(py, self.client.collection(&self.collection).delete(ids))
            .map_err(RustError)?)
    }
}
