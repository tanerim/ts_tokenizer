
**TS Tokenizer** is a hybrid tokenizer designed specifically for tokenizing Turkish texts.
It uses a hybrid (lexicon-based and rule-based) approach to split text into tokens.


### Key Features:
- **Hybrid Tokenization**: Combines lexicon-based and rule-based techniques to tokenize complex Turkish texts with precision.
- **Special Token Handling**: Detects and processes mentions, hashtags, emails, URLs, dates, numbers, smileys, emoticons, and more.
- **Configurable Outputs**: Offers multiple output formats, including plain tokens, tagged tokens, tokenized lines, and tagged lines, to suit diverse NLP workflows.
- **Multi-core Processing**: Speeds up tokenization for large files with parallel processing.
- **Preprocess Handling**: Handles corrupted Turkish text and punctuation gracefully using built-in fixes.
- **Command-Line Friendly**: Use it directly from the terminal for file-based or piped input workflows.


On natural language processing (NLP), information retrieval, or text mining for Turkish, **TS Tokenizer** offers
a reliable solution for tokenization.

---

## Installation

You can install the ts-tokenizer package using pip.
```bash
pip install ts-tokenizer
```
Ensure you have Python 3.9 or higher installed on your system.

You can update current version using pip
```bash
pip install --upgrade ts-tokenizer
```
---

To remove package, use:
```bash
pip uninstall ts-tokenizer
```
You can also clone the repo locally.
```bash
git clone https://github.com/tanerim/ts_tokenizer.git
cd ts-tokenizer
pip install -e .

```

---

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/tanerim/ts_tokenizer/blob/main/LICENSE) file for details.


## Command line tool

You can use TS Tokenizer directly from the command line for both file inputs and pipeline processing:
## Tokenize from a File:
```bash
ts-tokenizer input.txt
```
or
```bash
cat input.txt | ts-tokenizer
```
or
```bash
zcat input.txt.gz | ts-tokenizer
```
---

## Help

Get detailed help for available options using:

| Argument             | Short | Description                                                                                     | Default       |
|----------------------|-------|-------------------------------------------------------------------------------------------------|---------------|
| `--output`           | `-o`  | Specify the output format: `tokenized`, `lines`, `tagged`, `tagged_lines`.                      | `tokenized`   |
| `--num-workers`      | `-n`  | Set the number of parallel workers for processing.                                              | `CPU cores-1` |
| `--verbose`          | `-v`  | Enable verbose mode to display additional processing details.                                   | Disabled      |
| `--version`          | `-V`  | Display the current version of `ts-tokenizer`.                                                 | N/A           |
| `--help`             | `-h`  | Show the help message and exit.   

---

## CLI Arguments

You can specify the output format using the -o option:

- **tokenized (default):** Returns plain tokens, one per line.
- **tagged:** Returns tokens with their tags.
- **lines:** Returns tokenized lines as lists.
- **tagged_lines:** Returns tokenized lines as a list of tuples (token, tag).

```bash
input_text = "Queen , 31.10.1975 tarihinde çıkardıðı A Night at the Opera albÃ¼mÃ¼yle dÃ¼nya mÃ¼ziðini deðiåÿtirdi ."

$ ts-tokenizer input_text

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
```

Note that **tags are not part-of-speech tags** but they define the given string.
```bash
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
```

The other two arguments are "lines" and "tagged_lines".
The "lines" parameter reads input file line-by-line and returns a list for each line. Note that each line is defined by end-of-line markers in the given text.
```bash
$ ts-tokenizer -o lines input.txt

['Queen', ',', '31.10.1975', 'tarihinde', 'çıkardığı', 'A', 'Night', 'at', 'the', 'Opera', 'albümüyle', 'dünya', 'müziğini', 'değiştirdi', '.']
```

The "tagged_lines" parameter reads input file line-by-line and returns a list of tuples for each line. Note that each line is defined by end-of-line markers in the given text.
```bash
$ ts-tokenizer -o tagged_lines input.txt

 [('Queen', 'English_Word'), (',', 'Punc'), ('31.10.1975', 'Date'), ('tarihinde', 'Valid_Word'), ('çıkardığı', 'Valid_Word'), ('A', 'OOV'), ('Night', 'English_Word'), ('at', 'Valid_Word'), ('the', 'English_Word'), ('Opera', 'Valid_Word'), ('albümüyle', 'Valid_Word'), ('dünya', 'Valid_Word'), ('müziğini', 'Valid_Word'), ('değiştirdi', 'Valid_Word'), ('.', 'Punc')]
```
---

