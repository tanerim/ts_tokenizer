# TS Tokenizer

A rule-based (old-fashioned) Turkish Tokenizer.

## Classes

## CharFix

This method replaces non-UTF characters.

### CharFix Class
```python
```python
from ts_tokenizer.char_fix import CharFix
```


```python
line = "ParÃ§a ve bÃ¼tÃ¼n iliåÿkisi ''her zaman'' iåÿlevsel deðildir."
fixed_chars = CharFix.fix(line)
print(fixed_chars)
> Parça ve bütün ilişkisi "her zaman" işlevsel değildir.
```

### Fix Characters

```python
line = "ParÃ§a ve bÃ¼tÃ¼n iliåÿkisi her zaman iåÿlevsel deðildir."
fix_chars = CharFix.fix(line)
print(fix_chars)
> Parça ve bütün ilişkisi her zaman işlevsel değildir.
```
### Fix Lowercase

```python
line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
tr_lowercase = CharFix.fix_tr_lowercase(line)
print(tr_lowercase)
> istanbul ve ığdır ''arası'' 1528 km'dir.
```
### Fix Quotes

```python
line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
fix_quotes = CharFix.fix_quote(line)
print(quotes)
> İstanbul ve Iğdır "arası" 1528 km'dir.
```