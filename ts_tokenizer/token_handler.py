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
extra_puncs = ["–", "'", "°", "—", "(", ")"]
puncs += re.escape(''.join(extra_puncs))
domains_pattern = '|'.join([re.escape(domain[1:]) for domain in LocalData.domains()])  # Escaping only necessary parts

# Create a dict of RegExps
REGEX_PATTERNS = {
    "xml_tag": r"<\s*\w+(\s+\w+\s*=\s*\"[^\"]+\")+\s*/?>|</\w+\s*>",
    "hashtag": r'^#[^#]{1,143}$',
    "mention": r'^@[^@]{1,143}$',
    "email": r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b(?![.,!?;:])',
    "email_punc": r'\b[' + re.escape(string.punctuation) + r']*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[' + re.escape(string.punctuation) + r']*\b',
    "url_pattern": fr'(?:(?:http|https|ftp)://)?(?:www\.)?[-a-zA-Z0-9:%._\\+~#=]{{1,256}}(?:{domains_pattern})(?:\.[a-zA-Z]{{2,3}})?(?:/[-a-zA-Z0-9()@:%_\\+.~#?&//=]*)?\b(?![.,!?;:])',
    "hour": r"\b(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9](?: ?[AP]M)?(?:'te|'de|'da|'den|'dan|'ten|'tan|'deki|'daki)?(?=$|\s)",
    "percentage_numbers_chars": r'%(\d+\D+)',
    "percentage_numbers": r'(%\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d{1,3}(?:\.\d{3})*(?:,\d+)?%)',
    "single_hyphen": r'^(?!-)[\w]+-[\w]+(?!-)$',
    "date_range": r'^\d{4}-\d{4}$',
    "in_parenthesis": '^[\(\[\{][^()\[\]{}]*[\)\]\}]$',
    "in_quotes": r'^[\'"][^\'"]*[\'"]$',
    "copyright": r'(?:^©[a-zA-Z0-9]+$)|(?:^[a-zA-Z0-9]+©$)',
    "registered": r'(?:^®[a-zA-Z]+$)|(?:^[a-zA-Z]+®$)',
    "three_or_more": r'([' + re.escape(string.punctuation) + r'])\1{2,}',
    "num_char_sequence": r'\d+[\w\s]*',
    "roman_number": r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?$',
    "apostrophed": r"\b\w+'[a-zA-ZıiİüÜçÇöÖşŞğĞ]+\b",
    "currency": rf"(?:[{re.escape(''.join(LocalData.currency_symbols()))}]\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?|\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?[{re.escape(''.join(LocalData.currency_symbols()))}])"
}

exception_list = ["(!)", "...", "[...]"]


def check_regex(word, pattern):
    return word if re.search(REGEX_PATTERNS[pattern], CharFix.fix(word)) else None


def punc_count(word: str) -> int:
    return sum(1 for char in word if char in puncs)


def punc_pos(word: str) -> list:
    return [i for i, char in enumerate(word) if char in puncs]


def apply_charfix(func):
    def wrapper(word, *args, **kwargs):
        fixed_word = CharFix.fix(word)
        # Pass the fixed word, and also any additional args (like lower_word)
        return func(fixed_word, *args, **kwargs)
    return wrapper


def tr_lowercase(func):
    def wrapper(word, *args, **kwargs):
        turkish_lowercase = CharFix.tr_lowercase(word)
        # Pass both original word and lowercase version to the function
        return func(word, turkish_lowercase, *args, **kwargs)
    return wrapper


