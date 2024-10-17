# TS Tokenizer

**TS Tokenizer** is a hybrid tokenizer designed for Turkish text.
It uses a hybrid (lexicon-based and rule-based) approach to split text into tokens.
The tokenizer leverages regular expressions to handle non-standard text elements like dates, percentages, URLs, and punctuation marks.


### Key Features:
- **Hybrid Approach**: Uses a hybrid (lexicon-based and rule-based approach) for tokenization.
- **Handling of Special Tokens**: Recognizes special tokens like mentions, hashtags, emails, URLs, numbers, smiley, emoticons, etc..
- **Highly Configurable**: Provides multiple output formats to suit different NLP processing needs,
- including plain tokens, tagged tokens, and token-tag pairs in list or line formats.

Whether you are working on natural language processing (NLP), information retrieval, or text mining for Turkish, **TS Tokenizer** offers
a versatile and reliable solution for tokenization.


# Installation

You can install the ts-tokenizer package using pip. Ensure you have Python 3.9 or higher installed on your system.

    pip install ts-tokenizer

## Command line tool
Basic usage returns tokenized output of given text file.

    $ ts-tokenizer input.txt

## CLI Arguments

-o parameter takes four arguments.

The two arguments 'tokenized' and 'tagged' returns word/per/line output.
Tokenized is the default value and it is not obligatory to declare.

input_text = "Queen , 31.10.1975 tarihinde çıkardıðı A Night at the Opera albÃ¼mÃ¼yle dÃ¼nya mÃ¼ziðini deðiåÿtirdi ."

    $ ts-tokenizer input text

    Queen
    ,
    31.10.1975
    tarihinde
    çıkardığı
    A
    Night
    at
    the
    Opera
    albümüyle
    dünya
    müziğini
    değiştirdi
    .

Note that tags are not part-of-speech tags but they define the given string.
    
    $ ts-tokenizer -o tagged input.txt

    Queen	English_Word
    ,	Punc
    31.10.1975	Date
    tarihinde	Valid_Word
    çıkardığı	Valid_Word
    A	OOV
    Night	English_Word
    at	Valid_Word
    the	English_Word
    Opera	Valid_Word
    albümüyle	Valid_Word
    dünya	Valid_Word
    müziğini	Valid_Word
    değiştirdi	Valid_Word
    .	Punc


The other two arguments are "lines" and "tagged_lines".
The "lines" parameter reads input file line-by-line and returns a list for each line.

    $ ts-tokenizer -o lines input.txt

    ['Queen', ',', '31.10.1975', 'tarihinde', 'çıkardığı', 'A', 'Night', 'at', 'the', 'Opera', 'albümüyle', 'dünya', 'müziğini', 'değiştirdi', '.']

The "tagged_lines" parameter reads input file line-by-line and returns a list of tuples for each line.


    $ ts-tokenizer -o tagged_lines input.txt

    [('Queen', 'English_Word'), (',', 'Punc'), ('31.10.1975', 'Date'), ('tarihinde', 'Valid_Word'), ('çıkardığı', 'Valid_Word'), ('A', 'OOV'), ('Night', 'English_Word'), ('at', 'Valid_Word'), ('the', 'English_Word'), ('Opera', 'Valid_Word'), ('albümüyle', 'Valid_Word'),('dünya', 'Valid_Word'), ('müziğini', 'Valid_Word'), ('değiştirdi', 'Valid_Word'), ('.', 'Punc')]

-w parameter reads given word/sentence on bash cli. Note that this parameter get only one word and omits whitespaces.

    $ ts-tokenizer -w "yenilikçi"
    
    yenilikçi

    $ ts-tokenizer -w -o tagged "yenilikçi"

    yenilikçi	Valid_Word

The tokenizer is designed to take advantge of multiple cores. Default value is [Total Number of Cores - 1].
-j parameter sets the number of parallel workers.

    $ ts-tokenizer -j 2 -o tagged input_file

## Using CLI Arguments with pipelines

ts-tokenizer could also be used in a pipeline on bash.

Following sample returns calculated  frequencies for the given file:

    $ ts-tokenizer input.txt | sort | uniq -c | sort -n

For case-insensitive output tr is employed in the sample below:

    $ ts-tokenizer input.txt | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -n

Sample below returns number of tags in given text

    $ts-tokenizer -o tagged input.txt | cut -f3 | sort | uniq -c
      1 Hyphen_In
      1 Inner_Punc
      2 FMP
      8 ISP
      8 Num_Char_Seq
     12 Number
     24 Apostrophe
     25 OOV
     69 FSP
    515 Valid_Word

To find a specific tag following command could be used.

    $ ts-tokenizer -o tagged input.txt | cut -f2,3 | grep "Num_Char_Seq"
    40'ar	Num_Char_Seq
    2.	Num_Char_Seq
    24.	Num_Char_Seq
    Num_Char_Seq
    16'sı	Num_Char_Seq
    8.	Num_Char_Seq
    20'şer	Num_Char_Seq
    40'ar	Num_Char_Seq

By employing sort and uniq commands frequency of the words with target tag could be found:

    $ ts-tokenizer -o tagged Test_Text.txt | cut -f2,3 | grep "Num_Char_Seq" | sort | uniq -c | sort -n
      1 16'sı	Num_Char_Seq
      1 20'şer	Num_Char_Seq
      1 2.	Num_Char_Seq
      1 8.	Num_Char_Seq
      2 24.	Num_Char_Seq
      2 40'ar	Num_Char_Seq



--help returns help
    
    $ ts-tokenizer --help

    usage: main.py [-h] [-o {tokenized,lines,tagged,tagged_lines}] [-w] [-v] [-j JOBS] filename

    positional arguments:
      filename              Name of the file to process
    
    options:
      -h, --help            show this help message and exit
      -o {tokenized,lines,tagged,tagged_lines}, --output {tokenized,lines,tagged,tagged_lines}
                            Specify the output format
      -w, --word            Enable CLI input mode
      -v, --verbose         Enable verbose mode
      -j JOBS, --jobs JOBS  Number of parallel workers


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
print(CharFix.fix(line))

Parça ve bütün ilişkisi her zaman işlevsel değildir.
```
### Lowercase

```python
line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
print(CharFix.tr_lowercase(line))

istanbul ve ığdır ''arası'' 1528 km'dir.
```
### Fix Quotes

```python
line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
print(CharFix.fix_quote(line))

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
word = "ParÃ§a"
print(TokenCheck.token_tagger(word))

$ Valid_Word

print(TokenCheck.token_tagger(word, output="all", output_format="tuple"))

$ ('ParÃ§a', 'Parça', 'Valid_Word')

print(TokenCheck.token_tagger(word, output="all", output_format="list"))

$ ['ParÃ§a', 'Parça', 'Valid_Word']

word = "#tstokenizer"
print(TokenCheck.token_tagger(word, output='all', output_format='tuple'))  # Returns a tuple
('#tstokenizer', '#tstokenizer', 'HashTag')

word = "#tanerim"
print(TokenCheck.token_tagger(word, output='all', output_format='list'))   # Returns a list
['@tanerim', '@tanerim', 'Mention']

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
