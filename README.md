# TS Tokenizer

TS Tokenizer is a Turkish Tokenizer.

## Classes

## CharFix

This class has 4 methods. They are useful to fix corrupted texts.

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


## TokenPreProcess

This class is used to pass input tokens to the tokenizer for further analysis.
However, it could be used for various tasks.
The tags are "Valid_Word", "Exception_Word", "Eng_Word", "Date", "Hour", "In_Parenthesis", "In_Quotes", "Smiley", "Inner_Char", "Abbr", "Number", "Non_Prefix_URL", "Prefix_URL", "Emoticon", "Mention", "HashTag", "Percentage_Numbers", "Percentage_Number_Chars", "Num_Char_Seq", "Multiple_Smiley", "Punc", "Underscored", "Hyphenated", "Hyphen_In", "Multiple_Emoticon", "Copyright", "Email", "Registered", "Three_or_More"

### token_tagger

```python
from ts_tokenizer.token_preprocess import TokenPreProcess
```

### Default Usage
```python
word = "''arası''"
TokenTag = TokenPreProcess.token_tagger(word)
print(TokenTag)
> In_Quotes
```

```python
word = "#tstokenizer"
print(TokenPreProcess.token_tagger(word, output='all', output_format='tuple'))  # Returns a tuple
> ('#tstokenizer', '#tstokenizer', 'HashTag')

word = "#tanerim"
print(TokenPreProcess.token_tagger(word, output='all', output_format='list'))   # Returns a list
> ['@tanerim', '@tanerim', 'Mention']

word = "16:37"
print(TokenPreProcess.token_tagger(word, output='all', output_format='json'))   # Returns a JSON string
> {"input_token": "16:37", "fixed_token": "16:37", "tag": "Hour"}
```

```python
line = "Queen 31.10.1975 tarihinde çıkardığı A Night at the Opera albümüyle dünya müziğini değiåÿtirdi ."

for word in line.split(" "):
    TokenTag = TokenPreProcess.token_tagger(word, output='all', output_format='list')
    print(TokenTag)
['Queen', 'Queen', 'Eng_Word']
['31.10.1975', '31.10.1975', 'Date']
['tarihinde', 'tarihinde', 'Valid_Word']
['çıkardığı', 'çıkardığı', 'Valid_Word']
['A', 'A', 'OOV']
['Night', 'Night', 'Eng_Word']
['at', 'at', 'Valid_Word']
['the', 'the', 'Eng_Word']
['Opera', 'Opera', 'Valid_Word']
['albümüyle', 'albümüyle', 'Valid_Word']
['dünya', 'dünya', 'Valid_Word']
['müziğini', 'müziğini', 'Valid_Word']
['değiåÿtirdi', 'değiştirdi', 'Valid_Word']
['.', '.', 'Punc']
```
