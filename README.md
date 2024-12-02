# TS Tokenizer

**TS Tokenizer** is a hybrid tokenizer designed specifically for tokenizing Turkish texts.
It uses a hybrid (lexicon-based and rule-based) approach to split text into tokens.


### Key Features:
- **Hybrid Approach**: Uses a hybrid (lexicon-based and rule-based approach) for tokenization.
- **Handling of Special Tokens**: Recognizes special tokens like mentions, hashtags, emails, URLs, numbers, smiley, emoticons, etc..
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
    $ 1
print(PuncMatcher.punc_count(sample_two))
    $ 3
```
---

### punc_pos
This method returns indexes of punctuations in given string as list

```python
from ts_tokenizer.punctuation_process import PuncMatcher

sample_one = "ornek,"
sample_two = "kalem,kitap,defter"

print(PuncMatcher.punc_pos(sample_one))
    $ [5]
print(PuncMatcher.punc_pos(sample_two))
    $ [5. 11]
```

---

## Below are the list of tags generated by tokenizer in their process order:


lexicon_based = [
    TokenPreProcess.is_in_exceptions,
    TokenPreProcess.is_emoticon,
    TokenPreProcess.is_smiley,
    TokenPreProcess.is_abbr,
    TokenPreProcess.is_in_lexicon,
    TokenPreProcess.is_in_eng_words,
    TokenPreProcess.is_single_punc,
]

regex = [
    TokenPreProcess.is_full_url,
    TokenPreProcess.is_web_url,
    TokenPreProcess.is_email,
    TokenPreProcess.is_currency,
    TokenPreProcess.is_date_range,
    TokenPreProcess.is_date,
    TokenPreProcess.is_hour,
    TokenPreProcess.is_number,
    TokenPreProcess.is_mention,
    TokenPreProcess.is_hashtag,
    TokenPreProcess.is_in_quotes,
    TokenPreProcess.is_apostrophed,
    TokenPreProcess.is_numbered_title,
    TokenPreProcess.is_in_parenthesis,
    TokenPreProcess.is_roman_number,
    TokenPreProcess.is_registered,
    TokenPreProcess.is_copyright,
    TokenPreProcess.is_trademark,
    TokenPreProcess.is_bullet_list,
    TokenPreProcess.is_roman_number,
    TokenPreProcess.is_percentage_numbers_chars,
    TokenPreProcess.is_percentage_numbers,
    TokenPreProcess.is_multiple_smiley_in,
    TokenPreProcess.is_multiple_smiley,
]

single_punc = [
    TokenPreProcess.is_single_hyphenated,
    TokenPreProcess.is_multi_hyphenated,
    TokenPreProcess.is_single_underscored,
    TokenPreProcess.is_multi_underscored,
    TokenPreProcess.is_midsp,
    TokenPreProcess.is_midmp,
    TokenPreProcess.is_isp,
    TokenPreProcess.is_fsp,
    TokenPreProcess.is_apostrophed,
    TokenPreProcess.is_copyright,
    TokenPreProcess.is_registered,
    TokenPreProcess.is_trademark,
    TokenPreProcess.is_bullet_list,
]

multi_punc = [
    TokenPreProcess.is_fmp,
    TokenPreProcess.is_imp,
    TokenPreProcess.is_mssp,
    TokenPreProcess.is_one_char_fixable,
    TokenPreProcess.is_in_parenthesis,
    TokenPreProcess.is_non_latin,
    TokenPreProcess.is_multi_punc,
    TokenPreProcess.is_msp,
    TokenPreProcess.is_num_char_sequence,
    TokenPreProcess.is_three_or_more,
    TokenPreProcess.is_complex_punc,
    TokenPreProcess.is_math,
]

    is_mention ==> tanersezerr@gmail.com
    is_hashtag ==> #ts-tokenizer
    is_in_quotes ==> "ts-tokenizer"
    is_numbered_title ==> (1)
    is_in_parenthesis ==> ()
is_date_range
is_complex_punc
is_date
is_hour
is_percentage_numbers
is_percentage_numbers_chars
is_roman_number
is_bullet_list
is_email_punc
is_email
is_full_url
is_web_url
is_copyright
is_registered
is_trademark
is_currency
is_num_char_sequence
is_abbr
is_in_lexicon
is_in_exceptions
is_in_eng_words
is_smiley
is_emoticon
is_multiple_smiley
is_multiple_smiley_in
is_multiple_emoticon
is_number
is_fsp
is_isp
is_mssp
is_msp
is_imp
is_fmp
is_apostrophed
is_single_punc
is_multi_punc
is_single_hyphenated
is_multi_hyphenated
is_single_underscored
is_multi_underscored
is_three_or_more
is_non_latin
is_one_char_fixable
is_midsp
is_midmp
is_math