class TokenPreProcess:

    def __init__(self):
        pass

    # Regex Based Tokens
    # These functions get the input token, checks against to regexs defined above and
    # return word, tag as tuple
    @staticmethod
    @apply_charfix
    def is_xml(word: str) -> tuple:
        result = check_regex(word, "xml_tag")
        return (result, "XML_Tag") if result else None

    @staticmethod
    @apply_charfix
    def is_mention(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "mention") if p_count == 1 else None
        return (result, "Mention") if result else None

    @staticmethod
    @apply_charfix
    def is_hashtag(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "hashtag") if p_count == 1 else None
        return (result, "Hashtag") if result else None

    @staticmethod
    @apply_charfix
    def is_in_quotes(word: str) -> list:
        result = check_regex(word, "in_quotes")
        if result:
            initial_parenthesis = word[0]
            final_parenthesis = word[-1]
            content = word[1:-1]
            processed_content = TokenProcessor.process_token(content)
            if isinstance(processed_content, tuple):
                processed_content = [processed_content]
            return [(initial_parenthesis, "Punc")] + processed_content + [(final_parenthesis, "Punc")]

    @staticmethod
    @apply_charfix
    def is_in_parenthesis(word: str) -> list:
        result = check_regex(word, "in_parenthesis")
        if result:
            initial_parenthesis = word[0]
            final_parenthesis = word[-1]
            content = word[1:-1]
            processed_content = TokenProcessor.process_token(content)
            if isinstance(processed_content, tuple):
                processed_content = [processed_content]
            return [(initial_parenthesis, "Punc")] + processed_content + [(final_parenthesis, "Punc")]

    @staticmethod
    def is_date_range(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        if PuncMatcher.find_punctuation(word) == "-" and p_count == 1:
            result = check_regex(word, "date_range")
            return (result, "Date_Range") if result else None

    @staticmethod
    def is_date(word: str) -> tuple:
        result = DateCheck.is_date(word)
        return (word, "Date") if result else None

    @staticmethod
    def is_hour(word: str) -> tuple:
        result = check_regex(word, "hour")
        return (result, "Hour") if result else None

    @staticmethod
    def is_percentage_numbers(word: str) -> tuple:
        p_count = PuncMatcher.punc_count(word)
        result = check_regex(word, "percentage_numbers") if p_count == 1 else None
        return (result, "Percentage_Numbers") if result else None

    @staticmethod
    @apply_charfix
    def is_percentage_numbers_chars(word: str) -> tuple:
        result = check_regex(word, "percentage_numbers_chars")
        return (result, "Percentage_Numbers_Chars") if result else None

    @staticmethod
    def is_roman_number(word: str) -> tuple:
        result = check_regex(word, "roman_number")
        return (result, "Roman_Number") if result else None

    @staticmethod
    def is_email_punc(word: str) -> list:
        # Check if the word matches the email with punctuation pattern
        result = check_regex(word, "email_punc")

        if result:
            # Initialize variables to count starting and ending punctuation
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

            # Handle case when there's no end punctuation or start punctuation
            initial_punc = word[:start_punc_count] if start_punc_count > 0 else ""
            final_punc = word[-end_punc_count:] if end_punc_count > 0 else ""

            # Extract email part
            if start_punc_count > 0 and end_punc_count > 0:
                email_part = word[start_punc_count: -end_punc_count]
            elif start_punc_count > 0:
                email_part = word[start_punc_count:]
            elif end_punc_count > 0:
                email_part = word[:-end_punc_count]
            else:
                email_part = word

            # Prepare output
            result_list = []
            if initial_punc:
                result_list.append((initial_punc, "Punc"))
            if email_part:
                result_list.append((email_part, "Email"))
            if final_punc:
                result_list.append((final_punc, "Punc"))

            return result_list

    @staticmethod
    def is_email(word: str) -> tuple:
        result = check_regex(word, "email")
        if result and any(dne in word for dne in LocalData.domains()) and word[0] not in puncs and word[-1] not in puncs:
            return (result, "Email")

    @staticmethod
    def is_url(word: str) -> tuple:
        if any(dne in word for dne in LocalData.domains()) and "@" not in word and word[0] not in puncs and word[-1] not in [")", "(", "[", "]"]:
            result = check_regex(word, "url_pattern")
            if "'" in word:
                return (result, "URL_Suffix")
            else:
                return (result, "URL") if result else None

    @staticmethod
    def is_copyright(word: str) -> tuple:
        result = check_regex(word, "copyright")
        return (result, "Copyright") if result else None

    @staticmethod
    def is_registered(word: str) -> tuple:
        result = check_regex(word, "registered")
        return (result, "Registered") if result else None

    @staticmethod
    def is_currency(word: str) -> tuple:
        result = check_regex(word, "currency")
        return (result, "Currency") if result else None

    @staticmethod
    @apply_charfix
    def is_num_char_sequence(word: str) -> tuple:
        result = check_regex(word, "num_char_sequence")
        return (result, "Num_Char_Sequence") if result else None

    # Lexicon Based Tokens
    @staticmethod
    @apply_charfix
    def is_abbr(word: str) -> tuple:
        # Use lower_word for comparison
        return (word, "Abbr") if word in LocalData.abbrs() else None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_in_lexicon(word: str, lower_word: str) -> tuple:
        if lower_word in LocalData.word_list():
            return word, "Valid_Word"

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_in_exceptions(word: str, lower_word: str) -> tuple:
        return (word, "Exception") if lower_word in LocalData.exception_words() else None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_in_eng_words(word, lower_word: str):
        word_fixed = CharFix.fix(word)
        if lower_word in LocalData.eng_word_list():
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
    @apply_charfix
    @tr_lowercase
    def is_fsp(word: str, lower_word: str) -> list:
        if len(word) > 1 and word[-1] in puncs and all(char not in puncs for char in word[:-1]):
            final_punc = word[-1]
            remaining_word = word[:-1]
            processed_word = TokenProcessor.process_token(remaining_word)
            if isinstance(processed_word, tuple):
                processed_word = [processed_word]
            return processed_word + [(final_punc, "Punc")]

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_isp(word: str, lower_word: str) -> list:
        if len(word) > 1 and word[0] in puncs and all(char not in puncs for char in word[1:]):
            initial_punc = word[0]
            remaining_word = word[1:]
            processed_word = TokenProcessor.process_token(remaining_word)
            if isinstance(processed_word, tuple):
                processed_word = [processed_word]

            return [(initial_punc, "Punc")] + processed_word

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_mssp(word: str, lower_word: str) -> list:
        if len(word) > 2 and word[0] in puncs and word[-1] in puncs and all(char not in puncs for char in word[1:-1]):
            initial_punc = TokenProcessor.process_token(word[0])
            final_punc = TokenProcessor.process_token(word[-1])
            remaining_word = lower_word[1:-1]
            processed_word = TokenProcessor.process_token(remaining_word)
            if isinstance(processed_word, tuple):
                processed_word = [processed_word]
            return [initial_punc] + processed_word + [final_punc]

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_msp(word: str, lower_word: str) -> list:
        if len(word) > 2 and word not in exception_list:
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
            if start_punc_count >= 1 and end_punc_count >= 1 and all(
                    char not in puncs for char in word[start_punc_count: -end_punc_count]):
                initial_punc = word[:start_punc_count]
                final_punc = word[-end_punc_count:]
                remaining_word = lower_word[start_punc_count: -end_punc_count]
                if remaining_word == '':
                    return [(initial_punc, "Punc"), (final_punc, "Punc")]
                processed_word = TokenProcessor.process_token(remaining_word)
                if isinstance(processed_word, tuple):
                    processed_word = [processed_word]
                return [(initial_punc, "Punc")] + processed_word + [(final_punc, "Punc")]

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_imp(word: str, lower_word: str) -> list:
        if len(word) > 1 and word not in exception_list:
            start_punc_count = 0
            for char in word:
                if char in puncs:
                    start_punc_count += 1
                else:
                    break
            if start_punc_count >= 2 and all(char not in puncs for char in word[start_punc_count:]):
                initial_punc = [(word[:start_punc_count], "Punc")]
                remaining_word = lower_word[start_punc_count:]
                processed_word = TokenProcessor.process_token(remaining_word)
                if isinstance(processed_word, tuple):
                    processed_word = [processed_word]
                return initial_punc + processed_word

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_fmp(word: str, lower_word: str) -> list:
        if len(word) > 1 and word not in exception_list:
            end_punc_count = 0
            for char in word[::-1]:
                if char in puncs:
                    end_punc_count += 1
                else:
                    break
            if end_punc_count >= 2 and all(char not in puncs for char in word[:-end_punc_count]):
                final_punc = word[-end_punc_count:]
                remaining_word = word[:-end_punc_count]
                lower_remaining_word = lower_word[:-end_punc_count]
                processed_word = TokenProcessor.process_token(lower_remaining_word)
                if isinstance(processed_word, tuple):
                    processed_word = [processed_word]
                if processed_word:
                    processed_word[0] = (remaining_word, processed_word[0][1])
                return processed_word + [(final_punc, "Punc")]

    @staticmethod
    @apply_charfix
    def is_apostrophed(word: str) -> tuple:
        result = check_regex(word, "apostrophed")
        if result:
            return word, "Apostrophed"

    @staticmethod
    @apply_charfix
    def is_midp(word: str) -> list:
        if len(word) > 2:
            if word[0] not in puncs and word[-1] not in puncs:
                mid_punc_pos = [i for i in range(1, len(word) - 1) if word[i] in puncs]
                if len(mid_punc_pos) == 1:
                    mid_punc_idx = mid_punc_pos[0]
                    initial_part = word[:mid_punc_idx]
                    mid_punc = word[mid_punc_idx]
                    remaining_part = word[mid_punc_idx + 1:]
                    processed_initial = TokenProcessor.process_token(initial_part)
                    processed_remaining = TokenProcessor.process_token(remaining_part)
                    if isinstance(processed_initial, tuple):
                        processed_initial = [processed_initial]
                    if isinstance(processed_remaining, tuple):
                        processed_remaining = [processed_remaining]
                    return processed_initial + [(mid_punc, "Punc")] + processed_remaining

    @staticmethod
    def is_punc(word):
        if word in exception_list:
            return word, "Punc"
        return (word, "Punc") if all(char in puncs for char in word) else None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_underscored(word: str, lower_word: str) -> tuple:
        if "_" in word and 1 <= word.count("_") <= 1 and word[0] != "_" and word[-1] != "_":
            parts = lower_word.split("_")
            # Check if it is alphanumeric underscored
            if len(parts) == 2 and parts[0].isalpha() and parts[1].isdigit() or parts[0].isdigit() and parts[1].isalpha():
                return word, "Alphanumeric_Underscored"
            # Check if all parts exist in the lexicon
            elif all(part in LocalData.word_list() for part in parts):
                return word, "Underscored"
            return word, "OOV"

    @staticmethod
    @apply_charfix
    def is_three_or_more(word):
        exceptions = ["...", "!!!"]
        if word in exceptions:
            return word, "Punc"
        result = check_regex(word, "three_or_more")
        return (result, "Three_Or_More") if result else None

    @staticmethod
    def is_non_latin(word):
        u_word = unicodedata.normalize('NFC', word)
        allowed_chars = set("abcçdefgğhıijklmnoöprsştuüvyzwqxâîûABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZWQXÂÎ")
        sum_foreign_char = sum(1 for char in u_word if char not in allowed_chars or char not in puncs)
        sum_punc = PuncMatcher.punc_count(u_word)
        has_digit = any(char.isdigit() for char in u_word)
        hyphen_check = PuncMatcher.hyphen_in(word)
        underscore_check = TokenPreProcess.is_underscored(word)
        multiple_emoticon = TokenPreProcess.is_multiple_emoticon(word)
        if sum_foreign_char >= 1 and sum_punc == 0 and not has_digit and not hyphen_check and not multiple_emoticon and not underscore_check:
            return u_word, "Non_Latin"
        return None

    @staticmethod
    def is_one_char_fixable(word):
        extra_chars = ["¬", "-"]
        for extra in extra_chars:
            if PuncMatcher.punc_pos(extra) != [0] or PuncMatcher.punc_pos(word) != [-1]:
                fixed_word = word.replace(extra, "")
                if TokenPreProcess.is_in_lexicon(fixed_word):
                    return fixed_word, "One_Char_Fixed"
        return None


check_methods = [
        # First Check for SGML tags |
        TokenPreProcess.is_xml,

        # Lexicon Based Tokens
        TokenPreProcess.is_abbr,
        TokenPreProcess.is_in_exceptions,
        TokenPreProcess.is_in_lexicon,
        TokenPreProcess.is_in_eng_words,
        TokenPreProcess.is_smiley,
        TokenPreProcess.is_emoticon,
        TokenPreProcess.is_number,


        # Specific Cases for Punctuation Use
        TokenPreProcess.is_in_quotes,
        TokenPreProcess.is_in_parenthesis,
        TokenPreProcess.is_underscored,

        TokenPreProcess.is_email,
        TokenPreProcess.is_email_punc,
        TokenPreProcess.is_url,
        TokenPreProcess.is_date_range,
        TokenPreProcess.is_date,
        TokenPreProcess.is_hour,

        # Various Status for Punctuation
        TokenPreProcess.is_apostrophed,

        # Basic Regex Tokens
        TokenPreProcess.is_mention,
        TokenPreProcess.is_hashtag,
        TokenPreProcess.is_copyright,
        TokenPreProcess.is_registered,
        TokenPreProcess.is_currency,
        TokenPreProcess.is_percentage_numbers_chars,
        TokenPreProcess.is_percentage_numbers,
        #TokenPreProcess.is_multiple_smiley_in,
        TokenPreProcess.is_multiple_smiley,
        TokenPreProcess.is_one_char_fixable,


        # These need recursive handling
        TokenPreProcess.is_fsp,
        TokenPreProcess.is_isp,
        TokenPreProcess.is_mssp,
        TokenPreProcess.is_msp,
        TokenPreProcess.is_midp,
        TokenPreProcess.is_imp,
        TokenPreProcess.is_fmp,

        # Raw Punctuation
        TokenPreProcess.is_punc,
        TokenPreProcess.is_roman_number,

        TokenPreProcess.is_multiple_emoticon,
        TokenPreProcess.is_three_or_more,
        TokenPreProcess.is_non_latin,
        # TokenPreProcess.is_num_char_sequence
    ]


class TokenProcessor:

    def __init__(self):
        pass

    @staticmethod
    def format_output(result, output_format):
        if output_format == 'tuple':
            return result
        elif output_format == 'list':
            return list(result)
        elif output_format == 'string':
            return f"{result[0]}\t{result[1]}"

    @staticmethod
    def process_token(token: str, output_format: str = 'tuple') -> tuple:
        for check in check_methods:
            result = check(token)
            if result:
                return TokenProcessor.format_output(result, output_format)

        # If no checks match, return "OOV" with the requested output format
        oov_result = (token, "OOV")
        return TokenProcessor.format_output(oov_result, output_format)