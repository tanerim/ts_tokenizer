
**TS Tokenizer** is a foundational lexical processing engine for Turkish Natural Language Processing. It is a hybrid tokenizer designed specifically for tokenizing Turkish texts.
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

To force upgrade:
```bash
pip install --upgrade --no-cache-dir --force-reinstall ts-tokenizer
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

# Python API

For simple Python usage, import `tokenize` from the package root:

```python
from ts_tokenizer import tokenize

text = "Merhaba dünya. Bugün 16.08.2026."
result = tokenize(text, "tokenized")

print(result)
```

Output:

```text
Merhaba
dünya
.
Bugün
16.08.2026
.
```

Supported `return_format` values:

- `tokenized`: returns a newline-delimited `str` of tokens.
- `tagged`: returns a newline-delimited `str` of `token<TAB>tag` pairs.
- `lines`: returns a single `str` containing one tokenized line.
- `tagged_lines`: returns a Python list of `(token, tag)` tuples.

Tagged example:

```python
from ts_tokenizer import tokenize

text = "Merhaba dünya."
result = tokenize(text, "tagged")

print(result)
```

Output:

```text
Merhaba	Valid_Word
dünya	Valid_Word
.	Punc
```

Line-preserving examples:

```python
from ts_tokenizer import tokenize

text = "Merhaba dünya."
print(tokenize(text, "lines"))
print(tokenize(text, "tagged_lines"))
```

Output:

```text
Merhaba dünya .
[('Merhaba', 'Valid_Word'), ('dünya', 'Valid_Word'), ('.', 'Punc')]
```

## TSTokenizer

`TSTokenizer.ts_tokenize(...)` is intended for CLI-style workflows. It writes results to standard output and does not return token data to the caller.

```python
from ts_tokenizer import TSTokenizer

TSTokenizer.ts_tokenize(
    input_file="Merhaba dünya.\nİkinci satır.",
    output_format="tokenized",
)
```

Use `tokenize(...)` when you want a value back inside Python code.
```

**tagged_lines**: Same as lines but includes tags for each token.

