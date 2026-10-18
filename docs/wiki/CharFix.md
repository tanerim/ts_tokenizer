# Character correction

CharFix offers methods to correct corrupted Turkish text:

You can use these helpers either through `CharFix` or as direct package-level functions:

```python
from ts_tokenizer import CharFix, fix, tr_lowercase, fix_quote

text = "İSTANBUL"
assert CharFix.fix(text) == fix(text)
assert CharFix.tr_lowercase(text) == tr_lowercase(text)
assert CharFix.fix_quote(text) == fix_quote(text)
```

Existing imports from `ts_tokenizer.char_fix` remain supported. Both styles
accept and return strings; class methods are available through IDE autocomplete.

### Fix Characters

```python
from ts_tokenizer import fix

line = "ParÃ§a ve bÃ¼tÃ¼n iliåÿkisi her zaman iåÿlevsel deðildir."
print(fix(line))  # Fixes corrupted characters
```
```bash
$ Parça ve bütün ilişkisi her zaman işlevsel değildir.
```
### Lowercase

```python
from ts_tokenizer import tr_lowercase

line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
print(tr_lowercase(line))
```
```bash
$ istanbul ve ığdır ''arası'' 1528 km'dir.
```
### Fix Quotes

```python
from ts_tokenizer import fix_quote

line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
print(fix_quote(line))
```
    $ İstanbul ve Iğdır "arası" 1528 km'dir.
