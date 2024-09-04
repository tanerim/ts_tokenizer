import re
import string
import inspect
from .data import LocalData
from .char_fix import CharFix
from .date_check import DateCheck
from .smiley_check import SmileyParser
from .emoticon_check import EmoticonParser
from .punctuation_process import PuncMatcher


# Create a dict of RegExps
REGEX_PATTERNS = {
    "hashtag": r'^#[^#]{1,143}$',
    "mention": r'^@[^@]{1,143}$',
    "email": r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b(?![.,!?;:])',
    # "email": r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "email_punc": r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[' + re.escape(string.punctuation) + r']+$',
    # "Non_Prefix_URL": r'[-a-zA-Z0-9@:%._\\+~#=]{1,256}\.(?:com|net|org|edu|gov|mil)(?:\.[a-zA-Z]{2,3})?(?:/[-a-zA-Z0-9()@:%_\\+.~#?&//=]*)?+\b(?![.,!?;:])',
    "Non_Prefix_URL": r'[-a-zA-Z0-9@:%._\\+~#=]{1,256}\.(?:com|net|org|edu|gov|mil)(?:\.[a-zA-Z]{2,3})?(?:/[-a-zA-Z0-9()@:%_\\+.~#?&//=]*)?\b(?![.,!?;:])',
    "prefix_url": r'(?:(?:http|https|ftp)://)?(?:www\.)?[A-Za-z0-9\-_]+(?:\.[A-Za-z0-9\-_]+)+(?:/\S*)?',
    "hour": r"\b(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9](?: ?[AP]M)?(?:'te|'de|'da|'den|'dan|'ten|'tan|'deki|'daki)?(?=$|\s)",
    "percentage_numbers_chars": r'%(\d+\D+)',
    "percentage_numbers": r'%(\d+)$',
    "in_quotes": r'"[^"]+"|\'[^\']+\'',
    "date_range": r'^[\(\[]\d{4}[\-–]\d{4}[\)\]]$',
    "in_parenthesis": r'^[\(\[\{].*[\)\]\}]$',
    "copyright": r'(?:^©[a-zA-Z]+$)|(?:^[a-zA-Z]+©$)',
    "registered": r'(?:^®[a-zA-Z]+$)|(?:^[a-zA-Z]+®$)',
    "three_or_more": r'([' + re.escape(string.punctuation) + r'])\1{2,}',
    "num_char_sequence": r'\d+[\w\s]*',
    "roman_number": r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?$',
    "currency_initial": r'^(?P<Currency>[$€£₺]\d+(?:,\d{3})*(?:\.\d{2})?)$',
    "currency_final": r'^(?P<Currency>\d+(?:,\d{3})*(?:\.\d{2})?[$€£₺])$'
}


def check_regex(word, pattern_key):
    pattern = REGEX_PATTERNS[pattern_key]
    if pattern:
        return word if re.match(pattern, word) else None
    else:
        return None