```python 
from ts_tokenizer import tokenize
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
Millet, fakruzaruret içinde harap ve bîtap düþmüþ olabilir. Ey Türk istikbalinin evladý! Ýþte, bu ahval ve þerait içinde dahi, vazifen; Türk istiklâl ve cumhuriyetini kurtarmaktýr! 
Muhtaç olduðun kudret, damarlarýndaki asil kanda, mevcuttur!
"""
tagged_lines = tokenize(Multi_Line_Sample, "tagged_lines")
print(tagged_lines)
```
Generated output is as follows:
```bash
[("ATATÜRK'ün", 'Apostrophed'), ('GENÇLİĞE', 'Valid_Word'), ('HİTABESİ', 'Valid_Word')]
[('Ey', 'Valid_Word'), ('Türk', 'Valid_Word'), ('gençliği', 'Valid_Word'), ('!', 'Punc'), ('Birinci', 'Valid_Word'), ('vazifen', 'Valid_Word'), (',', 'Punc'), ('Türk', 'Valid_Word'), ('istiklâlini', 'Valid_Word'), (',', 'Punc'), ('Türk', 'Valid_Word'), ("Cumhuriyet'ini", 'Apostrophed'), (',', 'Punc'), ('ilelebet', 'Valid_Word'), (',', 'Punc'), ('muhafaza', 'Valid_Word'), ('ve', 'Valid_Word'), ('müdafaa', 'Valid_Word'), ('etmektir', 'Valid_Word'), ('.', 'Punc')]
[('Mevcudiyetinin', 'Valid_Word'), ('ve', 'Valid_Word'), ('istikbalinin', 'Valid_Word'), ('yegâne', 'Valid_Word'), ('temeli', 'Valid_Word'), ('budur', 'Valid_Word'), ('.', 'Punc')]
[('Bu', 'Valid_Word'), ('temel', 'Valid_Word'), (',', 'Punc'), ('senin', 'Valid_Word'), (',', 'Punc'), ('en', 'Valid_Word'), ('kıymetli', 'Valid_Word'), ('hazinendir', 'Valid_Word'), ('.', 'Punc')]
[('İstikbalde', 'Valid_Word'), ('dahi', 'Valid_Word'), (',', 'Punc'), ('seni', 'Valid_Word'), ('bu', 'Valid_Word'), ('hazineden', 'Valid_Word'), ('mahrum', 'Valid_Word'), ('etmek', 'Valid_Word'), ('isteyecek', 'Valid_Word'), (',', 'Punc'), ('dahilî', 'Valid_Word'), ('ve', 'Valid_Word'), ('haricî', 'Valid_Word'), ('bedhahların', 'Valid_Word'), ('olacaktır', 'Valid_Word'), ('.', 'Punc')]
[('Bir', 'Valid_Word'), ('gün', 'Valid_Word'), (',', 'Punc'), ('istiklâl', 'Valid_Word'), ('ve', 'Valid_Word'), ('cumhuriyeti', 'Valid_Word'), ('müdafaa', 'Valid_Word'), ('mecburiyetine', 'Valid_Word'), ('düşersen', 'Valid_Word'), (',', 'Punc'), ('vazifeye', 'Valid_Word'), ('atılmak', 'Valid_Word'), ('için', 'Valid_Word'), (',', 'Punc'), ('içinde', 'Valid_Word'), ('bulunacağın', 'Valid_Word'), ('vaziyetin', 'Valid_Word'), ('imkân', 'Valid_Word'), ('ve', 'Valid_Word'), ('şeraitini', 'Valid_Word'), ('düşünmeyeceksin', 'Valid_Word'), ('!', 'Punc')]
[('Bu', 'Valid_Word'), ('imkân', 'Valid_Word'), ('ve', 'Valid_Word'), ('şerait', 'Valid_Word'), (',', 'Punc'), ('çok', 'Valid_Word'), ('nâmüsait', 'Valid_Word'), ('bir', 'Valid_Word'), ('mahiyette', 'Valid_Word'), ('tezahür', 'Valid_Word'), ('edebilir', 'Valid_Word'), ('.', 'Punc')]
[('İstiklâl', 'Valid_Word'), ('ve', 'Valid_Word'), ('cumhuriyetine', 'Valid_Word'), ('kastedecek', 'Valid_Word'), ('düşmanlar', 'Valid_Word'), (',', 'Punc'), ('bütün', 'Valid_Word'), ('dünyada', 'Valid_Word'), ('emsali', 'Valid_Word'), ('görülmemiş', 'Valid_Word'), ('bir', 'Valid_Word'), ('galibiyetin', 'Valid_Word'), ('mümessili', 'Valid_Word'), ('olabilirler', 'Valid_Word'), ('.', 'Punc')]
[('Cebren', 'Valid_Word'), ('ve', 'Valid_Word'), ('hile', 'Valid_Word'), ('ile', 'Valid_Word'), ('aziz', 'Valid_Word'), ('vatanın', 'Valid_Word'), (',', 'Punc'), ('bütün', 'Valid_Word'), ('kaleleri', 'Valid_Word'), ('zaptedilmiş', 'OOV'), (',', 'Punc'), ('bütün', 'Valid_Word'), ('tersanelerine', 'Valid_Word'), ('girilmiş', 'Valid_Word'), (',', 'Punc'), ('bütün', 'Valid_Word'), ('orduları', 'Valid_Word'), ('dağıtılmış', 'Valid_Word'), ('ve', 'Valid_Word'), ('memleketin', 'Valid_Word'), ('her', 'Valid_Word'), ('köşesi', 'Valid_Word'), ('bilfiil', 'Valid_Word'), ('işgal', 'Valid_Word'), ('edilmiş', 'Valid_Word'), ('olabilir', 'Valid_Word'), ('.', 'Punc')]
[('Bütün', 'Valid_Word'), ('bu', 'Valid_Word'), ('şeraitten', 'Valid_Word'), ('daha', 'Valid_Word'), ('elîm', 'Valid_Word'), ('ve', 'Valid_Word'), ('daha', 'Valid_Word'), ('vahim', 'Valid_Word'), ('olmak', 'Valid_Word'), ('üzere', 'Valid_Word'), (',', 'Punc'), ('memleketin', 'Valid_Word'), ('dahilinde', 'Valid_Word'), (',', 'Punc'), ('iktidara', 'Valid_Word'), ('sahip', 'Valid_Word'), ('olanlar', 'Valid_Word'), ('gaflet', 'Valid_Word'), ('ve', 'Valid_Word'), ('dalâlet', 'Valid_Word'), ('ve', 'Valid_Word'), ('hattâ', 'Valid_Word'), ('hıyanet', 'Valid_Word'), ('içinde', 'Valid_Word'), ('bulunabilirler', 'Valid_Word'), ('.', 'Punc')]
[('Hatta', 'Valid_Word'), ('bu', 'Valid_Word'), ('iktidar', 'Valid_Word'), ('sahipleri', 'Valid_Word'), ('şahsî', 'Valid_Word'), ('menfaatlerini', 'Valid_Word'), (',', 'Punc'), ('müstevlilerin', 'Valid_Word'), ('siyasî', 'Valid_Word'), ('emelleriyle', 'Valid_Word'), ('tevhit', 'Valid_Word'), ('edebilirler', 'Valid_Word'), ('.', 'Punc')]
[('Millet', 'Valid_Word'), (',', 'Punc'), ('fakruzaruret', 'Valid_Word'), ('içinde', 'Valid_Word'), ('harap', 'Valid_Word'), ('ve', 'Valid_Word'), ('bîtap', 'Valid_Word'), ('düşmüş', 'Valid_Word'), ('olabilir', 'Valid_Word'), ('.', 'Punc'), ('Ey', 'Valid_Word'), ('Türk', 'Valid_Word'), ('istikbalinin', 'Valid_Word'), ('evladı', 'Valid_Word'), ('!', 'Punc'), ('İşte', 'Valid_Word'), (',', 'Punc'), ('bu', 'Valid_Word'), ('ahval', 'Valid_Word'), ('ve', 'Valid_Word'), ('şerait', 'Valid_Word'), ('içinde', 'Valid_Word'), ('dahi', 'Valid_Word'), (',', 'Punc'), ('vazifen', 'Valid_Word'), (';', 'Punc'), ('Türk', 'Valid_Word'), ('istiklâl', 'Valid_Word'), ('ve', 'Valid_Word'), ('cumhuriyetini', 'Valid_Word'), ('kurtarmaktır', 'Valid_Word'), ('!', 'Punc')]
[('Muhtaç', 'Valid_Word'), ('olduğun', 'Valid_Word'), ('kudret', 'Valid_Word'), (',', 'Punc'), ('damarlarındaki', 'Valid_Word'), ('asil', 'Valid_Word'), ('kanda', 'Valid_Word'), (',', 'Punc'), ('mevcuttur', 'Valid_Word'), ('!', 'Punc')]
```

