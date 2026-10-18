# Python API

## Tokenize text

```python
from ts_tokenizer import tokenize

result = tokenize("Merhaba dünya.")
print(result)
```

`tokenize(line, return_format=OutputFormat.TOKENIZED, output=False)` returns a
value; it does not print it. The default result is a newline-delimited string.

Select formats through IDE autocomplete:

```python
from ts_tokenizer import OutputFormat, tokenize

pairs = tokenize("Merhaba dünya.", OutputFormat.TAGGED_LINES)
for token, tag in pairs:
    print(token, tag)
```

See [Output formats](Output-Formats) for return types and XML handling.

## Multiple input lines

A single `tokenize()` call splits text on whitespace, including newlines.
To preserve input line boundaries, call it for each line:

```python
from ts_tokenizer import OutputFormat, tokenize

text = "Merhaba dünya.\nİkinci satır."
results = [tokenize(line, OutputFormat.TAGGED_LINES) for line in text.splitlines()]
```

`tokenize()` does not automatically run the full character-correction pipeline.
Apply [CharFix](CharFix) explicitly when needed:

```python
from ts_tokenizer import fix, tokenize

result = tokenize(fix("ParÃ§a"))
```

## Print-oriented processing

`TSTokenizer.ts_tokenize()` prints results and returns `None`:

```python
from ts_tokenizer import OutputFormat, TSTokenizer

TSTokenizer.ts_tokenize(
    input_file="Merhaba dünya.\nİkinci satır.",
    output_format=OutputFormat.TOKENIZED,
)
```

For file processing, pass `filename="input.txt"` and optionally `num_workers=2`.
The filename path applies `CharFix.fix()` to each line before tokenization.
The `input_file` parameter accepts text, despite its name; it is not a file object.
If both input arguments are supplied, `input_file` takes precedence.
`verbose` is accepted for compatibility and has no effect.
