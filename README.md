# TS Tokenizer

**TS Tokenizer** is a hybrid tokenizer designed specifically for tokenizing Turkish texts.
It uses a hybrid (lexicon-based and rule-based) approach to split text into tokens.


### Key Features:
- **Hybrid Approach**: Uses a hybrid (lexicon-based and rule-based approach) for tokenization.
- **Handling of Special Tokens**: Recognizes special tokens like mentions, hashtags, emails, URLs, numbers, smiley, emoticons, etc.
- **Highly Configurable**: Provides multiple output formats to suit different NLP processing needs, including plain tokens, tagged tokens, and token-tag pairs in list or line formats.

On natural language processing (NLP), information retrieval, or text mining for Turkish, **TS Tokenizer** offers
a reliable solution for tokenization.

---

## Installation

You can install the ts-tokenizer package using pip.

    pip install ts-tokenizer

Ensure you have Python 3.9 or higher installed on your system.

You can update current version using pip

    pip install --upgrade ts-tokenizer
---

## Command line tool

You can use TS Tokenizer directly from the command line for both file inputs and pipeline processing:
## Tokenize from a File:

    $ ts-tokenizer input.txt

or
    
    $ cat input.txt | ts-tokenizer

## Tokenizing with Piped Input:

    $ zcat input.txt.gz | ts-tokenizer

---

## Help

Get detailed help for available options using:
    
    $ ts-tokenizer --help
    
    usage: main.py [-h] [-o {tokenized,lines,tagged,tagged_lines}] [-v] [-n NUM_WORKERS]
                   [filename]
    
    Tokenizer Script
    
    positional arguments:
      filename              Name of the file to process (optional if input is piped)
    
    options:
      -h, --help            show this help message and exit
      -o {tokenized,lines,tagged,tagged_lines}, --output {tokenized,lines,tagged,tagged_lines}
                            Specify the output format
      -v, --verbose         Enable verbose mode
      -n NUM_WORKERS, --num-workers NUM_WORKERS
                            Number of parallel workers

---

## CLI Arguments

You can specify the output format using the -o option:

- **tokenized (default):** Returns plain tokens, one per line.
- **tagged:** Returns tokens with their tags.
- **lines:** Returns tokenized lines as lists.
- **tagged_lines:** Returns tokenized lines as a list of tuples (token, tag).

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

Note that **tags are not part-of-speech tags** but they define the given string.
    
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

    [('Queen', 'English_Word'), (',', 'Punc'), ('31.10.1975', 'Date'), ('tarihinde', 'Valid_Word'), ('çıkardığı', 'Valid_Word'), ('A', 'OOV'), ('Night', 'English_Word'), ('at', 'Valid_Word'), ('the', 'English_Word'), ('Opera', 'Valid_Word'), ('albümüyle', 'Valid_Word'), ('dünya', 'Valid_Word'), ('müziğini', 'Valid_Word'), ('değiştirdi', 'Valid_Word'), ('.', 'Punc')]

---

## Parallel Processing
Use the -n option to set the number of parallel workers:

    $ ts-tokenizer -n 2 -o tagged input_file

By default, TS Tokenizer uses [number of CPU cores - 1].

---

## Using CLI Arguments with pipelines

You can use TS Tokenizer in bash pipelines, such as counting word frequencies:

Following sample returns calculated  frequencies for the given file:

    $ ts-tokenizer input.txt | sort | uniq -c | sort -n

---

To count tags:

    $ts-tokenizer -o tagged input.txt | cut -f2 | sort | uniq -c
        1 Date
        3 English_Word
        2 Hashtag
        2 Mention
        1 Multi_Hyphenated
        3 Numbered_Title
        1 OOV
        9 Punc
        1 Single_Hyphenated
        17 Valid_Word


To find a specific tag following command could be used.

    $ ts-tokenizer -o tagged input.txt | cut -f1,2 | grep "Web_URL"
    www.wikipedia.org	Web_URL
    www.wim-wenders.com	Web_URL
    www.winterwar.com.	Web_URL
    www.wissenschaft.de:	Web_URL
    www.wittingen.de	Web_URL
    www.wlmqradio.com	Web_URL
    www.worldstadiums.com	Web_URL
    www.worldstatesmen.org	Web_URL


---

# Classes

## CharFix

CharFix offers methods to correct corrupted Turkish text:

### Fix Characters

```python
from ts_tokenizer.char_fix import CharFix

line = "ParÃ§a ve bÃ¼tÃ¼n iliåÿkisi her zaman iåÿlevsel deðildir."
print(CharFix.fix(line))  # Fixes corrupted characters

```
### Lowercase

```python
from ts_tokenizer.char_fix import CharFix

line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
print(CharFix.tr_lowercase(line))
```
    $istanbul ve ığdır ''arası'' 1528 km'dir.

### Fix Quotes

```python
from ts_tokenizer.char_fix import CharFix

line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
print(CharFix.fix_quote(line))
```
    $ İstanbul ve Iğdır "arası" 1528 km'dir.


## Punctuation Check
This method returns information about the punctuations in given word.

## PuncMatcher Class

This class has 6 methods. They return information about punctuations in given string.

### punc_count
This method returns number of punctuations in given string as list