## CharFix

CharFix offers methods to correct corrupted Turkish text:

You can use these helpers either through `CharFix` or as direct package-level functions:

```python
from ts_tokenizer import fix, tr_lowercase, fix_quote
```

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

---
## Local Data

Bundled lexical resources can also be accessed directly from the package.

Generic accessor:

```python
from ts_tokenizer import get_data

smileys = get_data("smileys")
print(":)" in smileys)
```

Named helpers:

```python
from ts_tokenizer import smileys_data, word_list_data

print(":)" in smileys_data())
print("istanbul" in word_list_data())
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

Returned values are `frozenset[str]`, so they are safe to inspect without mutating the tokenizer's in-memory resources.

---
## TokenHandler

TokenHandler gets each given string and process it using methods defined under TokenPreProcess class.
This process follows a strictly defined order and it is recursive.
Each method could be called 
```python
from ts_tokenizer import TokenPreProcess

```


### Below are the list of tags generated by tokenizer to process tokens:


| #  | Function                   | Sample                       | Used As Output | Tag                |
|----|----------------------------|------------------------------|----------------|--------------------|
| 01 | is_mention                 | @ts-tokenizer                | Yes            | Mention            |
| 02 | is_hashtag                 | #ts-tokenizer                | Yes            | Hashtag            |
| -- | is_mention_suffix          | @SerkanÇayoğlu'ndan          | Yes            | Mention_Suffix     |
| -- | is_hashtag_suffix          | #Şanlıurfa'da                | Yes            | Hashtag_Suffix     |
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
| 18 | is_full_url                | www.example.com'un           | Yes            | URL_Suffix         |
| 19 | is_formula                 | F(2,37)=6.42                 | Yes            | Formula            |
| 20 | is_copyright               | ©tscorpus                    | Yes            | Copyright          |
| 21 | is_registered              | tscorpus®                    | Yes            | Registered         |
| 22 | is_trademark               | tscorpus™                    | Yes            | Trademark          |
| 23 | is_currency                | 100$                         | Yes            | Currency           |
| 24 | is_num_char_sequence       | 380A                         | No             | -----              |
| 25 | is_abbr                    | TBMM                         | Yes            | Abbr               |
| 26 | is_in_lexicon              | bilgisayar                   | Yes            | Valid_Word         |
| 27 | is_in_exceptions           | e-mail                       | Yes            | Exception          |
| 28 | is_in_eng_words            | computer                     | Yes            | English_Word       |
| 29 | is_smiley                  | :)                           | Yes            | Smiley             |
| 30 | is_multiple_smiley         | :):)                         | No             | -----              |
| 31 | is_emoticon                | 🍻                           | Yes            | Emoticon           |
| 32 | is_multiple_emoticon       | 🍻🍻                         | No             | -----              |
| 33 | is_multiple_smiley_in      | hey:):)                      | No             | -----              |
| 34 | is_number                  | 175.01                       | Yes            | Number             |
| 35 | is_apostrophed             | Türkiye'nin                  | Yes            | Apostrophed        |
| 36 | is_single_punc             | !                            | Yes            | Punc               |
| 37 | is_multi_punc              | !!                           | No             | -----              |
| 38 | is_single_hyphenated       | sabah-akşam                  | Yes            | Single_Hyphenated  |
| 39 | is_multi_hyphenated        | çay-su-kahve                 | Yes            | Multi-Hyphenated   |
| 40 | is_single_underscored      | Gel_Git                      | Yes            | Single_Underscored |
| 41 | is_multi_underscored       | Yarı_Yapılandırılmış_Mülakat | Yes            | Multi_Underscored  |
| 42 | is_one_char_fixable        | bilgisa¬yar                  | Yes            | One_Char_Fixed     |
| 43 | is_three_or_more           | heyyyyy                      | No             | -----              |
| 44 | is_fsp                     | bilgisayar.                  | No             | -----              |
| 45 | is_isp                     | .bilgisayar                  | No             | -----              |
| 46 | is_fmp                     | bilgisayar..                 | No             | -----              |
| 47 | is_imp                     | ..bilgisayar                 | No             | -----              |
| 48 | is_msp                     | --bilgisayar--               | No             | -----              |
| 49 | is_mssp                    | -bilgisayar-                 | No             | -----              |
| 50 | is_midsp                   | okul,öğrenci                 | No             | -----              |
| 51 | is_midmp                   | okul,öğrenci, öğretmen       | No             | -----              |
| 52 | is_non_latin               | 한국드                          | No             | Non_Latin          |

----------------------

## Performance

ts-tokenizer is optimized for efficient tokenization and takes advantage of multi-core processing for large-scale text. By default, the script utilizes all available CPU cores minus one, ensuring your system remains responsive while processing large datasets.

### Performance Benchmarks:

The following benchmarks were conducted on different machines with the following specifications:

| **Processor**                                                            | **Cores**                 | **RAM**      | **1 Million Tokens (Multi-Core)** | **Throughput (Multi-Core)** | **1 Million Tokens (Single-Core)** | **Throughput (Single-Core)** |
|--------------------------------------------------------------------------|---------------------------|--------------|-----------------------------------|-----------------------------|------------------------------------|------------------------------|
| AMD Ryzen 7 5800H with Radeon Graphics (Laptop) <br/>3.2 GHz / 4.4 Ghz   | 8 physical cores (16 threads) | 16GB DDR4   | ~170 seconds                      | ~5,800 tokens/second        | ~715 seconds                     | ~1,400 tokens/second         |
| AMD Ryzen 9 7950X3D with Radeon Graphics (Desktop)<br/>4.2 Ghz / 5.7 Ghz | 16 physical cores (32 threads)| 96GB DDR5   | ~14 seconds                       | ~71,500 tokens/second       | ~110 seconds                    | ~9,090 tokens/second         |
