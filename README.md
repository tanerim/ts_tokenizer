# TS Tokenizer

ts-tokenizer is a rule-based tokenizer specifically designed for processing Turkish text.

It provides functionalities to split text into tokens following the grammatical and linguistic rules of the Turkish language.

# Installation
You can install the ts-tokenizer package using pip. Ensure you have Python 3.9 or higher installed on your system.

```bash
pip install ts-tokenizer
```

# CLI notes

Basic usage. It prints tokenized output
```bash
python main.py [file]
```

Enables verbose mode
```bash
python main.py -v [file] >> [output_file]
```

--output
parameter selects process mode.

tokenized is default option

tagged returns candidate tags for token.

details information about candidate tags
```bash
python main.py --output [tagged, details, tokenized] [file]
```


```bash
python main.py -w [word]
```


## Classes

## CharFix

This class has 4 methods. They are useful to fix corrupted texts.

### CharFix Class

```python
from ts_tokenizer.char_fix import CharFix
```

### Fix Characters

```python
line = "ParÃ§a ve bÃ¼tÃ¼n iliåÿkisi her zaman iåÿlevsel deðildir."
fix_chars = CharFix.fix(line)
print(fix_chars)
Parça ve bütün ilişkisi her zaman işlevsel değildir.
```
### Lowercase

```python
line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
tr_lowercase = CharFix.tr_lowercase(line)
print(tr_lowercase)
istanbul ve ığdır ''arası'' 1528 km'dir.
```
### Fix Quotes

```python
line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
fix_quotes = CharFix.fix_quote(line)
print(quotes)
İstanbul ve Iğdır "arası" 1528 km'dir.
```


## TokenCheck

This class is used to pass input tokens to the tokenizer for further analysis.
However, it could be used for various tasks.<br>
The tags are "Valid_Word", "Exception_Word", "Eng_Word", "Date", "Hour", "In_Parenthesis", "In_Quotes", "Smiley", "Inner_Char", "Abbr", "Number", "Non_Prefix_URL", "Prefix_URL", "Emoticon", "Mention", "HashTag", "Percentage_Numbers", "Percentage_Number_Chars", "Num_Char_Seq", "Multiple_Smiley", "Punc", "Underscored", "Hyphenated", "Hyphen_In", "Multiple_Emoticon", "Copyright", "Email", "Registered", "Three_or_More"

### token_tagger

```python
from ts_tokenizer.token_check import TokenCheck
```

### Default Usage
```python
word = "''arası''"
TokenTag = TokenCheck.token_tagger(word)
print(TokenTag)
In_Quotes
```

```python
word = "#tstokenizer"
print(TokenCheck.token_tagger(word, output='all', output_format='tuple'))  # Returns a tuple
('#tstokenizer', '#tstokenizer', 'HashTag')

word = "#tanerim"
print(TokenCheck.token_tagger(word, output='all', output_format='list'))   # Returns a list
['@tanerim', '@tanerim', 'Mention']

word = "16:37"
print(TokenCheck.token_tagger(word, output='all', output_format='json'))   # Returns a JSON string
{"input_token": "16:37", "fixed_token": "16:37", "tag": "Hour"}

word = "16:37"
print(TokenCheck.token_tagger(word, output='all', output_format='json'))   # Returns a JSON string
{"input_token": "16:37", "fixed_token": "16:37", "tag": "Hour"}

word = ":):):)"
print(TokenCheck.token_tagger(word, output='all', output_format='string'))   # Returns a tab-separated string
:):):)  :):):)  Multiple_Smiley
```

```python
line = "Queen , 31.10.1975 tarihinde çıkardıðı A Night at the Opera albÃ¼mÃ¼yle dÃ¼nya mÃ¼ziðini deðiåÿtirdi ."

for word in line.split(" "):
    TokenTag = TokenCheck.token_tagger(word, output='all', output_format='list')
    print(TokenTag)
['Queen', 'Queen', 'Eng_Word']
[',', ',', 'Punc']
['31.10.1975', '31.10.1975', 'Date']
['tarihinde', 'tarihinde', 'Valid_Word']
['çıkardıðı', 'çıkardığı', 'Valid_Word']
['A', 'A', 'OOV']
['Night', 'Night', 'Eng_Word']
['at', 'at', 'Valid_Word']
['the', 'the', 'Eng_Word']
['Opera', 'Opera', 'Valid_Word']
['albÃ¼mÃ¼yle', 'albümüyle', 'Valid_Word']
['dÃ¼nya', 'dünya', 'Valid_Word']
['mÃ¼ziðini', 'müziğini', 'Valid_Word']
['deðiåÿtirdi', 'değiştirdi', 'Valid_Word']
['.', '.', 'Punc']

```