## Parallel Processing
Use the -n option to set the number of parallel workers:
```bash
$ ts-tokenizer -n 2 -o tagged input_file
```

By default, TS Tokenizer uses [number of CPU cores - 1].

---

## Using CLI Arguments with pipelines

You can use TS Tokenizer in bash pipelines, such as counting word frequencies:

Following sample returns calculated  frequencies for the given file:
```bash
$ ts-tokenizer input.txt | sort | uniq -c | sort -n
```

---

To count tags:
```bash
$ ts-tokenizer -o tagged input.txt | cut -f2 | sort | uniq -c

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
```

To find a specific tag following command could be used.
```bash
$ ts-tokenizer -o tagged input.txt | cut -f1,2 | grep "Web_URL"

www.wikipedia.org	Web_URL
www.wim-wenders.com	Web_URL
www.winterwar.com.	Web_URL
www.wissenschaft.de:	Web_URL
www.wittingen.de	Web_URL
www.wlmqradio.com	Web_URL
www.worldstadiums.com	Web_URL
www.worldstatesmen.org	Web_URL
```
---

# Classes

Below are samples to implement ts-tokenizer in Python

## TSTokenizer

**tokenized** : Outputs a list of plain tokens extracted from the input text.

```python
from ts_tokenizer.tokenizer import TSTokenizer
Single_Line_Sample = "ParÃ§a ve bÃ¼tÃ¼n iliåÿkisi her zaman iåÿlevsel deðildir."
simple_tokens = TSTokenizer.ts_tokenize(Single_Line_Sample, output_format="tokenized")
if simple_tokens is None:
    pass
else:
    for token in simple_tokens:
        print(token)
```
Generated output is as follows:

```bash
Parça
ve
bütün
ilişkisi
her
zaman
işlevsel
değildir
```
**tagged** : Outputs tokens with associated tags. Please note that these are not POSTags.
Check TokenHandler below for tag set.

```python
tagged_tokens = TSTokenizer.ts_tokenize(Single_Line_Sample, output_format="tagged")
if tagged_tokens is None:
    pass
else:
    for token in tagged_tokens:
        print(token)
```
Generated output is as follows:

```bash
Parça	Valid_Word
ve	Valid_Word
bütün	Valid_Word
ilişkisi	Valid_Word
her	Valid_Word
zaman	Valid_Word
işlevsel	Valid_Word
değildir	Valid_Word
.	Punc

```

**lines** : Maintains the structure of the input text, with each line's tokens grouped together.
Please note that "line" is defined with end-of-line markers.

```python
from ts_tokenizer.tokenizer import TSTokenizer
Multi_Line_Sample = """
ATATÜRK'ün GENÇLÝÐE HÝTABESÝ 
Ey Türk gençliði! Birinci vazifen, Türk istiklâlini, Türk Cumhuriyet'ini, ilelebet, muhafaza ve müdafaa etmektir. 
Mevcudiyetinin ve istikbalinin yegâne temeli budur. 
Bu temel, senin, en kýymetli hazinendir.
Ýstikbalde dahi, seni bu hazineden mahrum etmek isteyecek, dahilî ve haricî bedhahlarýn olacaktýr. 
Bir gün, istiklâl ve cumhuriyeti müdafaa mecburiyetine düþersen, vazifeye atýlmak için, içinde bulunacaðýn vaziyetin imkân ve þeraitini düþünmeyeceksin! 
Bu imkân ve þerait, çok nâmüsait bir mahiyette tezahür edebilir. 
Ýstiklâl ve cumhuriyetine kastedecek düþmanlar, bütün dünyada emsali görülmemiþ bir galibiyetin mümessili olabilirler. 
Cebren ve hile ile aziz vatanýn, bütün kaleleri zaptedilmiþ, bütün tersanelerine girilmiþ, bütün ordularý daðýtýlmýþ ve memleketin her köþesi bilfiil iþgal edilmiþ olabilir. 
Bütün bu þeraitten daha elîm ve daha vahim olmak üzere, memleketin dahilinde, iktidara sahip olanlar gaflet ve dalâlet ve hattâ hýyanet içinde bulunabilirler.
Hatta bu iktidar sahipleri þahsî menfaatlerini, müstevlilerin siyasî emelleriyle tevhit edebilirler.
Millet, fakr u zaruret içinde harap ve bîtap düþmüþ olabilir. Ey Türk istikbalinin evladý! Ýþte, bu ahval ve þerait içinde dahi, vazifen; Türk istiklâl ve cumhuriyetini kurtarmaktýr! 
Muhtaç olduðun kudret, damarlarýndaki asil kanda, mevcuttur!
"""
line_tokens = TSTokenizer.ts_tokenize(Multi_Line_Sample, output_format="lines")
if line_tokens is None:
    pass
else:
    for token in line_tokens:
        print(token)
```