class TokenPreProcess:

    @staticmethod
    def is_in_lexicon(word):
        word = CharFix.fix(word)
        return word if TokenPreProcess.fix_tr_lowercase(word) in LocalData.word_list() else None

    @staticmethod
    def is_in_exceptions(word):
        word = CharFix.fix(word)
        return word if TokenPreProcess.fix_tr_lowercase(word) in LocalData.exception_words() else None

    @staticmethod
    def is_in_eng_words(word):
        word = CharFix.fix(word)
        return word if TokenPreProcess.fix_tr_lowercase(word) in LocalData.eng_word_list() else None

    @staticmethod
    def fix_tr_lowercase(word):
        conversion = {'I': 'ı', 'İ': 'i'}
        for key, value in conversion.items():
            word = word.replace(key, value)
        return word.lower()

    @staticmethod
    def is_smiley(word):
        return word if word in LocalData.smileys() else None

    @staticmethod
    def is_multiple_smiley(word):
        if SmileyParser.consecutive_smiley(word) is True:
            if not str(word[0]).isalpha() and not str(word[1]).isalpha():
                if SmileyParser.smiley_count(word) >= 2:
                    return word

    @staticmethod
    def is_emoticon(word):
        return word if word in LocalData.emoticons() else None

    @staticmethod
    def is_multiple_emoticon(word):
        if EmoticonParser.emoticon_count(word) >= 2:
            return word

    @staticmethod
    def is_abbr(word):
        return word if word in LocalData.abbrs() else None

    @staticmethod
    def is_number(word):
        return word if word.isdigit() else None

    @staticmethod
    def is_punc(word):
        exception_list = ["(!)", "...", "[...]"]
        # Check for Full-Side Punctuation (FSP) cases
        if any(word.startswith(exc) and word.endswith(tuple(string.punctuation)) and len(word) > len(exc) for exc in
               exception_list):
            return "FSP"
        # Check for standalone exception (like (!)) returning "Punc"
        elif word in exception_list:
            return "Punc"
        # Otherwise, check if all characters are punctuation
        return word if all(char in string.punctuation for char in word) else None

    @staticmethod
    def is_mention(word):
        p_count = PuncMatcher.punc_count(word)
        if p_count == 1:
            return check_regex(word, "mention")

    @staticmethod
    def is_hashtag(word):
        p_count = PuncMatcher.punc_count(word)
        if p_count == 1:
            return check_regex(word, "hashtag")

    @staticmethod
    def is_num_char_sequence(word):
        return check_regex(word, "num_char_sequence")

    @staticmethod
    def is_in_quotes(word):
        p_count = PuncMatcher.punc_count(word)
        if p_count <= 2:
            return check_regex(word, "in_quotes")

    @staticmethod
    def is_date_range(word):
        p_count = PuncMatcher.punc_count(word)
        if p_count <= 2:
            return check_regex(word, "date_range")

    @staticmethod
    def is_in_parenthesis(word):
        p_count = PuncMatcher.punc_count(word)
        if p_count <= 2:
            return check_regex(word, "in_parenthesis")

    @staticmethod
    def is_hour(word):
        return check_regex(word, "hour")

    @staticmethod
    def is_date(word):
        return DateCheck.is_date(word)

    @staticmethod
    def is_percentage_numbers(word):
        p_count = PuncMatcher.punc_count(word)
        if p_count == 1:
            return check_regex(word, "percentage_numbers")

    @staticmethod
    def is_percentage_numbers_chars(word):
        return check_regex(word, "percentage_numbers_chars")

    @staticmethod
    def is_roman_number(word):
        return check_regex(word, "roman_number")

    @staticmethod
    def is_email_punc(word):
        return check_regex(word, "email_punc")

    @staticmethod
    def is_email(word):
        return check_regex(word, "email")

    @staticmethod
    def is_prefix_url(word):
        if any(dne in word for dne in LocalData.domains()):
            return check_regex(word, "prefix_url")

    @staticmethod
    def is_non_prefix_url(word):
        if any(dne in word for dne in LocalData.domains()):
            return check_regex(word, "Non_Prefix_URL")

    @staticmethod
    def is_copyright(word):
        return check_regex(word, "copyright")

    @staticmethod
    def is_registered(word):
        return check_regex(word, "registered")

    @staticmethod
    def is_hyphenated(word):
        if ("-" in word and word.count("-") == 1 and word[0] != "-" and word[-1] != "-"
                and not any(c in string.punctuation for c in word if c != "-")):
            parts = word.split("-")
            if TokenPreProcess.fix_tr_lowercase(parts[0]) in LocalData.word_list() and TokenPreProcess.fix_tr_lowercase(parts[1]) in LocalData.word_list():
                return word

    @staticmethod
    def is_mishpyhenated(word):
        izafe = ["ı", "i", "ü", "u"]
        if ("-" in word and word.count("-") == 1 and word[0] != "-" and word[-1] != "-"
                and not any(c in string.punctuation for c in word if c != "-")):
            parts = word.split("-")
            if TokenPreProcess.fix_tr_lowercase(parts[0]) not in LocalData.word_list() and TokenPreProcess.fix_tr_lowercase(parts[1]) not in LocalData.word_list() and TokenPreProcess.fix_tr_lowercase(parts[1]) not in izafe:
                return word

    @staticmethod
    def is_underscored(word):
        if "_" in word and word.count("_") == 1 and word[0] != "_" and word[-1] != "_":
            parts = word.split("_")
            if TokenPreProcess.fix_tr_lowercase(parts[0]) in LocalData.word_list() and TokenPreProcess.fix_tr_lowercase(parts[1]) in LocalData.word_list():
                return word

    @staticmethod
    def is_hyphen_in(word):
        if "-" in word and word.count("-") <= 5 and word[0] != "-" and word[-1] != "-":
            if sum(char.isdigit() for char in word) <= 1:
                if TokenPreProcess.is_hyphenated(word) is True:
                    return word, CharFix.fix(word), "Hyphenated"
                else:
                    return word, CharFix.fix(word), "OOV"
        elif "_" in word and word[0] != "_" and word[-1] != "_":
            if TokenPreProcess.is_underscored(word) is True:
                return word, CharFix.fix(word), "Underscored"
            else:
                return word, CharFix.fix(word), "OOV"

    @staticmethod
    def is_formula(word):
        # Check for numbers and letters
        if any(c.isdigit() for c in word) and any(c.isalpha() for c in word):
            has_numbers_and_letters = True
        else:
            has_numbers_and_letters = False
        # Check for multiple mathematical operators
        math_operators = ['+', '-', '*', '/', '%', '^']
        operator_count = sum(word.count(op) for op in math_operators)
        has_multiple_operators = operator_count >= 2
        if has_numbers_and_letters and has_multiple_operators:
            return word

    @staticmethod
    def is_three_or_more(word):
        exceptions = ["...", "!!!"]
        if word in exceptions:
            return word, "Punc"
        else:
            return check_regex(word, "three_or_more")

    @staticmethod
    def is_inner_char(word):
        pattern = r'\([a-zA-ZğüşıöçĞÜŞİÖÇ]\)'
        if "(" in word and ")" in word:
            if re.search(pattern, word):
                candidate = re.split(pattern, word)
                candidate = "".join(candidate)
                if candidate in LocalData.word_list():
                    return word, "Inner_Char"
        return None

    @staticmethod
    def is_currency_initial(word):
        return check_regex(word, "currency_initial")

    @staticmethod
    def is_currency_final(word):
        return check_regex(word, "currency_final")


class TokenProcessor:

    @staticmethod
    def run_all(word):
        results = {}
        for method_name in dir(TokenPreProcess):
            method = getattr(TokenPreProcess, method_name)
            # Skip special methods and built-in types
            if callable(method) and not method_name.startswith('__'):
                try:
                    # Check if the method requires one argument
                    if len(inspect.signature(method).parameters) == 1:
                        result = method(word)
                        if result:
                            results[method_name] = result
                except ValueError:
                    # Skip methods that don't have signatures (like built-ins)
                    continue
        return results if results else None
