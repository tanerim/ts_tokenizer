# TS Tokenizer Documentation

TS Tokenizer is a hybrid, lexicon-based and rule-based tokenizer for Turkish.
It can be used as a Python library or a command-line tool.

This documentation describes version **0.3.0**.

## Start here

- [Installation](Installation): requirements and installation.
- [Python API](Python-API): return tokenization results to Python code.
- [Command line](CLI): process files and piped input.
- [Output formats](Output-Formats): select a representation with `OutputFormat`.
- [Character correction](CharFix): normalize Turkish text.
- [Local data](Local-Data): access bundled lexical resources.
- [Token tags](Token-Tags): reference table of token classifications.
- [Compatibility and FAQ](Compatibility): legacy calls and common questions.

## Quick start

```python
from ts_tokenizer import tokenize

print(tokenize("Merhaba dünya."))
```

```text
Merhaba
dünya
.
```

For command-line use:

```bash
printf 'Merhaba dünya.\n' | ts-tokenizer
```

[Source code](https://github.com/tanerim/ts_tokenizer) ·
[Report an issue](https://github.com/tanerim/ts_tokenizer/issues)