**tagged_lines**: Same as lines but includes tags for each token.

```python 
tagged_line_tokens = TSTokenizer.ts_tokenize(Multi_Line_Sample, output_format="tagged_lines")
if tagged_line_tokens is None:
    pass
else:
    for token in tagged_line_tokens:
        print(token)
```


## CharFix

CharFix offers methods to correct corrupted Turkish text:

### Fix Characters

```python
from ts_tokenizer.char_fix import CharFix

line = "ParÃ§a ve bÃ¼tÃ¼n iliåÿkisi her zaman iåÿlevsel deðildir."
print(CharFix.fix(line))  # Fixes corrupted characters
```
```bash
$ Parça ve bütün ilişkisi her zaman işlevsel değildir.
```
### Lowercase

```python
from ts_tokenizer.char_fix import CharFix

line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
print(CharFix.tr_lowercase(line))
```
```bash
$ istanbul ve ığdır ''arası'' 1528 km'dir.
```
### Fix Quotes

```python
from ts_tokenizer.char_fix import CharFix

line = "İstanbul ve Iğdır ''arası'' 1528 km'dir."
print(CharFix.fix_quote(line))
```
    $ İstanbul ve Iğdır "arası" 1528 km'dir.

---
## TokenHandler

TokenHandler gets each given string and process it using methods defined under TokenPreProcess class.
This process follows a strictly defined order and it is recursive.
Each method could be called 
```python
from ts_tokenizer.token_handler import TokenPreProcess

```


### Below are the list of tags generated by tokenizer to process tokens:


