# Compatibility and FAQ

## Do existing imports still work?

Yes. Package-level imports and imports from `ts_tokenizer.tokenizer`,
`ts_tokenizer.char_fix`, and `ts_tokenizer.data` remain supported.

```python
from ts_tokenizer.tokenizer import tokenize
from ts_tokenizer.char_fix import CharFix
from ts_tokenizer.data import LocalData

result = tokenize("Merhaba", "tokenized")
```

## Do I have to use OutputFormat?

No. Valid string names remain accepted. `OutputFormat` adds named choices for
IDE completion, and `tokenize(text)` now defaults to the tokenized format.

Invalid formats now raise `ValueError`. Earlier code logged an error and
returned `None` for ordinary text; XML input could bypass format validation.

## Why is LocalData mutable?

Existing `LocalData` methods return shared sets. That behavior is retained.
Use `get_data()` or the named `*_data()` helpers for frozen copies.
See [Local data](Local-Data).

## Is tqdm still required?

No. Version 0.3.0 removes the dependency and progress bars. `verbose=True` and
CLI `-v` remain accepted but have no effect.

## Does tagged_lines always return a list?

Recognized standalone XML tags return a string. See [Output formats](Output-Formats).

## Does tokenize correct corrupted characters?

Use `tokenize(fix(text))` when correction is needed. File processing through
`TSTokenizer.ts_tokenize(filename=...)` applies `CharFix.fix()` per line.
