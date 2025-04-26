#![warn(clippy::pedantic, clippy::nursery)]

use feruca::{Collator, Locale, Tailoring};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

/// Sort a list of strings using the Unicode Collation Algorithm
#[pyfunction]
fn collate(mut strings: Vec<String>, tailoring: &str) -> PyResult<Vec<String>> {
    let t: Tailoring = match tailoring {
        "default" => Tailoring::Cldr(Locale::Root),
        "ArabicFirst" => Tailoring::Cldr(Locale::ArabicScript),
        "ArabicInterleaved" => Tailoring::Cldr(Locale::ArabicInterleaved),
        _ => return Err(PyValueError::new_err("Invalid tailoring")),
    };

    // For now, we always set `shifting` and `tiebreak` to true
    let mut coll = Collator::new(t, true, true);

    strings.sort_unstable_by(|a, b| coll.collate(a, b));
    Ok(strings)
}

/// Python module implemented in Rust
#[pymodule]
#[pyo3(name = "feruca")]
fn feruca_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(collate, m)?)?;
    Ok(())
}
