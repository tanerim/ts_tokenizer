import re
import string
import unicodedata
import ipaddress

from .data import LocalData
from .char_fix import CharFix
from .date_check import DateCheck
from .smiley_check import SmileyParser
from .emoticon_check import EmoticonParser
from .punctuation_process import PuncMatcher

puncs = re.escape(string.punctuation)
extra_puncs = ["–", "°", "—"]
puncs += re.escape(''.join(extra_puncs))
domains_pattern = '|'.join([re.escape(domain[1:]) for domain in LocalData.domains()])
# Create a dict of RegExps
# noinspection RegExpRedundantEscape
REGEX_PATTERNS = {
    "hashtag": re.compile(r'^#[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\-\uFE0F]{1,139}$'),
    "mention": re.compile(r'^@[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\-\uFE0F]{1,15}$'),
    "hashtag_suffix": re.compile(r"^#[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\-\uFE0F]{1,139}'[a-zA-ZıiİüÜçÇöÖşŞğĞ]+$"),
    "mention_suffix": re.compile(r"^@[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\-\uFE0F]{1,15}'[a-zA-ZıiİüÜçÇöÖşŞğĞ]+$"),
    "numeric_hyphenated_suffix": re.compile(r"^(?=.*\d)[A-Za-zÇĞİÖŞÜçğıöşü0-9]+(?:-[A-Za-zÇĞİÖŞÜçğıöşü0-9]+)+'[A-Za-zÇĞİÖŞÜçğıöşü]+$"),
    "email": re.compile(rf'^[^{puncs}][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+(?<![{puncs}])$'),
    "email_punc": re.compile(r'\b[' + re.escape(string.punctuation) + r']*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[' + re.escape(string.punctuation) + r']*\b'),
    "hour": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9]$"),
    "hour_suffix": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9](?:'te|'de|'da|'den|'dan|'ten|'tan|'deki|'daki)$"),
    "number_suffix": re.compile(r"^\d+(?:[.,]\d+)*'[a-zA-ZıiİüÜçÇöÖşŞğĞ]+$"),
    "currency_suffix": re.compile(rf"^(?:[{re.escape(''.join(LocalData.currency_symbols()))}]\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?|\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?[{re.escape(''.join(LocalData.currency_symbols()))}])'[a-zA-ZıiİüÜçÇöÖşŞğĞ]+$"),
    #"hour_12": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9]([AP]M)$"),
    "hour_12": re.compile(r"^(0[1-9]|1[0-2])[:.][0-5][0-9](AM|PM)$"),
    "percentage_numbers_initial": re.compile(r'^%\d{1,3}(?:[.,]\d+)?$'),
    "percentage_numbers_final": re.compile(r'^\d{1,3}(?:[.,]\d+)*%$'),
    "percentage_numbers_chars": re.compile(r'^%\d{1,3}(?:[.,]\d+)*\D.*$'),
    "single_hyphen": re.compile(rf'^[^{puncs}]+-[^{puncs}]+$'),
    "multi_hyphen": re.compile(rf'^[^{puncs}]+(-[^{puncs}]+)+$'),
    "single_underscore": re.compile(rf'^[^{puncs}]+_[^{puncs}]+$'),
    "multi_underscore": re.compile(rf'^[^{puncs}]+(_[^{puncs}]+)+$'),
    "date_range": re.compile(r'^(?:(?:0[1-9]|[1-2][0-9]|3[0-1])\.(?:0[1-9]|1[0-2])\.\d{4})-(?:(?:0[1-9]|[1-2][0-9]|3[0-1])\.(?:0[1-9]|1[0-2])\.\d{4})$'),
    "year_range": re.compile(r'^(?:[1-9]\d{3})-(?:[1-9]\d{3})$'),
    "date_range_suffix": re.compile(r"^(?:(?:0[1-9]|[1-2][0-9]|3[0-1])\.(?:0[1-9]|1[0-2])\.\d{4})-(?:(?:0[1-9]|[1-2][0-9]|3[0-1])\.(?:0[1-9]|1[0-2])\.\d{4})'[a-zA-ZıiİüÜçÇöÖşŞğĞ]+$"),
    "in_parenthesis": re.compile(r'^[(\[{]+[^()\[\]{}]*[)\]}]+}$'),
    "numbered_title": re.compile(r'^\((\d{1,2})\)|^\[(\d{1,2})\]|^{(\d{1,2})\}'),
    "in_quotes": re.compile(r'^[\'"][^\'"]*[\'"]$'),
    "copyright": re.compile(r'(^©[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_-]+$)|(^[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_-]+©$)'),
    "registered": re.compile(r'(^®[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_-]+$)|(^[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_-]+®$)'),
    "trade_mark": re.compile(r'(^™[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_-]+$)|(^[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_-]+™$)'),
    "bullet_list": re.compile(r'^•[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9]+$'),
    "three_or_more": re.compile(r'^([{}])\1{{2,}}$'.format(re.escape(string.punctuation))),
    "roman_number": re.compile(r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?$'),
    "apostrophed": re.compile(r"^([a-zA-ZıiİüÜçÇöÖşŞğĞ]+)'([a-zA-ZıiİüÜçÇöÖşŞğĞ]+)$"),
    "currency": re.compile(rf"^(?:[{re.escape(''.join(LocalData.currency_symbols()))}]\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?|\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?[{re.escape(''.join(LocalData.currency_symbols()))}])$"),
    "full_url": re.compile(r'^((http|https)\:\/\/)[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F\.\/\?\:@\-=#]+\.([a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F\&\/\?\:@\-=#])+'),
    "web_url": re.compile(r'^((www)\.)[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F\.\/\?\:@\-=#]+\.([a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F\&\/\?\:@\-=#])+',re.IGNORECASE),
    "num_char_sequence": re.compile(r'\d+[\w\s]*'),
}

exception_list = ["(!)", "..."]

MATH_OPERATORS = {'+', '-', '*', '/', '%', '^', '**', '=', '!=', '==', '>', '<', '>=', '<=', '+=', '-=', '*=', '/=',
                  '%=', '√', '∑', 'π', '∞', '∩', '∪', '⊆', '⊂', '∈', '∉', '∧', '∨', '¬', '|', '!'}

FORMULA_OPERATORS = ("≤", "≥", "<", ">", "=")
FORMULA_TERM_RE = re.compile(r"^-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?$|^-?\.\d+$|^[A-Za-zΑ-Ωα-ωÇĞİÖŞÜçğıöşü](?:[²³¹⁰⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉̄])?$")
FORMULA_SIMPLE_SYMBOL_RE = re.compile(r"^[A-Za-zΑ-Ωα-ωÇĞİÖŞÜçğıöşü](?:[²³¹⁰⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉̄])?$")
FORMULA_TEST_SYMBOL_RE = re.compile(r"^[A-Za-zΑ-Ωα-ωÇĞİÖŞÜçğıöşü](?:[²³¹⁰⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉̄])?$")
FORMULA_PARENS_RE = re.compile(r"^-?(?:\d+(?:\.\d+)?|\.\d+)(?:,-?(?:\d+(?:\.\d+)?|\.\d+))*$")
FORMULA_EXPR_RE = re.compile(
    r"^(?:[A-Za-zΑ-Ωα-ωÇĞİÖŞÜçğıöşü](?:[²³¹⁰⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉̄])?|-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|-?\.\d+)"
    r"(?:[+\-*/^](?:[A-Za-zΑ-Ωα-ωÇĞİÖŞÜçğıöşü](?:[²³¹⁰⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉̄])?|-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|-?\.\d+)){1,2}$"
)
MARKDOWN_LINK_TARGET_RE = re.compile(
    r"(?:https?://|www\.)[^()\s]+|mailto:[^()\s]+|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
)
DOI_CORE_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$")
DOI_WITH_PREFIX_RE = re.compile(r"^DOI:10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$", re.IGNORECASE)
ISBN_HYPHENATED_RE = re.compile(r"^(?:\d-){8}[\dXx]$|^(?:\d{3}-)(?:\d+-){3}[\dXx]$")


def check_regex(word, pattern):
    # print(f"Checking {pattern} for word: {word}")
    return word if REGEX_PATTERNS[pattern].search(CharFix.fix(word)) else None


def punc_count(word: str) -> int:
    return sum(1 for char in word if char in puncs)

def social_media_punc_count(word: str) -> int:
    return sum(1 for char in word if char in puncs and char != '_')



def punc_pos(word: str) -> list:
    return [i for i, char in enumerate(word) if char in puncs]


def apply_charfix(func):
    def wrapper(word, *args, **kwargs):
        fixed_word = CharFix.fix(word)
        return func(fixed_word, *args, **kwargs)

    return wrapper


def tr_lowercase(func):
    def wrapper(word, *args, **kwargs):
        turkish_lowercase = CharFix.tr_lowercase(word)
        return func(word, turkish_lowercase, *args, **kwargs)

    return wrapper


# noinspection PyTypeChecker
class TokenPreProcess:

    def __init__(self):
        pass

    @staticmethod
    def _is_formula_term(term: str) -> bool:
        return bool(FORMULA_TERM_RE.fullmatch(term))

    @staticmethod
    def _is_formula_expression(expr: str) -> bool:
        return bool(FORMULA_EXPR_RE.fullmatch(expr))

    @staticmethod
    def _split_formula_operator(word: str):
        for operator in ("≤", "≥", "<", ">", "="):
            if operator in word:
                left, right = word.split(operator, 1)
                if left and right:
                    return left, operator, right
        return None

    @staticmethod
    def _is_ip_address(word: str) -> bool:
        try:
            ipaddress.ip_address(word)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_bibliographic_abbr(word: str) -> bool:
        return word in {"ISBN", "DOI"}

    @staticmethod
    def _split_consecutive_hashtags(word: str):
        matches = list(re.finditer(r"#[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\-\uFE0F]+", word))
        if not matches or matches[0].start() != 0:
            return None

        if "".join(match.group(0) for match in matches) != word or len(matches) < 2:
            return None

        return [match.group(0) for match in matches]

    @staticmethod
    def _process_markdown_link_part(link_part: str):
        if not (len(link_part) > 2 and link_part[0] == "(" and link_part[-1] == ")"):
            return None

        content = link_part[1:-1]
        if not content:
            return None

        if content.startswith("mailto:"):
            email_part = content[len("mailto:"):]
            if TokenPreProcess.is_email(email_part):
                return [("(", "Punc"), (content, "Email"), (")", "Punc")]

        processed_link = TokenPreProcess.is_in_parenthesis(link_part)
        return processed_link

    # Regex Based Tokens
    # These functions get the input token, checks against to regular expressions defined above and
    # return word, tag as tuple

    @staticmethod
    @apply_charfix
    def is_ip_address(word: str) -> list:
        return [(word, "IP_Address")] if TokenPreProcess._is_ip_address(word) else None

    @staticmethod
    @apply_charfix
    def is_doi(word: str) -> list:
        if DOI_WITH_PREFIX_RE.fullmatch(word) or DOI_CORE_RE.fullmatch(word):
            return [(word, "DOI")]
        return None

    @staticmethod
    @apply_charfix
    def is_isbn(word: str) -> list:
        return [(word, "ISBN")] if ISBN_HYPHENATED_RE.fullmatch(word) else None

    @staticmethod
    @apply_charfix
    def is_bibliographic_abbr(word: str) -> list:
        return [(word, "Abbr")] if TokenPreProcess._is_bibliographic_abbr(word) else None

    @staticmethod
    @apply_charfix
    def is_formula(word: str) -> list:
        if not word or any(char.isspace() for char in word):
            return None

        if any(char in word for char in {"@", "#", "'"}):
            return None

        if word.startswith("±"):
            return [(word, "Formula")] if TokenPreProcess._is_formula_term(word[1:]) else None

        match = re.fullmatch(r"([A-Za-zΑ-Ωα-ωÇĞİÖŞÜçğıöşü](?:[²³¹⁰⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉̄])?)\(([^()]*)\)([=<>≤≥])(.+)", word)
        if match:
            symbol, paren_content, operator, right = match.groups()
            if FORMULA_TEST_SYMBOL_RE.fullmatch(symbol) and FORMULA_PARENS_RE.fullmatch(paren_content) and TokenPreProcess._is_formula_term(right):
                return [(word, "Formula")]
            return None

        split_result = TokenPreProcess._split_formula_operator(word)
        if not split_result:
            return None

        left, operator, right = split_result
        if not FORMULA_SIMPLE_SYMBOL_RE.fullmatch(left):
            return None

        if operator != "=":
            return [(word, "Formula")] if TokenPreProcess._is_formula_term(right) else None

        if TokenPreProcess._is_formula_term(right) or TokenPreProcess._is_formula_expression(right):
            return [(word, "Formula")]

        return None

    @staticmethod
    @apply_charfix
    def is_multiple_hashtag(word: str) -> list:
        hashtags = TokenPreProcess._split_consecutive_hashtags(word)
        if not hashtags:
            return None

        return [(hashtag, "Hashtag") for hashtag in hashtags]

    @staticmethod
    @apply_charfix
    def is_mention_suffix(word: str) -> list:
        result = check_regex(word, "mention_suffix")
        return [(result, "Mention_Suffix")] if result else None

    @staticmethod
    @apply_charfix
    def is_hashtag_suffix(word: str) -> list:
        result = check_regex(word, "hashtag_suffix")
        return [(result, "Hashtag_Suffix")] if result else None

    @staticmethod
    @apply_charfix
    def is_numeric_hyphenated_with_apostrophe_suffix(word: str) -> list:
        result = check_regex(word, "numeric_hyphenated_suffix")
        return [(result, "Apostrophed")] if result else None

    @staticmethod
    @apply_charfix
    def is_mention(word: str) -> list:
        result = check_regex(word, "mention")
        if result:
            return [(result, "Mention")] if result else None

        p_count = social_media_punc_count(word)
        if p_count == 2:
            punc = word[-1]
            word_parts = word.rsplit(word[-1], 1)
            if len(word_parts) == 2:
                result = check_regex(word_parts[0], "mention")
                if result:
                    return [("".join(word_parts[:-1]), "Mention"), (punc, "Punc")] if result else None
        elif p_count == 1:
            result = check_regex(word, "mention")
            if result:
                return [(result, "Mention")] if result else None

    @staticmethod
    @apply_charfix
    def is_hashtag(word: str) -> list:
        result = check_regex(word, "hashtag")
        if result:
            return [(result, "Hashtag")] if result else None

        p_count = social_media_punc_count(word)
        # As # symbol is also a punc we set
        if p_count == 2:
            punc = word[-1]
            word_parts = word.rsplit(word[-1], 1)
            if len(word_parts) == 2:
                result = check_regex(word_parts[0], "hashtag")
                if result:
                    return [("".join(word_parts[:-1]), "Hashtag"), (punc, "Punc")] if result else None
        elif p_count == 1:
            result = check_regex(word, "hashtag")
            if result:
                return [(result, "Hashtag")] if result else None

    @staticmethod
    @apply_charfix
    def is_in_quotes(word: str) -> list:
        result = check_regex(word, "in_quotes")
        if result:
            initial_quotes = word[0]
            final_quotes = word[-1]
            content = word[1:-1]
            processed_content = TokenProcessor.process_token(content)
            if isinstance(processed_content, tuple):
                processed_content = [processed_content]
            return [(initial_quotes, "Punc")] + processed_content + [(final_quotes, "Punc")] if result else None

    @staticmethod
    @apply_charfix
    def is_opening_quote(word: str) -> list:
        if len(word) > 1 and word[0] in {'"', "'"}:
            content = word[1:]
            if not content:
                return None

            processed_content = TokenProcessor.process_token(content)
            if isinstance(processed_content, tuple):
                processed_content = [processed_content]
            elif not isinstance(processed_content, list):
                processed_content = [(content, "OOV")]

            return [(word[0], "Punc")] + processed_content
        return None

    @staticmethod
    @apply_charfix
    def is_escaped_opening_quote(word: str) -> list:
        if len(word) > 2 and word[0] == "\\" and word[1] in {'"', "'"}:
            content = word[2:]
            if not content:
                return None

            processed_content = TokenProcessor.process_token(content)
            if isinstance(processed_content, tuple):
                processed_content = [processed_content]
            elif not isinstance(processed_content, list):
                processed_content = [(content, "OOV")]

            return [("\\", "Punc"), (word[1], "Punc")] + processed_content
        return None

    @staticmethod
    @apply_charfix
    def is_abbr_with_apostrophe_suffix(word: str) -> list:
        match = re.fullmatch(r"([A-Za-zÇĞİÖŞÜçğıöşü]+\.?)'([A-Za-zÇĞİÖŞÜçğıöşü]+)", word)
        if not match:
            return None

        abbr_part = match.group(1)
        suffix_part = match.group(2)
        normalized_abbr = CharFix.tr_lowercase(abbr_part)

        if not abbr_part.endswith("."):
            return None

        if normalized_abbr not in LocalData.abbrs() and abbr_part not in LocalData.candidate_abbrs():
            return None

        processed_suffix = TokenProcessor.process_token(suffix_part)
        if isinstance(processed_suffix, tuple):
            processed_suffix = [processed_suffix]
        elif not isinstance(processed_suffix, list):
            processed_suffix = [(suffix_part, "OOV")]

        return [(abbr_part, "Abbr"), ("'", "Punc")] + processed_suffix

    @staticmethod
    @apply_charfix
    def is_hyphenated_with_apostrophe_suffix(word: str) -> list:
        if "'" not in word or "-" not in word:
            return None

        stem, suffix = word.rsplit("'", 1)
        if not stem or not suffix:
            return None

        if any(char.isdigit() for char in stem):
            return None

        processed_stem = TokenProcessor.process_token(stem)
        if TokenProcessor.is_oov(processed_stem):
            return None

        processed_suffix = TokenProcessor.process_token(suffix)
        if isinstance(processed_suffix, tuple):
            processed_suffix = [processed_suffix]
        elif not isinstance(processed_suffix, list):
            processed_suffix = [(suffix, "OOV")]

        return processed_stem + [("'", "Punc")] + processed_suffix

    @staticmethod
    def is_numbered_title(word: str) -> list:
        # Check if the word matches the "numbered_title" regex pattern
        match = re.match(r'^(\((\d{1,2}|[IVXLCDM]+)\)|\[(\d{1,2}|[IVXLCDM]+)\]|\{(\d{1,2}|[IVXLCDM]+)\})', word, re.IGNORECASE)
        if match:
            numbered_title = match.group(1)
            inner_value = numbered_title[1:-1]
            normalized_inner = CharFix.tr_lowercase(inner_value).replace("ı", "i")
            roman_match = re.fullmatch(
                r'(m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3}))\.?',
                normalized_inner
            )
            is_roman_inner = bool(roman_match) and any(char in "mdclxvi" for char in normalized_inner)

            if not (inner_value.isdigit() or is_roman_inner):
                return None

            rest = word[len(numbered_title):]
            tokens = [(numbered_title, "Numbered_Title")]

            if rest:
                processed_rest = TokenProcessor.process_token(rest)
                if isinstance(processed_rest, tuple):
                    processed_rest = [processed_rest]
                tokens.extend(processed_rest)

            return tokens

        return None

    @staticmethod
    @apply_charfix
    def is_in_parenthesis(word: str):
        if len(word) > 2 and word[0] in "([{<" and word[-1] in ")]}>":
            initial_parenthesis = word[0]
            final_parenthesis = word[-1]
            content = word[1:-1]  # Extract content inside parentheses

            # Process the content inside the parentheses
            processed_content = TokenProcessor.process_token(content)
            if isinstance(processed_content, tuple):
                processed_content = [processed_content]

            # Return tokens with parentheses as separate tokens
            return [(initial_parenthesis, "Punc")] + processed_content + [(final_parenthesis, "Punc")]
        return None

    @staticmethod
    @apply_charfix
    def is_parenthesized_with_trailing_colon(word: str):
        if len(word) > 3 and word[0] == "(" and word.endswith("):"):
            content = word[1:-2]
            if not content:
                return None

            processed_content = TokenProcessor.process_token(content)
            if isinstance(processed_content, tuple):
                processed_content = [processed_content]
            elif not isinstance(processed_content, list):
                processed_content = [(content, "OOV")]

            return [("(", "Punc")] + processed_content + [(")", "Punc"), (":", "Punc")]
        return None

    @staticmethod
    @apply_charfix
    def is_markdown_link(word: str):
        match = re.fullmatch(rf"(\[[^\[\]]+\])\(({MARKDOWN_LINK_TARGET_RE.pattern})\)", word)
        if not match:
            return None

        label_part, link_content = match.groups()
        processed_label = TokenPreProcess.is_in_parenthesis(label_part)
        processed_link = TokenPreProcess._process_markdown_link_part(f"({link_content})")

        if not processed_label or not processed_link:
            return None

        return processed_label + processed_link

    @staticmethod
    @apply_charfix
    def is_markdown_link_tail(word: str):
        match = re.fullmatch(rf"(.+)(\])\(({MARKDOWN_LINK_TARGET_RE.pattern})\)", word)
        if not match:
            return None

        label_tail, closing_bracket, link_content = match.groups()
        processed_tail = TokenProcessor.process_token(label_tail)
        processed_link = TokenPreProcess._process_markdown_link_part(f"({link_content})")

        if isinstance(processed_tail, tuple):
            processed_tail = [processed_tail]

        if not processed_tail or not processed_link:
            return None

        return processed_tail + [(closing_bracket, "Punc")] + processed_link

    @staticmethod
    def is_date_range(word: str) -> list:
        result = check_regex(word, "date_range") or check_regex(word, "year_range")
        if result:
            return [(result, "Date_Range")] if result else None

    @staticmethod
    @apply_charfix
    def is_date_range_suffix(word: str) -> list:
        result = check_regex(word, "date_range_suffix")
        return [(result, "Date_Range_Suffix")] if result else None

    @staticmethod
    @apply_charfix
    def is_complex_punc(word: str) -> list:
        # Check if the token starts and ends with punctuation
        if punc_count(word) > 3 and word[0] in puncs and word[-1] in puncs:
            # Ensure there's meaningful content inside the punctuation
            inner_content = word[1:-1]
            if inner_content and not all(char in puncs for char in inner_content):
                return [(word, "Complex_Punc")]
        return None

    @staticmethod
    def is_date(word: str):
        result = DateCheck.is_date(word)
        return [(word, "Date")] if result else None

    @staticmethod
    def is_hour(word: str) -> tuple:
        result = check_regex(word, "hour")
        return [(result, "Hour")] if result else None
    @staticmethod
    def is_hour_suffix(word: str) -> tuple:
        result = check_regex(word, "hour_suffix")
        return [(result, "Hour_Suffix")] if result else None

    @staticmethod
    @apply_charfix
    def is_number_suffix(word: str) -> list:
        result = check_regex(word, "number_suffix")
        if not result:
            return None

        number_part, suffix_part = word.rsplit("'", 1)
        if TokenPreProcess.is_number(number_part) and suffix_part:
            return [(word, "Number")]

        return None

    @staticmethod
    @apply_charfix
    def is_currency_suffix(word: str) -> list:
        result = check_regex(word, "currency_suffix")
        if not result:
            return None

        currency_part, suffix_part = word.rsplit("'", 1)
        if TokenPreProcess.is_currency(currency_part) and suffix_part:
            return [(word, "Currency")]

        return None

    @staticmethod
    @apply_charfix
    def is_percentage_numbers(word: str) -> list:
        # Check if the word starts with a percentage symbol
        if word.startswith('%'):
            # Extract the numeric part after the '%'
            main_part = word[1:]
            suffix = ""

            # Check if there is a suffix (e.g., `'ye`, `'de`)
            for i, char in enumerate(main_part):
                if not char.isdigit() and char not in [',', '.']:
                    suffix = main_part[i:]
                    main_part = main_part[:i]
                    break

            # Process the main part (numeric part)
            if main_part.isdigit() or (',' in main_part or '.' in main_part):
                tokens = [('%' + main_part, 'Percentage_Numbers')]

                # Process the suffix if it exists
                if suffix:
                    processed_suffix = TokenProcessor.process_token(suffix)
                    if isinstance(processed_suffix, tuple):
                        processed_suffix = [processed_suffix]
                    tokens.extend(processed_suffix)

                return tokens

        # If the word does not match the expected format, return None
        return None

    @staticmethod
    @apply_charfix
    def is_percentage_numbers_chars(word: str) -> list:
        result = check_regex(word, "percentage_numbers_chars")
        if result:
            if word[-1] in puncs:
                initial = word[:-1]
                final = word[-1]
                processed_word = TokenProcessor.process_token(initial)
                if isinstance(processed_word, tuple):
                    processed_word = [processed_word]
                if isinstance(processed_word, list) and all(isinstance(item, tuple) for item in processed_word):
                    return processed_word + [(final, "Punc")]
                else:
                    raise ValueError(f"Unexpected result format: {processed_word}")
            else:
                return [(word, "Percentage_Numbers")]
        return []

    @staticmethod
    def is_roman_number(word: str) -> list:
        if not word or not any(char.upper() in {"M", "D", "C", "L", "X", "V", "I"} for char in word):
            return None
        result = check_regex(word, "roman_number")
        if result:
            return [(result, "Roman_Number")] if result else None

    @staticmethod
    def is_bullet_list(word: str) -> list:
        result = check_regex(word, "bullet_list")
        return [(result, "Bullet_List")] if result else None

    @staticmethod
    def is_email_punc(word: str) -> list:
        result = check_regex(word, "email_punc")
        if result:
            start_punc_count = 0
            end_punc_count = 0
            for char in word:
                if char in puncs:
                    start_punc_count += 1
                else:
                    break
            for char in word[::-1]:
                if char in puncs:
                    end_punc_count += 1
                else:
                    break
            initial_punc = word[:start_punc_count] if start_punc_count > 0 else ""
            final_punc = word[-end_punc_count:] if end_punc_count > 0 else ""
            if start_punc_count > 0 and end_punc_count > 0:
                email_part = word[start_punc_count: -end_punc_count]
            elif start_punc_count > 0:
                email_part = word[start_punc_count:]
            elif end_punc_count > 0:
                email_part = word[:-end_punc_count]
            else:
                email_part = word
            result_list = []
            if initial_punc:
                result_list.append((initial_punc, "Punc"))
            if email_part:
                result_list.append((email_part, "Email"))
            if final_punc:
                result_list.append((final_punc, "Punc"))
            return result_list if result else None

    @staticmethod
    def is_email(word: str) -> list:
        result = check_regex(word, "email")
        if result and any(dne in word for dne in LocalData.domains()) and word[0] not in puncs and word[-1] not in puncs:
            return [(result, "Email")] if result else None

    @staticmethod
    def is_full_url(word: str) -> list:
        if any(dne in word for dne in LocalData.domains()) and "@" not in word and word[0] not in puncs and word[-1] not in [")", "(", "[", "]"]:
            result = check_regex(word, "full_url")
            if "'" in word:
                # word.split("'")
                return [(result, "URL_Suffix")] if result else None
            else:
                return [(result, "Full_URL")] if result else None

    @staticmethod
    def is_web_url(word: str) -> list:
        if any(dne in word for dne in LocalData.domains()) and "@" not in word and word[0] not in puncs and word[-1] not in [")", "(", "[", "]"]:
            result = check_regex(word, "web_url")
            if "'" in word:
                # word.split("'")
                return [(result, "URL_Suffix")] if result else None
            else:
                return [(result, "Web_URL")] if result else None

    @staticmethod
    def is_copyright(word: str) -> tuple:
        result = check_regex(word, "copyright")
        return [(result, "Copyright")] if result else None

    @staticmethod
    def is_registered(word: str) -> list:
        result = check_regex(word, "registered")
        return [(result, "Registered")] if result else None

    @staticmethod
    def is_trademark(word: str) -> list:
        result = check_regex(word, "trade_mark")
        return [(result, "Trademark")] if result else None

    @staticmethod
    @apply_charfix
    def is_marked_with_trailing_punc(word: str) -> list:
        for suffix_len in range(1, len(word)):
            trailing_punc = word[-suffix_len:]
            core = word[:-suffix_len]

            if not core or not all(char in puncs for char in trailing_punc):
                continue

            for checker in (
                TokenPreProcess.is_copyright,
                TokenPreProcess.is_registered,
                TokenPreProcess.is_trademark,
            ):
                marked = checker(core)
                if marked:
                    return marked + [(char, "Punc") for char in trailing_punc]

        return None

    @staticmethod
    def is_currency(word: str) -> list:
        result = check_regex(word, "currency")
        return [(result, "Currency")] if result else None

    @staticmethod
    @apply_charfix
    def is_num_char_sequence(word: str) -> list:
        # Check if the word matches the numeric character sequence regex
        result = check_regex(word, "num_char_sequence")

        if result:
            separators = ["-", "|", "(", ")", ":", ";", "—", "\\"]
            for sep in separators:
                if sep in word:
                    parts = word.split(sep)
                    # print(len(parts), parts)

                    if len(parts) == 2:
                        initial = TokenProcessor.process_token(parts[0])
                        final = TokenProcessor.process_token(parts[1])

                        if isinstance(initial, tuple):
                            initial = [initial]
                        if isinstance(final, tuple):
                            final = [final]

                        return initial + [(sep, "Punc")] + final

            if len(word) > 1 and word[-1] in separators:
                final_punc = word[-1]
                remaining_word = word[:-1]
                processed_word = TokenProcessor.process_token(remaining_word)

                if isinstance(processed_word, tuple):
                    processed_word = [processed_word]

                return processed_word + [(final_punc, "Punc")]

        return [(word, "OOV")]

    # Lexicon Based Tokens
    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_abbr(word: str, lower_word: str) -> list:
        return [(word, "Abbr")] if lower_word in LocalData.abbrs() else None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_in_lexicon(word: str, lower_word: str) -> list:
        # print(lower_word)
        return [(word, "Valid_Word")] if lower_word in LocalData.word_list() else None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_in_exceptions(word: str, lower_word: str) -> list:
        return [(word, "Exception")] if lower_word in LocalData.exception_words() else None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_in_eng_words(word, lower_word: str) -> list:
        return [(word, "English_Word")] if lower_word in LocalData.eng_word_list() else None

    @staticmethod
    def is_smiley(word: str) -> list:
        return [(word, "Smiley")] if word in LocalData.smileys() else None

    @staticmethod
    def is_emoticon(word: str):
        word = unicodedata.normalize('NFC', word)
        word = word.replace(" ", "")
        if word in LocalData.emoticons():
            return [(word, "Emoticon")]

        emoticon_segments = EmoticonParser.emoticon_tokenize(word).split("\n")
        if len(emoticon_segments) == 1 and emoticon_segments[0] == word and EmoticonParser.emoticon_count(word) == 1:
            return [(word, "Emoticon")]

        return None

    # Multi-Unit Tokens
    @staticmethod
    def is_multiple_smiley(word: str) -> list:
        if SmileyParser.consecutive_smiley(word) and not str(word[0:-1]).isalnum():
            smiley_tokens = SmileyParser.smiley_tokenize(word).split("\n")
            smiley_list = [(smiley, "Smiley") for smiley in smiley_tokens]
            return smiley_list
        return None

    @staticmethod
    def is_smiley_in(word: str) -> list:
        if not any(char.isalnum() for char in word):
            return None

        segments = SmileyParser.smiley_split(word)
        if not any(is_smiley for _, is_smiley in segments):
            return None

        filtered_segments = []
        for index, (segment, is_smiley) in enumerate(segments):
            if not is_smiley:
                filtered_segments.append((segment, False))
                continue

            if segment.isalnum():
                filtered_segments.append((segment, False))
                continue

            prev_char = segments[index - 1][0][-1] if index > 0 and segments[index - 1][0] else ""
            next_char = segments[index + 1][0][0] if index + 1 < len(segments) and segments[index + 1][0] else ""

            if prev_char.isalnum() and next_char.isalnum():
                filtered_segments.append((segment, False))
            else:
                filtered_segments.append((segment, True))

        if not any(is_smiley for _, is_smiley in filtered_segments):
            return None

        merged_segments = []
        for segment, is_smiley in filtered_segments:
            if merged_segments and not is_smiley and not merged_segments[-1][1]:
                merged_segments[-1] = (merged_segments[-1][0] + segment, False)
            else:
                merged_segments.append((segment, is_smiley))

        tokens = []
        for segment, is_smiley in merged_segments:
            if is_smiley:
                tokens.append((segment, "Smiley"))
                continue

            processed_segment = TokenProcessor.process_token(segment)
            if isinstance(processed_segment, tuple):
                tokens.append(processed_segment)
            elif isinstance(processed_segment, list):
                tokens.extend(processed_segment)
            else:
                tokens.append((segment, "OOV"))

        return tokens

    @staticmethod
    def is_multiple_smiley_in(word: str) -> list:
        return TokenPreProcess.is_smiley_in(word)

    @staticmethod
    def is_multiple_emoticon(word):
        return (word, "Multiple_Emoticon") if EmoticonParser.emoticon_count(word) >= 2 else None

    @staticmethod
    def is_emoticon_in(word: str) -> list:
        if EmoticonParser.emoticon_count(word) == 0:
            return None

        segments = EmoticonParser.emoticon_tokenize(word).split("\n")
        if len(segments) <= 1:
            return None

        tokens = []
        for segment in segments:
            if segment in LocalData.emoticons():
                tokens.append((segment, "Emoticon"))
                continue

            processed_segment = TokenProcessor.process_token(segment)
            if isinstance(processed_segment, tuple):
                tokens.append(processed_segment)
            elif isinstance(processed_segment, list):
                tokens.extend(processed_segment)
            else:
                tokens.append((segment, "OOV"))

        return tokens

    @staticmethod
    def is_number(word: str) -> list:
        # Check if the entire word is a number
        if word.isdigit():
            return [(word, "Number")]

        if re.fullmatch(r"[+-]\d+(?:\.\d+)?", word):
            return [(word, "Number")]

        if PuncMatcher.punc_count(word) == 1 and word.endswith("."):
            if all(char.isdigit() for char in word[:-1]):
                return [(word, "Ordinal_Number")]

        if PuncMatcher.punc_count(word) == 1 and ("," in word or "." in word):
            separator_index = max(word.find(","), word.find("."))
            if 0 < separator_index < len(word) - 1:
                if all(char.isdigit() for char in word if char not in {",", "."}):
                    # Ensure the word has at least one digit
                    if any(char.isdigit() for char in word):
                        return [(word, "Number")]

        # Check for patterns like number+characters
        # Ensure it's not mixed with complex formats like number+char+number
        match = re.fullmatch(r"(\d+)([a-zA-ZğüşöçİĞÜŞÖÇ]+)", word)
        if match:
            number_part = match.group(1)  # Extract the numeric part
            char_part = match.group(2)  # Extract the character part

            # Process the character part
            processed_word = TokenProcessor.process_token(char_part)
            if isinstance(processed_word, tuple):
                processed_word = [processed_word]  # Wrap tuple into a list for consistency
            elif not isinstance(processed_word, list):
                processed_word = [(char_part, "OOV")]  # Handle unexpected cases

            # Combine the numeric and processed character parts
            return [(number_part, "Number")] + processed_word

        # Check for standard patterns like numbers ending with specific suffixes
        if PuncMatcher.punc_count(word) == 1 and word[0:-1].isdigit():
            if word[-1] == "K":
                return [(word[0:-1], "Number"), ("K", "Kelvin")]
            elif word.endswith("°C"):
                return [(word[:-2], "Number"), ("°C", "Celsius")]
            elif word.endswith("°F"):
                return [(word[:-2], "Number"), ("°F", "Fahrenheit")]
            elif word[-1] == "°":
                return [(word[0:-1], "Number"), ("°", "Celsius")]
            elif "-" in word:
                return [(word, "Number_Sequence")]

        # Handle abbreviations defined in LocalData
        for abbr in LocalData.abbrs():
            if word.endswith(abbr) and word[:-len(abbr)].isdigit():
                return [(word[:-len(abbr)], "Number"), (abbr, "Abbr")]

        # Default case: if it doesn't match any known pattern
        return None

    @staticmethod
    @apply_charfix
    def is_fsp(word: str) -> list:
        if len(word) > 1 and word[-1] in puncs and PuncMatcher.punc_count(word) == 1:
            final_punc = word[-1]
            remaining_word = word[:-1]
            processed_word = TokenProcessor.process_token(remaining_word)
            if isinstance(processed_word, tuple):
                processed_word = [processed_word]
            return processed_word + [(final_punc, "Punc")]
        return None

    @staticmethod
    @apply_charfix
    def is_isp(word: str) -> list:
        if len(word) > 1 and word[0] in puncs and (word[0] != "@" and word[0] != "#") and PuncMatcher.punc_count(word) <= 2:
            initial_punc = word[0]
            remaining_word = word[1:]

            if remaining_word == word:
                return [(initial_punc, "Punc"), (remaining_word, "OOV")]

            processed_word = TokenProcessor.process_token(remaining_word)

            result = [(initial_punc, "Punc")]

            if isinstance(processed_word, list):
                result.extend(processed_word)
            elif isinstance(processed_word, tuple):
                result.append(processed_word)
            else:
                # Default case for out-of-vocabulary (OOV) words
                result.append((remaining_word, "OOV"))

            return result
        elif len(word) == 1 and word in puncs:
            return [(word, "Punc")]
        else:
            return [(word, "OOV")]

    @staticmethod
    @apply_charfix
    def is_mssp(word: str) -> list:
        if len(word) >= 3 and word[0] in puncs and word[-1] in puncs:
            # Match valid parenthetical patterns, excluding exceptions like "(!)"
            pattern = r"^([\(\[\{<]).*?([\)\]\}>])"
            match = re.search(pattern, word)

            if match and match.group(0) != "(!)":
                # Process the matched part as parenthetical content
                matched_part = match.group(0)
                rest = word[match.end():]  # Remaining part of the word after the match

                # Process the matched part
                matched_tokens = TokenPreProcess.is_in_parenthesis(matched_part) or []

                # Process the remaining part (if any)
                rest_tokens = TokenProcessor.process_token(rest) if rest else []

                # Combine tokens from matched part and remaining part
                return matched_tokens + rest_tokens

            # For general multi-punctuation, process as before
            initial_punc = word[0]
            final_punc = word[-1]
            remaining_word = word[1:-1]

            # Process the content between the punctuations
            processed_word = TokenProcessor.process_token(remaining_word) or []

            # Initialize the result with the starting punctuation
            result = [(initial_punc, "Punc")]

            # Add the processed content
            if isinstance(processed_word, list):
                result.extend(processed_word)
            elif isinstance(processed_word, tuple):
                result.append(processed_word)
            else:
                result.append((remaining_word, "OOV"))  # Default to OOV if no processing matches

            # Append the ending punctuation
            result.append((final_punc, "Punc"))
            return result

        return None  # Return None if conditions are not met

    @staticmethod
    @apply_charfix
    def is_msp(word: str) -> list:
        if len(word) >= 3 and word not in exception_list:
            start_punc_count = 0
            end_punc_count = 0
            # Count starting punctuation
            for char in word:
                if char in puncs:
                    start_punc_count += 1
                else:
                    break
            # Count ending punctuation
            for char in word[::-1]:
                if char in puncs:
                    end_punc_count += 1
                else:
                    break
            # Ensure word has both starting and ending punctuations and valid middle part
            if start_punc_count >= 1 and end_punc_count >= 1 and all(char not in puncs for char in word[start_punc_count: -end_punc_count]):
                initial_punc = word[:start_punc_count]
                final_punc = word[-end_punc_count:]
                remaining_word = word[start_punc_count: -end_punc_count]
                if remaining_word == '':
                    return [TokenProcessor.process_token(initial_punc), TokenProcessor.process_token(final_punc)]
                processed_word = TokenProcessor.process_token(remaining_word)
                if isinstance(processed_word, tuple):
                    processed_word = [processed_word]
                return [TokenProcessor.process_token(initial_punc)] + processed_word + [TokenProcessor.process_token(final_punc)]
        else:
            return None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_imp(word: str, lower_word: str) -> list:
        if len(word) > 1 and word not in exception_list:
            start_punc_count = 0
            # Count initial punctuation characters
            for char in word:
                if char in puncs:
                    start_punc_count += 1
                else:
                    break

            if start_punc_count >= 1:
                initial_punc = [(word[:start_punc_count], "Punc")]
                remaining_word = lower_word[start_punc_count:]
                if TokenPreProcess.is_three_or_more(remaining_word):
                    processed_word = TokenProcessor.process_token(remaining_word)
                    if isinstance(processed_word, tuple):
                        processed_word = [processed_word]
                    return initial_punc + processed_word
        return None

    @staticmethod
    @apply_charfix
    def is_fmp(word: str):
        if len(word) >= 3 and word[0] in puncs and word[-1] in puncs:
            return None

        # Check if the word matches any exception from the exception list
        for exception in exception_list:
            # Case 1: The word ends with an exception
            if word.endswith(exception):
                main_word = word[:-len(exception)]
                exception_token = (exception, "Punc")

                if main_word:
                    processed_main_word = TokenProcessor.process_token(main_word)
                    if isinstance(processed_main_word, tuple):
                        processed_main_word = [processed_main_word]
                    return processed_main_word + [exception_token]
                else:
                    return [exception_token]

        # Handle patterns like (!), extract and split
        special_pattern = r"(\(!\))"
        match = re.search(special_pattern, word)
        if match:
            # Split the word into parts
            split_parts = word.split(match.group(1))
            tokens = []

            # Process the part before the match
            if split_parts[0]:
                processed_before = TokenProcessor.process_token(split_parts[0])
                if isinstance(processed_before, tuple):
                    tokens.append(processed_before)
                else:
                    tokens.extend(processed_before)

            # Add the matched part as a separate token
            tokens.append((match.group(1), "Punc"))

            # Process the part after the match
            if len(split_parts) > 1 and split_parts[1]:
                processed_after = TokenProcessor.process_token(split_parts[1])
                if isinstance(processed_after, tuple):
                    tokens.append(processed_after)
                else:
                    tokens.extend(processed_after)

            return tokens

        # Handle trailing punctuations generally
        trailing_punc_pattern = r"(\W+)$"
        match = re.search(trailing_punc_pattern, word)
        if match:
            trailing_punc = match.group(0)
            main_word = word[:match.start()]

            tokens = []
            # Preserve analyzable stems like ordinal numbers before splitting the
            # remaining trailing punctuation character-by-character.
            processed_main_word = None
            remaining_punc = trailing_punc
            if main_word:
                for split_index in range(1, len(trailing_punc)):
                    candidate = main_word + trailing_punc[:split_index]
                    processed_candidate = TokenProcessor.process_token(candidate)
                    if not TokenProcessor.is_oov(processed_candidate):
                        processed_main_word = processed_candidate
                        remaining_punc = trailing_punc[split_index:]
                        break

                if processed_main_word is None:
                    processed_main_word = TokenProcessor.process_token(main_word)

                if isinstance(processed_main_word, tuple):
                    tokens.append(processed_main_word)
                else:
                    tokens.extend(processed_main_word)

            # Process each punctuation mark in the trailing punctuation separately
            for char in remaining_punc:
                tokens.append((char, "Punc"))

            return tokens

        # If no conditions are met, return None
        return None

    @staticmethod
    @apply_charfix
    def is_apostrophed(word: str) -> list:
        if PuncMatcher.punc_count(word) == 1 and "'" in word:
            result = check_regex(word, "apostrophed")
            if result:
                # Split the word into parts around the apostrophe
                parts = word.split("'")

                # Validate each part using the lexicon processor
                part1_result = TokenProcessor.process_lexicon_based(parts[0])
                part2_result = TokenProcessor.process_lexicon_based(parts[1])

                # Check if both parts are valid words
                if part1_result and part1_result[0][1] == "Valid_Word" and part2_result and part2_result[0][
                    1] == "Valid_Word" and len(part2_result) > 3:
                    return [
                        part1_result[0],  # First part
                        ("'", "Punc"),  # Apostrophe
                        part2_result[0]  # Second part
                    ]

                # Fallback: If one or both parts are invalid
                return [(word, "Apostrophed")]

        # If no apostrophe is found or the word does not match the regex
        return None

    @staticmethod
    def is_single_punc(word: str) -> list:
        if len(word) == 1 and word in puncs:
            return [(word, "Punc")]
        else:
            return None

    @staticmethod
    def is_multi_punc(word: str) -> list:
        # Check if the word is in the exception list directly
        if word in exception_list:
            return [(word, "Punc")]

        # Check for exceptions at both the beginning and end of the word
        for exception in exception_list:
            if word.endswith(exception):
                split_part = word[:-len(exception)]
                if split_part:
                    processed_split_part = TokenProcessor.process_token(split_part)
                    if isinstance(processed_split_part, tuple):
                        processed_split_part = [processed_split_part]
                    return processed_split_part + [(exception, "Punc")]
                return [(exception, "Punc")]

            if word.startswith(exception):
                split_part = word[len(exception):]
                if split_part:
                    processed_split_part = TokenProcessor.process_token(split_part)
                    if isinstance(processed_split_part, tuple):
                        processed_split_part = [processed_split_part]
                    return [(exception, "Punc")] + processed_split_part
                return [(exception, "Punc")]

        # Enhanced trailing punctuation handling
        trailing_punc_pattern = r"(\W+)$"
        match = re.search(trailing_punc_pattern, word)

        if match:
            trailing_punc = match.group(0)
            main_word = word[:match.start()]

            # Split trailing punctuation into individual marks
            split_punc = re.findall(r'\W+', trailing_punc)

            result = []
            if main_word:
                processed_main_word = TokenProcessor.process_token(main_word)
                if isinstance(processed_main_word, tuple):
                    processed_main_word = [processed_main_word]
                result.extend(processed_main_word)

            # Add each trailing punctuation mark as a separate token
            for punc in split_punc:
                if punc in exception_list:
                    result.append((punc, "Punc"))
                else:
                    for char in punc:
                        result.append((char, "Punc"))
            return result
        # If no conditions are met, return None
        return None

    @staticmethod
    @apply_charfix
    def is_single_hyphenated(word: str):
        if "-" in word and len(word) > 3 and word[0] != "-" and word[-1] != "-":
            result = check_regex(word, "single_hyphen")
            return [(word, "Single_Hyphenated")] if result else None

    @staticmethod
    @apply_charfix
    def is_multi_hyphenated(word: str):
        if "-" in word and len(word) > 3 and word[0] != "-" and word[-1] != "-":
            result = check_regex(word, "multi_hyphen")
            return [(word, "Multi_Hyphenated")] if result else None

    @staticmethod
    @apply_charfix
    def is_single_underscored(word: str):
        if "_" in word and len(word) > 3 and word[0] != "_" and word[-1] != "_":
            result = check_regex(word, "single_underscore")
            return [(word, "Single_Underscored")] if result else None

    @staticmethod
    @apply_charfix
    def is_multi_underscored(word: str):
        if "_" in word and len(word) > 3 and word[0] != "_" and word[-1] != "_":
            result = check_regex(word, "multi_underscore")
            return [(word, "Multi_Underscored")] if result else None

    @staticmethod
    @apply_charfix
    def is_three_or_more(word: str) -> list:
        exceptions = ["...", "!!!"]
        if word in exceptions:
            return [(word, "Punc")]
        result = check_regex(word, "three_or_more")
        if result:
            return [(word, "Three_Or_More")] if result else None

    @staticmethod
    @apply_charfix
    def is_non_latin(word):
        allowed_chars = set("abcçdefgğhıijklmnoöprsştuüvyzwqxâîûABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZWQXÂÎ")
        sum_foreign_char = sum(
            1 for char in word if char not in allowed_chars and char not in puncs and not char.isdigit())
        sum_punc = PuncMatcher.punc_count(word)
        has_digit = any(char.isdigit() for char in word)
        hyphen_check = PuncMatcher.hyphen_in(word)
        single_underscore_check = TokenPreProcess.is_single_underscored(word)
        multi_underscore_check = TokenPreProcess.is_multi_underscored(word)
        multiple_emoticon = TokenPreProcess.is_multiple_emoticon(word)
        if sum_foreign_char >= 1 and sum_punc == 0 and not has_digit and not hyphen_check and not multiple_emoticon and not single_underscore_check and not multi_underscore_check:
            return [(word, "Non_Latin")]
        return None

    @staticmethod
    def is_one_char_fixable(word: str):
        extra_chars = ["¬", "º", "0", "1", "-"]
        # Think a solution for "-"
        for extra in extra_chars:
            if PuncMatcher.punc_pos(extra) != [0] or PuncMatcher.punc_pos(word) != [-1]:
                fixed_word = word.replace(extra, "")
                if TokenPreProcess.is_in_lexicon(fixed_word):
                    return [(fixed_word, "One_Char_Fixed")]
        return None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_midsp(word: str, lower_word: str):
        if (
                len(word) >= 3
                and word not in exception_list
                and word[0] not in puncs
                and word[-1] not in puncs
                and "_" not in word
                and "-" not in word
        ):
            # Find the positions of middle punctuation marks
            mid_punc_pos = [i for i in range(1, len(word) - 1) if word[i] in puncs]

            # If there is exactly one middle punctuation mark
            if len(mid_punc_pos) == 1:
                mid_punc_idx = mid_punc_pos[0]
                initial_part = lower_word[:mid_punc_idx]
                mid_punc = word[mid_punc_idx]
                remaining_part = lower_word[mid_punc_idx + 1:]

                # Check if all non-punctuation characters are numbers
                if initial_part.replace(".", "").isdigit() and remaining_part.replace(".", "").isdigit():
                    return [(word, "Number")]  # Return the word as a whole if it consists of numbers

                # Otherwise, process and split the word
                processed_initial = TokenProcessor.process_token(initial_part)
                processed_remaining = TokenProcessor.process_token(remaining_part)

                if isinstance(processed_initial, tuple):
                    processed_initial = [processed_initial]
                if isinstance(processed_remaining, tuple):
                    processed_remaining = [processed_remaining]

                return processed_initial + [(mid_punc, "Punc")] + processed_remaining

        return None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_midmp(word: str, lower_word: str):
        if (
                len(word) > 2
                and word not in exception_list
                and lower_word not in LocalData.exception_words()
                and word not in LocalData.abbrs()
                and word[0] not in puncs
                and word[-1] not in puncs
                and PuncMatcher.punc_count(word) >= 2
                and "_" not in word
                and "-" not in word
        ):
            mid_punc_pos = [i for i in range(1, len(word) - 1) if word[i] in puncs]

            # Check if all non-punctuation characters are numeric
            non_punc_parts = re.split(r"[{}]".format(re.escape(puncs)), word)
            if all(part.replace(".", "").isdigit() for part in non_punc_parts if part):
                return [(word, "Number")]

            if mid_punc_pos:
                tokens_with_puncs = []
                start_idx = 0

                # Iterate through the punctuation positions
                for punc_idx in mid_punc_pos:
                    initial_part = lower_word[start_idx:punc_idx]
                    mid_punc = word[punc_idx]

                    if initial_part:
                        processed_initial = TokenProcessor.process_token(initial_part)
                        if isinstance(processed_initial, tuple):
                            tokens_with_puncs.append(processed_initial)
                        else:
                            tokens_with_puncs.extend(processed_initial)

                    tokens_with_puncs.append((mid_punc, "Punc"))

                    start_idx = punc_idx + 1

                # Process the remaining part of the word
                remaining_part = lower_word[start_idx:]
                if remaining_part:
                    processed_remaining = TokenProcessor.process_token(remaining_part)
                    if isinstance(processed_remaining, tuple):
                        tokens_with_puncs.append(processed_remaining)
                    else:
                        tokens_with_puncs.extend(processed_remaining)

                return tokens_with_puncs

        return None

    @staticmethod
    def is_math(word: str) -> tuple:
        # Count the number of distinct mathematical operators in the word
        operator_count = sum(1 for op in MATH_OPERATORS if op in word)

        # Return the token as "Math_Operator" only if there are at least two distinct operators
        if operator_count >= 2:
            return [(word, "Math_Operator")]
        return None

    # This is an idea for next version.
    # Besides TS Corpus Word List,
    # https://data.tdd.ai/#/16e5fbcf-a658-424d-b50c-4454a4b367dc
    # for any possible missing words
    # A root + suffix possibilities might be used
    # @staticmethod
    # @apply_charfix
    # @tr_lowercase
    # def is_root_plus_suffix(word: str, lower_word: str) -> list:
    #    known_roots = ["kitap", "evrak", "çanta", "su"]
    #    for root in known_roots:
    #        if lower_word.startswith(root):
    #            suffix = lower_word[len(root):]
    #            if suffix and suffix in LocalData.suffixes():
    #                return [(root, "Root"), (suffix, "Suffix")]
    #    return None


lexicon_based = [
    TokenPreProcess.is_in_exceptions,
    TokenPreProcess.is_emoticon,
    TokenPreProcess.is_smiley,
    TokenPreProcess.is_bibliographic_abbr,
    TokenPreProcess.is_abbr,
    TokenPreProcess.is_in_lexicon,
    TokenPreProcess.is_in_eng_words,
    TokenPreProcess.is_single_punc,
]

regex = [
    TokenPreProcess.is_ip_address,
    TokenPreProcess.is_doi,
    TokenPreProcess.is_isbn,
    TokenPreProcess.is_formula,
    TokenPreProcess.is_mention_suffix,
    TokenPreProcess.is_hashtag_suffix,
    TokenPreProcess.is_numeric_hyphenated_with_apostrophe_suffix,
    TokenPreProcess.is_full_url,
    TokenPreProcess.is_web_url,
    TokenPreProcess.is_email,
    TokenPreProcess.is_currency,
    TokenPreProcess.is_date_range_suffix,
    TokenPreProcess.is_date_range,
    TokenPreProcess.is_date,
    TokenPreProcess.is_hour,
    TokenPreProcess.is_hour_suffix,
    TokenPreProcess.is_currency_suffix,
    TokenPreProcess.is_hyphenated_with_apostrophe_suffix,
    TokenPreProcess.is_number_suffix,
    TokenPreProcess.is_number,
    TokenPreProcess.is_mention,
    TokenPreProcess.is_multiple_hashtag,
    TokenPreProcess.is_hashtag,
    TokenPreProcess.is_in_quotes,
    TokenPreProcess.is_escaped_opening_quote,
    TokenPreProcess.is_opening_quote,
    TokenPreProcess.is_abbr_with_apostrophe_suffix,
    TokenPreProcess.is_apostrophed,
    TokenPreProcess.is_numbered_title,
    TokenPreProcess.is_parenthesized_with_trailing_colon,
    TokenPreProcess.is_markdown_link,
    TokenPreProcess.is_markdown_link_tail,
    TokenPreProcess.is_in_parenthesis,
    TokenPreProcess.is_roman_number,
    TokenPreProcess.is_registered,
    TokenPreProcess.is_copyright,
    TokenPreProcess.is_trademark,
    TokenPreProcess.is_marked_with_trailing_punc,
    TokenPreProcess.is_bullet_list,
    TokenPreProcess.is_roman_number,
    TokenPreProcess.is_percentage_numbers_chars,
    TokenPreProcess.is_percentage_numbers,
    TokenPreProcess.is_emoticon_in,
    TokenPreProcess.is_smiley_in,
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


class TokenProcessor:

    @staticmethod
    def format_output(output, output_format):
        if output_format == 'tuple':
            return tuple(output)
        elif output_format == 'list':
            return list(output)
        elif output_format == 'string':
            return f"{output[0]}\t{output[1]}"
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    @staticmethod
    def process_token(token: str, output_format: str = 'tuple') -> list:
        """
        Main method to process a token using (i) lexicon-based, (ii) regex-based,
        (iii) multi-punctuation, and (iv) single-punctuation checks in order.
        Note that the order is important!
        """

        # Step 1: Lexicon-based checks
        result = TokenProcessor.process_lexicon_based(token, output_format)
        if not TokenProcessor.is_oov(result):
            return result

        # Step 2: Regex-based checks
        result = TokenProcessor.process_regex(token, output_format)
        if not TokenProcessor.is_oov(result):
            return result

        # Step 3: Multi punctuation checks
        result = TokenProcessor.process_multi_punc(token, output_format)
        if not TokenProcessor.is_oov(result):
            return result

        # Step 4: Single punctuation checks
        result = TokenProcessor.process_single_punc(token, output_format)
        if not TokenProcessor.is_oov(result):
            return result

        # Step 5: Default case - return OOV if no checks matched
        return [(token, "OOV")]

    @staticmethod
    def process_lexicon_based(token: str, output_format: str = 'tuple') -> list:
        for CHECK in lexicon_based:
            result = CHECK(token)
            if result:
                return result

    @staticmethod
    def process_regex(token: str, output_format: str = 'tuple') -> list:
        for CHECK in regex:
            result = CHECK(token)
            if result:
                return result

    @staticmethod
    def process_single_punc(token: str, output_format: str = 'tuple') -> list:
        for CHECK in single_punc:
            result = CHECK(token)
            if result:
                return result

   # @staticmethod
    # def process_multi_punc(token: str, output_format: str = 'tuple') -> list:
    #    for CHECK in multi_punc:
    #        result = CHECK(token)
    #        if result:
    #            return result

    @staticmethod
    def process_multi_punc(token: str, output_format: str = 'tuple') -> list:
        # Avoid cyclic recursion by checking for already processed tokens
        if not token or all(char in puncs for char in token):  # Avoid reprocessing pure punctuation
            return [(token, "Punc")]

        # Handle exceptions or already processed tokens
        for CHECK in multi_punc:
            result = CHECK(token)
            if result:
                return result

        return [(token, "OOV")]  # Default fallback

    @staticmethod
    def is_oov(result):
        """
        Helper method to check if the result is Out-Of-Vocabulary (OOV).
        """
        return not result or all(tag == "OOV" for _, tag in result)
