import re
import string
import unicodedata
from .data import LocalData
from .char_fix import CharFix
from .date_check import DateCheck
from .smiley_check import SmileyParser
from .emoticon_check import EmoticonParser
from .punctuation_process import PuncMatcher

puncs = re.escape(string.punctuation)
extra_puncs = ["–", "'", "°", "—"]
for p in extra_puncs:
    puncs += p

# Create a dict of RegExps
REGEX_PATTERNS = {
    "xml_tag": r'^<[^>]+?>\s*$',
    "hashtag": r'^#[^#]{1,143}$',
    "mention": r'^@[^@]{1,143}$',
    "email": r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b(?![.,!?;:])',
    "email_punc": r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[' + re.escape(string.punctuation) + r']+$',
    "Non_Prefix_URL": r'[-a-zA-Z0-9@:%._\\+~#=]{1,256}\.(?:com|net|org|edu|gov|mil)(?:\.[a-zA-Z]{2,3})?(?:/[-a-zA-Z0-9()@:%_\\+.~#?&//=]*)?\b(?![.,!?;:])',
    "prefix_url": r'(?:(?:http|https|ftp)://)?(?:www\.)?[A-Za-z0-9\-_]+(?:\.[A-Za-z0-9\-_]+)+(?:/\S*)?',
    "hour": r"\b(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9](?: ?[AP]M)?(?:'te|'de|'da|'den|'dan|'ten|'tan|'deki|'daki)?(?=$|\s)",
    "percentage_numbers_chars": r'%(\d+\D+)',
    "percentage_numbers": r'%(\d+)$',
    "in_quotes": r'"[^"]+"|\'[^\']+\'',
    "single_hyphen": r'^(?!-)[\w]+-[\w]+(?!-)$',
    "date_range": r'^[\(\[]\d{4}[\-–]\d{4}[\)\]]$',
    "in_parenthesis": r'^[\(\[\{].*[\)\]\}]$',
    "copyright": r'(?:^©[a-zA-Z]+$)|(?:^[a-zA-Z]+©$)',
    "registered": r'(?:^®[a-zA-Z]+$)|(?:^[a-zA-Z]+®$)',
    "three_or_more": r'([' + re.escape(string.punctuation) + r'])\1{2,}',
    "num_char_sequence": r'\d+[\w\s]*',
    "roman_number": r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?$',
    "currency": rf"([{LocalData.currency_symbols()}]\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?)'.format(symbols=re.escape(''.join(LocalData.currency_symbols())))",
}


def check_regex(word, pattern):
    return word if re.search(REGEX_PATTERNS[pattern], word) else None


