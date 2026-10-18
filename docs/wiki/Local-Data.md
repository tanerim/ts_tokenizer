# Local data

Bundled lexical resources can also be accessed directly from the package.

Use named helpers to select a resource through IDE autocomplete without string arguments:

```python
from ts_tokenizer import smileys_data, word_list_data

print(":)" in smileys_data())
print("istanbul" in word_list_data())
```

Each dataset listed below has a corresponding `<name>_data()` helper, such as
`abbrs_data()` or `domains_data()`.

The generic string accessor remains supported:

```python
from ts_tokenizer import get_data

smileys = get_data("smileys")
print(":)" in smileys)
```

Available dataset names for `get_data(...)`:

- `emoticons`
- `smileys`
- `abbrs`
- `word_list`
- `correction_mark`
- `exception_words`
- `eng_word_list`
- `domains`
- `currency_symbols`

`get_data(...)` and the named `*_data()` helpers return `frozenset[str]`
copies, so callers cannot mutate the tokenizer's in-memory resources through them.
Unknown names passed to `get_data(...)` raise `ValueError`.

Existing `LocalData` calls and imports from `ts_tokenizer.data` remain supported:

```python
from ts_tokenizer import LocalData

print(":)" in LocalData.smileys())
print("istanbul" in LocalData.word_list())
```

`LocalData` methods retain their original behavior: they return shared, mutable
`set[str]` objects. Changing these sets changes the tokenizer's in-memory
resources. Prefer the frozen helpers when you only need to read data.
`LocalData.candidate_abbrs()` also remains available; it has no corresponding
`get_data(...)` entry or named helper.
