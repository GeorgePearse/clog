use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use pyo3::prelude::*;

pub mod ui;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Metric {
    pub name: String,
    pub value: f64,
    pub timestamp: DateTime<Utc>,
    pub step: usize,
}

#[derive(Clone, Debug)]
pub struct LogEntry {
    pub message: String,
    pub timestamp: DateTime<Utc>,
    pub level: LogLevel,
}

#[derive(Clone, Debug, PartialEq)]
pub enum LogLevel {
    Info,
    Warning,
    Error,
}

#[pyclass]
#[derive(Clone)]
pub struct ClogTracker {
    metrics: Arc<Mutex<HashMap<String, Vec<Metric>>>>,
    logs: Arc<Mutex<Vec<LogEntry>>>,
}

#[pymethods]
impl ClogTracker {
    #[new]
    pub fn new() -> Self {
        ClogTracker {
            metrics: Arc::new(Mutex::new(HashMap::new())),
            logs: Arc::new(Mutex::new(Vec::new())),
        }
    }

    pub fn log_metric(&self, name: String, value: f64, step: usize) -> PyResult<()> {
        let metric = Metric {
            name: name.clone(),
            value,
            timestamp: Utc::now(),
            step,
        };
        
        let mut metrics = self.metrics.lock().unwrap();
        metrics.entry(name).or_insert_with(Vec::new).push(metric);
        Ok(())
    }

    pub fn log_message(&self, message: String, level: String) -> PyResult<()> {
        let log_level = match level.as_str() {
            "info" => LogLevel::Info,
            "warning" => LogLevel::Warning,
            "error" => LogLevel::Error,
            _ => LogLevel::Info,
        };
        
        let entry = LogEntry {
            message,
            timestamp: Utc::now(),
            level: log_level,
        };
        
        let mut logs = self.logs.lock().unwrap();
        logs.push(entry);
        Ok(())
    }
    
    pub fn run_ui(&self) -> PyResult<()> {
        let tracker = Arc::new(self.clone());
        let mut ui = ui::TerminalUI::new(tracker);
        ui.run().map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        Ok(())
    }
}

#[pymodule]
fn _rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ClogTracker>()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_metric_tracking() {
        let tracker = ClogTracker::new();
        tracker.log_metric("test_metric".to_string(), 42.0, 1).unwrap();
        
        let metrics = tracker.metrics.lock().unwrap();
        assert!(metrics.contains_key("test_metric"));
    }
}