class TokenPreProcess:

    def __init__(self):
        pass

    # Regex Based Tokens
    # These functions get the input token, checks against to regexs defined above and
    # return word, tag as tuple
    @staticmethod
    def is_xml(word: str) -> tuple:
        result = check_regex(word, "xml_tag")
        return (result, "XML_Tag") if result else None

    @staticmethod
    def is_mention(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "mention") if p_count == 1 else None
        return (result, "Mention") if result else None

    @staticmethod
    def is_hashtag(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "hashtag") if p_count == 1 else None
        return (result, "Hashtag") if result else None

    @staticmethod
    def is_num_char_sequence(word: str) -> tuple:
        result = check_regex(word, "num_char_sequence")
        return (result, "Num_Char_Sequence") if result else None

    @staticmethod
    def is_in_quotes(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "in_quotes") if p_count <= 2 else None
        return (result, "In_Quotes") if result else None

    @staticmethod
    def is_in_parenthesis(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "in_parenthesis") if p_count <= 2 else None
        return (result, "In_Parenthesis") if result else None

    @staticmethod
    def is_date_range(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "date_range") if p_count <= 1 else None
        return (result, "Date_Range") if result else None

    @staticmethod
    def is_hour(word: str) -> tuple:
        result = check_regex(word, "hour")
        return (result, "Hour") if result else None

    @staticmethod
    def is_date(word):
        result = DateCheck.is_date(word)
        return (result, "Date") if result else None

    @staticmethod
    def is_percentage_numbers(word):
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "percentage_numbers") if p_count == 1 else None
        return (result, "Percentage_Numbers") if result else None

    @staticmethod
    def is_percentage_numbers_chars(word):
        result = check_regex(word, "percentage_numbers_chars")
        return (result, "Percentage_Numbers_Chars") if result else None

    @staticmethod
    def is_roman_number(word):
        result = check_regex(word, "roman_number")
        return (result, "Roman_Number") if result else None

    @staticmethod
    def is_email_punc(word):
        result = check_regex(word, "email_punc")
        return (result, "Email_Punc") if result else None

    @staticmethod
    def is_email(word):
        result = check_regex(word, "email")
        return (result, "Email") if result else None

    @staticmethod
    def is_prefix_url(word):
        if any(dne in word for dne in LocalData.domains()):
            result = check_regex(word, "prefix_url")
            return (result, "Prefix_URL") if result else None

    @staticmethod
    def is_non_prefix_url(word):
        if any(dne in word for dne in LocalData.domains()):
            result = check_regex(word, "Non_Prefix_URL")
            return (result, "Non_Prefix_URL") if result else None

    @staticmethod
    def is_copyright(word):
        result = check_regex(word, "copyright")
        return (result, "Copyright") if result else None

    @staticmethod
    def is_registered(word):
        result = check_regex(word, "registered")
        return (result, "Registered") if result else None

    @staticmethod
    def is_currency(word):
        result = check_regex(word, "currency")
        return (result, "Currency") if result else None

    # Lexicon Based Tokens
    @staticmethod
    def is_in_lexicon(word):
        word_fixed = CharFix.fix(word)
        if CharFix.tr_lowercase(word_fixed) in LocalData.word_list():
            return word_fixed, "Lexicon"
        return None

    @staticmethod
    def is_abbr(word):
        return (word, "Abbr") if word in LocalData.abbrs() else None

    @staticmethod
    def is_in_exceptions(word):
        word_fixed = CharFix.fix(word)
        if CharFix.tr_lowercase(word_fixed) in LocalData.exception_words():
            return word_fixed, "Exception"
        return None

    @staticmethod
    def is_in_eng_words(word):
        word_fixed = CharFix.fix(word)
        if CharFix.tr_lowercase(word_fixed) in LocalData.eng_word_list():
            return word_fixed, "English_Word"
        return None

    @staticmethod
    def is_smiley(word):
        return (word, "Smiley") if word in LocalData.smileys() else None

    @staticmethod
    def is_emoticon(word):
        return (word, "Emoticon") if word in LocalData.emoticons() else None

    # Multi-Unit Tokens
    @staticmethod
    def is_multiple_smiley(word):
        if SmileyParser.consecutive_smiley(word) and not str(word[0:-1]).isalnum():
            return word, "Multiple_Smiley"
        return None

    @staticmethod
    def is_multiple_smiley_in(word):
        if SmileyParser.consecutive_smiley(word) and any(char.isalnum() for char in word):
            return word, "Multiple_Smiley_In"
        return None

    @staticmethod
    def is_multiple_emoticon(word):
        return (word, "Multiple_Emoticon") if EmoticonParser.emoticon_count(word) >= 2 else None

    @staticmethod
    def is_number(word):
        return (word, "Number") if word.isdigit() else None

    @staticmethod
    def is_punc(word):
        exception_list = ["(!)", "...", "[...]"]
        if TokenPreProcess.is_currency(word):
            return word, "Currency"
        if any(word.startswith(exc) and word.endswith(tuple(puncs)) and len(word) > len(exc) for exc in exception_list):
            return word, "FSP"
        if word in exception_list:
            return word, "Punc"
        return (word, "Punc") if all(char in puncs for char in word) else None

    @staticmethod
    def is_underscored(word):
        if "_" in word and 1 <= word.count("_") <= 1 and word[0] != "_" and word[-1] != "_":
            parts = word.split("_")
            if len(parts) == 2 and parts[0].isalpha() and parts[1].isdigit():
                return word, "Alphanumeric_Underscored"
            elif all(CharFix.tr_lowercase(part) in LocalData.word_list() for part in parts):
                return word, "Underscored"
            return word, "OOV"
        return None

    @staticmethod
    def is_three_or_more(word):
        exceptions = ["...", "!!!"]
        if word in exceptions:
            return word, "Punc"
        result = check_regex(word, "three_or_more")
        return (result, "Three_Or_More") if result else None

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
    def is_non_latin(word):
        u_word = unicodedata.normalize('NFC', word)
        allowed_chars = set("abcçdefgğhıijklmnoöprsştuüvyzwqxâîûABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZWQXÂÎ")
        sum_foreign_char = sum(1 for char in u_word if char not in allowed_chars and char not in puncs)
        sum_punc = PuncMatcher.punc_count(u_word)
        has_digit = any(char.isdigit() for char in u_word)
        hyphen_check = PuncMatcher.hyphen_in(word)
        multiple_emoticon = TokenPreProcess.is_multiple_emoticon(word)
        if sum_foreign_char >= 1 and sum_punc == 0 and not has_digit and not hyphen_check and not multiple_emoticon:
            return u_word, "Non_Latin"
        return None

    @staticmethod
    def is_one_char_fixable(word):
        extra_chars = ["¬", "¬"]
        for extra in extra_chars:
            if PuncMatcher.punc_pos(extra) != [0] or PuncMatcher.punc_pos(word) != [-1]:
                fixed_word = word.replace(extra, "")
                if TokenPreProcess.is_in_lexicon(fixed_word):
                    return fixed_word, "One_Char_Fixed"
        return None