| #  | Function                   | Sample                       | Used As Output | Tag                |
|----|----------------------------|------------------------------|----------------|--------------------|
| 01 | is_mention                 | @ts-tokenizer                | Yes            | Mention            |
| 02 | is_hashtag                 | #ts-tokenizer                | Yes            | Hashtag            |
| 03 | is_in_quotes               | "ts-tokenizer"               | No             | -----              |
| 04 | is_numbered_title          | (1)                          | Yes            | Numbered_Title     |
| 05 | is_in_paranthesis          | (bilgisayar)                 | No             | -----              |
| 06 | is_date_range              | 01.01.2024-01.01.2025        | Yes            | Date_Range         |
| 07 | is_complex_punc            | -yeniden,sonradan..          | No             | -----              |
| 08 | is_date                    | 22.02.2016                   | Yes            | Date               |
| 09 | is_hour                    | 14.05                        | Yes            | Hour               |
| 10 | is_percentage_numbers      | %75                          | Yes            | Percentage_Numbers |
| 11 | is_percentage_numbers_chars | %75'lik                      | Yes            | Percentage_Numbers |
| 12 | is_roman_number            | XI                           | Yes            | Roman_Number       |
| 13 | is_bullet_list             | •Giriş                       | Yes            | Bullet_List        |
| 14 | is_email                   | tanersezerr@gmail.com        | Yes            | Email              |
| 15 | is_email_punc              | tanersezerr@gmail.com.       | No             | -----              |
| 16 | is_full_url                | https://tscorpus.com         | Yes            | Full_URL           |
| 17 | is_web_url                 | www.tscorpus.com             | Yes            | Web_URL            |
| -- | is_full_url                | www.example.com'un           | Yes            | URL_Suffix         |
| 18 | is_copyright               | ©tscorpus                    | Yes            | Copyright          |
| 19 | is_registered              | tscorpus®                    | Yes            | Registered         |
| 20 | is_trademark               | tscorpus™                    | Yes            | Trademark          |
| 21 | is_currency                | 100$                         | Yes            | Currency           |
| 22 | is_num_char_sequence       | 380A                         | No             | -----              |
| 23 | is_abbr                    | TBMM                         | Yes            | Abbr               |
| 24 | is_in_lexicon              | bilgisayar                   | Yes            | Valid_Word         |
| 25 | is_in_exceptions           | e-mail                       | Yes            | Exception          |
| 26 | is_in_eng_words            | computer                     | Yes            | English_Word       |
| 27 | is_smiley                  | :)                           | Yes            | Smiley             |
| 28 | is_multiple_smiley         | :):)                         | No             | -----              |
| 29 | is_emoticon                | 🍻                           | Yes            | Emoticon           |
| 30 | is_multiple_emoticon       | 🍻🍻                         | No             | -----              |
| 31 | is_multiple_smiley_in      | hey:):)                      | No             | -----              |
| 32 | is_number                  | 175.01                       | Yes            | Number             |
| 33 | is_apostrophed             | Türkiye'nin                  | Yes            | Apostrophed        |
| 34 | is_single_punc             | !                            | Yes            | Punc               |
| 35 | is_multi_punc              | !!                           | No             | -----              |
| 36 | is_single_hyphenated       | sabah-akşam                  | Yes            | Single_Hyphenated  |
| 37 | is_multi_hyphenated        | çay-su-kahve                 | Yes            | Multi-Hyphenated   |
| 38 | is_single_underscored      | Gel_Git                      | Yes            | Single_Underscored |
| 39 | is_multi_underscored       | Yarı_Yapılandırılmış_Mülakat | Yes            | Multi_Underscored  |
| 40 | is_one_char_fixable        | bilgisa¬yar                  | Yes            | One_Char_Fixed     |
| 42 | is_three_or_more           | heyyyyy                      | No             | -----              |
| 43 | is_fsp                     | bilgisayar.                  | No             | -----              |
| 44 | is_isp                     | .bilgisayar                  | No             | -----              |
| 45 | is_fmp                     | bilgisayar..                 | No             | -----              |
| 46 | is_imp                     | ..bilgisayar                 | No             | -----              |
| 47 | is_msp                     | --bilgisayar--               | No             | -----              |
| 48 | is_mssp                    | -bilgisayar-                 | No             | -----              |
| 49 | is_midsp                   | okul,öğrenci                 | No             | -----              |
| 50 | is_midmp                   | okul,öğrenci, öğretmen       | No             | -----              |
| 51 | is_non_latin               | 한국드                          | No             | Non_Latin          |

----------------------

## Performance

ts-tokenizer is optimized for efficient tokenization and takes advantage of multi-core processing for large-scale text. By default, the script utilizes all available CPU cores minus one, ensuring your system remains responsive while processing large datasets.

### Performance Benchmarks:

The following benchmarks were conducted on different machines with the following specifications:

| **Processor**                                                            | **Cores**                 | **RAM**      | **1 Million Tokens (Multi-Core)** | **Throughput (Multi-Core)** | **1 Million Tokens (Single-Core)** | **Throughput (Single-Core)** |
|--------------------------------------------------------------------------|---------------------------|--------------|-----------------------------------|-----------------------------|------------------------------------|------------------------------|
| AMD Ryzen 7 5800H with Radeon Graphics (Laptop) <br/>3.2 GHz / 4.4 Ghz   | 8 physical cores (16 threads) | 16GB DDR4   | ~170 seconds                      | ~5,800 tokens/second        | ~715 seconds                     | ~1,400 tokens/second         |
| AMD Ryzen 9 7950X3D with Radeon Graphics (Desktop)<br/>4.2 Ghz / 5.7 Ghz | 16 physical cores (32 threads)| 96GB DDR5   | ~14 seconds                       | ~71,500 tokens/second       | ~110 seconds                    | ~9,090 tokens/second         |


