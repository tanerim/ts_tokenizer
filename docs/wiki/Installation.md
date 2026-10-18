# Installation

TS Tokenizer requires **Python 3.9 or newer**. Version 0.3.0 has no third-party
runtime dependencies; lexical data is included in the distribution.

Install the version available on PyPI:

```bash
python -m pip install ts-tokenizer
```

Upgrade an existing installation:

```bash
python -m pip install --upgrade ts-tokenizer
```

Verify the installed version:

```bash
ts-tokenizer --version
```

To work with the source checkout:

```bash
git clone https://github.com/tanerim/ts_tokenizer.git
cd ts_tokenizer
python -m pip install -e .
```

The source checkout may contain changes that are not yet published to PyPI.
Continue with [Python API](Python-API) or [CLI](CLI).
