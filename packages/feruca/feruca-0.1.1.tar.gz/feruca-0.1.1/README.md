# feruca-py

This package is meant to provide a basic Python interface to
[feruca](https://github.com/theodore-s-beers/feruca), a Rust implementation of
the Unicode Collation Algorithm. There is, at this point, only one function
available: `collate`, which sorts a list of strings in accordance with the UCA,
and with a choice of a few "tailorings."

**There is a strong possibility that the Python API will be changed,** depending
on user feedback, benchmarking results, etc. This initial version is essentially
a proof of concept.

Below is an example of how to use the `collate` function in its current form:

```python
from feruca import collate

strings = ["zebra", "éléonore", "grok"]

# Tailoring options are "default", "ArabicScript", and "ArabicInterleaved"
strings_sorted = collate(strings, tailoring="default")

print(strings_sorted) # ['éléonore', 'grok', 'zebra']
```

The `default` tailoring follows the "root collation order" defined by the Common
Locale Data Repository (CLDR). `ArabicScript` modifies this such that the Arabic
script as a whole sorts before the Latin script. `ArabicInterleaved` is more
nuanced, mixing the two scripts such that Arabic _alif_ sorts after A but before
B; _bā’_ sorts after B but before C; etc.

In all cases, the "shifted" approach is taken with variable-weight characters. A
number of such options that are configurable in the Rust library are not yet
exposed in this Python wrapper.
