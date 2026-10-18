# Output formats

```python
from ts_tokenizer import OutputFormat, tokenize

result = tokenize("Merhaba dünya.", OutputFormat.TAGGED_LINES)
```

| Enum member | Legacy string / CLI value | Python result (`output=False`) |
| --- | --- | --- |
| `OutputFormat.TOKENIZED` | `tokenized` | `str`: one token per line |
| `OutputFormat.LINES` | `lines` | `str`: tokens separated by spaces |
| `OutputFormat.TAGGED` | `tagged` | `str`: one `token<TAB>tag` pair per line |
| `OutputFormat.TAGGED_LINES` | `tagged_lines` | `list`: `(token, tag)` tuples |

`tokenize(text)` defaults to `OutputFormat.TOKENIZED`. All four legacy strings
remain accepted. Invalid formats raise `ValueError`.
`LINES` and `TAGGED_LINES` do not preserve original newline boundaries within
a single call; see [Python API](Python-API).

## JSON serialization

With `output=True`, `TAGGED` and `TAGGED_LINES` return a JSON array of objects
with `token` and `tag` fields. `LINES` returns a JSON object with a `tokens`
array. `TOKENIZED` remains a plain string.

```python
import json
from ts_tokenizer import OutputFormat, tokenize

payload = tokenize("Merhaba dünya.", OutputFormat.TAGGED, output=True)
items = json.loads(payload)
```

`output=True` is a Python API option; it is not the CLI's `--output` flag.

## XML-only input

A recognized standalone XML tag is a special case. `TAGGED` returns
`tag<TAB>XML_Tag`, or a single JSON object with `output=True`. Other formats
return the stripped XML string unchanged, including `TAGGED_LINES`.
Callers expecting a list should account for this existing behavior.
