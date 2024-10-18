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

---

## Command line tool

You can use TS Tokenizer directly from the command line for both file inputs and pipeline processing:
## Tokenize from a File:

    $ ts-tokenizer input.txt

## Tokenizing with Piped Input:

    $ zcat input.txt.gz | ts-tokenizer

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

---

## Parallel Processing
Use the -j option to set the number of parallel workers:

    $ ts-tokenizer -j 2 -o tagged input_file

By default, TS Tokenizer uses [number of CPU cores - 1].

---

## Using CLI Arguments with pipelines

You can use TS Tokenizer in bash pipelines, such as counting word frequencies:

Following sample returns calculated  frequencies for the given file:

    $ ts-tokenizer input.txt | sort | uniq -c | sort -n

---

For case-insensitive output tr is employed in the sample below:

    $ ts-tokenizer input.txt | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -n

---

To count tags:

    $ts-tokenizer -o tagged input.txt | cut -f2 | sort | uniq -c
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

    $ ts-tokenizer -o tagged input.txt | cut -f1,2 | grep "Num_Char_Seq"
    40'ar	Num_Char_Seq
    2.	Num_Char_Seq
    24.	Num_Char_Seq
    Num_Char_Seq
    16'sı	Num_Char_Seq
    8.	Num_Char_Seq
    20'şer	Num_Char_Seq
    40'ar	Num_Char_Seq

---

## Help

Get detailed help for available options using:
    
    $ ts-tokenizer --help

    usage: main.py [-h] [-o {tokenized,lines,tagged,tagged_lines}] [-w] [-v] [-j JOBS] filename

    positional arguments:
      filename              Name of the file to process
    
    options:
      -h, --help            show this help message and exit
      -o {tokenized,lines,tagged,tagged_lines}, --output {tokenized,lines,tagged,tagged_lines}
                            Specify the output format
      -v, --verbose         Enable verbose mode
      -j JOBS, --jobs JOBS  Number of parallel workers

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

### find_punctuation
The find_punctuation method identifies the pattern of punctuation in a word or phrase.

The tags returned by **PuncMatcher.find_punctuation** are:
- **FSP**: Final Single Punctuation __(yeni,)__
- **ISP**: Initial Single Punctuation __(-eski)__
- **IMP**: Initial Multiple Punctuation __(..eski)__
- **FMP**: Final Multiple Punctuation __(yeni,,,)__
- **MSSP**: MultiSide Single Punctuation __(-eski,yeni,)__
- **MSP**: MultiSide Punctuation __(--eski,yeni!!)__


```python
from ts_tokenizer.punctuation_process import PuncMatcher

sample_one = "ornek,"
sample_two = ",ornek"
sample_three = "..ornek"
sample_four = "ornek.."
sample_five = ",ornek."
sample_six = "..ornek.."

print(PuncMatcher.find_punctuation(sample_one))  # Final Single Punctuation (FSP)
    $ FSP
print(PuncMatcher.find_punctuation(sample_two))  # Initial Single Punctuation (ISP)
    $ ISP
print(PuncMatcher.find_punctuation(sample_three))  # Initial Multiple Punctuation (IMP)
    $ IMP
print(PuncMatcher.find_punctuation(sample_four))  # Final Multiple Punctuation (FMP)
    $ FMP
print(PuncMatcher.find_punctuation(sample_five))  # Multi-Side Single Punctuation (MSSP)
    $ MSSP
print(PuncMatcher.find_punctuation(sample_six))  # Multi-Side Punctuation (MSP)
    $ MSP
```
---

## inner_punctuation
The inner_punctuation method identifies internal punctuation characters in the middle of a word or phrase.

```python
sample_one = "kalem,kitap"
sample_two = "kalem,kitap,defter"
sample_three = "kalem..kitap"

print(PuncMatcher.inner_punctuation(sample_one))
    $ Inner_Single_Punc
print(PuncMatcher.inner_punctuation(sample_two))
    $ Inner_Multiple_Punc
print(PuncMatcher.inner_punctuation(sample_three))
    $ Inner_Multiple_Punc
```

---

## apostrophed
This method identifies if given string that contains an apostrophe that is surronding with any characters.

```python
sample_one = "Defne'nin"
sample_two = "Defne'"
sample_three = "Defne"

print(PuncMatcher.apostrophed(sample_one))  # Output: apostrophes_in
    $ apostrophes_in
print(PuncMatcher.apostrophed(sample_two))  # Output: apostrophes_in
    $ None
print(PuncMatcher.apostrophed(sample_three))  # Output: None
    $ None
```

---

## hyphenated
This method checks if given string has a hyphen and if it has the surronding words are valid.

```python
sample_one = "gel-git"
sample_two = "gel-gitX"

print(PuncMatcher.hyphenated(sample_one))  # Output: Hyphenated
    $ Hyphenated
print(PuncMatcher.hyphenated(sample_two))  # Output: None
    $ None
```

---