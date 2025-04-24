use pyo3::prelude::*;

pub const N_CATCH22: usize = 25;

#[pymodule]
#[pyo3(name = "pycatchrs")]
fn py_module(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(compute, m)?)?;
    m.add_function(wrap_pyfunction!(zscore, m)?)?;
    Ok(())
}

#[pyfunction]
#[pyo3(signature = (x, n))]
pub fn compute(x: Vec<f64>, n: usize) -> f64 {
    catch22::compute(&x, n)
}

#[pyfunction]
#[pyo3(signature = (x))]
pub fn zscore(x: Vec<f64>) -> Vec<f64> {
    catch22::zscore(&x)
}