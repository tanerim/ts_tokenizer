import re
import string
import sys
from ts_tokenizer.data import LocalData
from ts_tokenizer.char_fix import CharFix
from ts_tokenizer.token_handler import TokenProcessor

puncs = re.escape(string.punctuation)
extra_puncs = ["–", "°", "—", "…"]
puncs += re.escape(''.join(extra_puncs))
domains_pattern = '|'.join([re.escape(domain[1:]) for domain in LocalData.domains()])

REGEX_PATTERNS = {
    "hashtag": re.compile(r'^#[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9__\uFE0F]{1,139}$'),
    "mention": re.compile(r'^@[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9__\uFE0F]{1,15}$'),
    # "email": re.compile(rf'^[^{puncs}][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b(?![.,!?;:])'),
    "email": re.compile(rf'^[^{puncs}][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+(?<![{puncs}])$'),
    "email_punc": re.compile(r'\b[' + re.escape(string.punctuation) + r']*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[' + re.escape(string.punctuation) + r']*\b'),
    "hour": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9]$"),
    "hour_suffix": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9](?:'te|'de|'da|'den|'dan|'ten|'tan|'deki|'daki)$"),
    "hour_12": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9]([AP]M)$"),
    "percentage_numbers_initial": re.compile(r'^%\d{1,3}(?:[.,]\d+)?$'),
    "percentage_numbers_final": re.compile(r'^\d{1,3}(?:[.,]\d+)*%$'),
    "percentage_numbers_chars": re.compile(r'^%\d{1,3}(?:[.,]\d+)*\D.*$'),
    "single_hyphen": re.compile(r'^(?!-)\w+-\w+(?!-)$'),
    "multi_hyphen": re.compile(r'^(?!-)(\w+-)+\w+(?!-)$'),
    "date_range": re.compile(r'^\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}$'),
    "year_range": re.compile(r'^\d{4}-\d{4}$'),
    "in_parenthesis": re.compile(r'^[(\[{]{1,}[^()\[\]{}]*[)\]}]{1,}$'),
    "numbered_title": re.compile(r'^\((\d{1,2})\)$|^\[(\d{1,2})\]$|^{(\d{1,2})}$'),
    "in_quotes": re.compile(r'^[\'"][^\'"]*[\'"]$'),
    "copyright": re.compile(r'(^©[a-zA-Z0-9]+$)|(^[a-zA-Z0-9]+©$)'),
    "registered": re.compile(r'(^®[a-zA-Z]+$)|(^[a-zA-Z]+®$)'),
    "trade_mark": re.compile(r'(^™[a-zA-Z]+$)|(^[a-zA-Z]+™$)'),
    "bullet_list": re.compile(r'^•[a-zA-Z]+$'),
    "three_or_more": re.compile(r'^([{}])\1{{2,}}$'.format(re.escape(string.punctuation))),
    "roman_number": re.compile(r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?$'),
    "apostrophed": re.compile(r"^([a-zA-ZıiİüÜçÇöÖşŞğĞ]+)'([a-zA-ZıiİüÜçÇöÖşŞğĞ]+)$"),
    "currency": re.compile(rf"^(?:[{re.escape(''.join(LocalData.currency_symbols()))}]\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?|\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?[{re.escape(''.join(LocalData.currency_symbols()))}])$"),
    "url_pattern": re.compile(r'^((http|https)\:\/\/)[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z0-9\&\/\?\:@\-_=#])+'),
    "url": re.compile(r'^((www)\.)[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z0-9\&\/\?\:@\-_=#])+'),
    "num_char_sequence": re.compile(r'\d+[\w\s]*'),
}

def check_regex(word, pattern):
    return word if REGEX_PATTERNS[pattern].search(CharFix.fix(word)) else None

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(">"):
                    continue

                # Split the line into words and check each word
                words = line.split()
                for word in words:
                    match= check_regex(word, "multi_hyphen")
                    if match:
                        print(CharFix.fix(word))
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        sys.exit(1)

if __name__ == "__main__":
    main()