```python
from ts_tokenizer.punctuation_process import PuncMatcher

sample_one = "ornek,"
sample_two = "kalem,kitap,defter"

print(PuncMatcher.punc_count(sample_one))
$1
print(PuncMatcher.punc_count(sample_two))
$3
```
---

### punc_pos
This method returns indexes of punctuations in given string as list

```python
from ts_tokenizer.punctuation_process import PuncMatcher

sample_one = "ornek,"
sample_two = "kalem,kitap,defter"

print(PuncMatcher.punc_pos(sample_one))
$[5]
print(PuncMatcher.punc_pos(sample_two))
$[5, 11]
```

---
## TokenHandler


```python
from ts_tokenizer.token_handler import TokenPreProcess

```


### Below are the list of tags generated by tokenizer to process tokens:


| #  | Function                    | Sample                       | Used As Output | Tag                |
|----|-----------------------------|------------------------------|----------------|--------------------|
| 01 | is_mention                  | tanersezerr@gmail.com        | Yes            | Mention            |
| 02 | is_hashtag                  | #ts-tokenizer                | Yes            | Hashtag            |
| 03 | is_in_quotes                | "ts-tokenizer"               | No             | -----              |
| 04 | is_numbered_title           | (1)                          | Yes            | Numbered_Title     |
| 05 | is_in_paranthesis           | (bilgisayar)                 | No             | -----              |
| 06 | is_date_range               | 01.01.2024-01.01.2025        | Yes            | Date_Range         |
| 07 | is_complex_punc             | -yeniden,sonradan..          | No             | -----              |
| 08 | is_date                     | 22.02.2016                   | Yes            | Date               |
| 09 | is_hour                     | 14.05                        | Yes            | Hour               |
| 10 | is_percentage_numbers       | %75                          | Yes            | Percentage_Numbers |
| 11 | is_percentage_numbers_chars | %75'lik                      | Yes            | Percentage_Numbers |
| 12 | is_roman_number             | XI                           | Yes            | Roman_Number       |
| 13 | is_bullet_list              | •Giriş                       | Yes            | BUllet_List        |
| 14 | is_email                    | tanersezerr@gmail.com        | Yes            | Email              |
| 15 | is_email_punc               | tanersezerr@gmail.com.       | No             | -----              |
| 16 | is_full_url                 | https://tscorpus.com         | Yes            | Full_URL           |
| -- | is_full_url                 | www.example.com'un           | Yes            | URL_Suffix         |
| 17 | is_web_url                  | www.tscorpus.com             | Yes            | Web_URL            |
| 18 | is_copyright                | ©tscorpus                    | Yes            | Copyright          |
| 19 | is_registered               | tscorpus®                    | Yes            | Registered         |
| 20 | is_trademark                | tscorpus™                    | Yes            | Trademark          |
| 21 | is_currency                 | 100$                         | Yes            | Currency           |
| 22 | is_num_char_sequence        | 380A                         | No             | -----              |
| 23 | is_abbr                     | TBMM                         | Yes            | Abbr               |
| 24 | is_in_lexicon               | bilgisayar                   | Yes            | Valid_Word         |
| 25 | is_in_exceptions            | e-mail                       | Yes            | Exception          |
| 26 | is_in_eng_words             | computer                     | Yes            | English_Word       |
| 27 | is_smiley                   | :)                           | Yes            | Smiley             |
| 28 | is_multiple_smiley          | :):)                         | No             | -----              |
| 29 | is_emoticon                 | 🍻                           | Yes            | Emoticon           |
| 30 | is_multiple_emoticon        | 🍻🍻                         | No             | -----              |
| 31 | is_multiple_smiley_in       | hey:):)                      | No             | -----              |
| 32 | is_number                   | 175.01                       | Yes            | Number             |
| 33 | is_apostrophed              | Türkiye'nin                  | Yes            | Apostrophed        |
| 34 | is_single_punc              | !                            | Yes            | Punc               |
| 35 | is_multi_punc               | !!                           | No             | -----              |
| 36 | is_single_hyphenated        | sabah-akşam                  | Yes            | Single_Hyphenated  |
| 37 | is_multi_hyphenated         | çay-su-kahve                 | Yes            | Multi-Hyphenated   |
| 38 | is_single_underscored       | Gel_Git                      | Yes            | Single_Underscored |
| 39 | is_multi_underscored        | Yarı_Yapılandırılmış_Mülakat | Yes            | Multi_Underscored  |
| 40 | is_one_char_fixable         | bilgisa¬yar                  | Yes            | One_Char_Fixed     |
| 42 | is_three_or_more            | heyyyyy                      | No             | -----              |
| 43 | is_fsp                      | bilgisayar.                  | No             | -----              |
| 44 | is_isp                      | .bilgisayar                  | No             | -----              |
| 45 | is_fmp                      | bilgisayar..                 | No             | -----              |
| 46 | is_imp                      | ..bilgisayar                 | No             | -----              |
| 47 | is_msp                      | --bilgisayar--               | No             | -----              |
| 48 | is_mssp                     | -bilgisayar-                 | No             | -----              |
| 49 | is_midsp                    | okul,öğrenci                 | No             | -----              |
| 50 | is_midmmp                   | okul,öğrenci, öğretmen       | No             | -----              |
| 51 | is_non_latin                | 한국드                          | No             | Non_Latin          |







