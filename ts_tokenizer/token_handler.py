import re
import string
from typing import List, Tuple, Any

from .data import LocalData
from .char_fix import CharFix
from .date_check import DateCheck
from .smiley_check import SmileyParser
from .emoticon_check import EmoticonParser
from .punctuation_process import PuncMatcher

puncs = re.escape(string.punctuation)
extra_puncs = ["–", "°", "—", "(", ")"]
puncs += re.escape(''.join(extra_puncs))
domains_pattern = '|'.join([re.escape(domain[1:]) for domain in LocalData.domains()])  # Escaping only necessary parts

# Create a dict of RegExps
REGEX_PATTERNS = {
    # Precompiled regular expressions using re.compile()
    # "xml_tag": re.compile(r"^<\s*/?\s*\w+(\s+\w+\s*=\s*\"[^\"]*\")*\s*/?\s*>$"),
    "xml_tag": re.compile(r"<\s*/?\s*\w+(\s+\w+\s*=\s*\"[^\"]*\")*\s*/?\s*>"),
    "hashtag": re.compile(r'^#[^#]{1,143}$'),
    "mention": re.compile(r'^@[^@]{1,143}$'),
    "email": re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b(?![.,!?;:])'),
    "email_punc": re.compile(r'\b[' + re.escape(string.punctuation) + r']*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[' + re.escape(string.punctuation) + r']*\b'),
    "url_pattern": re.compile(fr'^(?:(?:http|https|ftp)://)?(?:www\.)?[-a-zA-Z0-9:%._\\+~#=]{{1,256}}(?:{domains_pattern})(?:\.[a-zA-Z]{{2,3}})?(?:/[-a-zA-Z0-9()@:%_\\+.~#?&//=]*)?\b(?![.,!?;:])'),
    "hour": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9](?: ?[AP]M)?(?:'te|'de|'da|'den|'dan|'ten|'tan|'deki|'daki)?$"),
    "percentage_numbers_chars": re.compile(r'%(\d+\D+)'),
    "percentage_numbers": re.compile(r'(%\d{1,3}(?:\.\d{3})*(?:,\d+)?|\d{1,3}(?:\.\d{3})*(?:,\d+)?%)'),
    "single_hyphen": re.compile(r'^(?!-)[\w]+-[\w]+(?!-)$'),
    "date_range": re.compile(r'^\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}$'),
    #"date_range": re.compile(r'^\d{4}-\d{4}$'),
    "in_parenthesis": re.compile(r'^[\(\[\{][^()\[\]{}]*[\)\]\}]$'),
    "in_quotes": re.compile(r'^[\'"][^\'"]*[\'"]$'),
    "copyright": re.compile(r'(?:^©[a-zA-Z0-9]+$)|(?:^[a-zA-Z0-9]+©$)'),
    "registered": re.compile(r'(?:^®[a-zA-Z]+$)|(?:^[a-zA-Z]+®$)'),
    "trade_mark": re.compile(r'(?:^™[a-zA-Z]+$)|(?:^[a-zA-Z]+™$)'),
    "bullet_list": re.compile(r'^•[a-zA-Z]+$'),
    "initial_parenthesis": re.compile(r"^([\(\[\{]+)([^\)]+)([\)\]\}]+)(.*)$"),
    "three_or_more": re.compile(r'^([{}])\1{{2,}}$'.format(re.escape(string.punctuation))),
    "num_char_sequence": re.compile(r'\d+[\w\s]*'),
    "roman_number": re.compile(r'^(M{1,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?$'),

#    "roman_number": re.compile(r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?$'),
    "apostrophed": re.compile(r"\b\w+'[a-zA-ZıiİüÜçÇöÖşŞğĞ]+\b"),
    "currency": re.compile(rf"^(?:[{re.escape(''.join(LocalData.currency_symbols()))}]\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?|\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?[{re.escape(''.join(LocalData.currency_symbols()))}])$")
}


exception_list = ["(!)", "...", "[...]"]


def check_regex(word, pattern):
    # print(f"Checking {pattern} for word: {word}")
    return word if REGEX_PATTERNS[pattern].search(CharFix.fix(word)) else None


def punc_count(word: str) -> int:
    return sum(1 for char in word if char in puncs)


def punc_pos(word: str) -> list:
    return [i for i, char in enumerate(word) if char in puncs]


def split_on_punctuation(word: str, punctuation_list: str, depth: int = 0) -> list:
    result = []
    i = 0
    for j, char in enumerate(word):
        if char in punctuation_list:
            if i < j:  # Only process if there's something between punctuation
                processed_token = TokenProcessor.process_token(word[i:j], depth=depth+1)
                if isinstance(processed_token, list):
                    result.extend(processed_token)
                else:
                    result.append((word[i:j], processed_token[1]))
            result.append((char, "Punc"))
            i = j + 1
    if i < len(word):  # Process any remaining part after the last punctuation
        processed_token = TokenProcessor.process_token(word[i:], depth=depth+1)
        if isinstance(processed_token, list):
            result.extend(processed_token)
        else:
            result.append((word[i:], processed_token[1]))
    # Filter out any empty tokens from the result
    return [token for token in result if token[0] != '']




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


class TokenPreProcess:

    def __init__(self):
        pass

    # Regex Based Tokens
    # These functions get the input token, checks against to regexs defined above and
    # return word, tag as tuple
    @staticmethod
    def is_xml(word: str) -> tuple:
        # Check if the word starts with '<' and ends with '>', and there are no other '<' or '>' inside the word
        if word.startswith("<") and word.endswith(">") and (word.count("<") == 1 and word.count(">") == 1):
            if "/" not in word and " " in word:
                result = check_regex(word, "xml_tag")
                return (result, "XML_Tag") if result else None
            elif " " not in word and "/" in word:
                result = check_regex(word, "xml_tag")
                return (result, "XML_Tag") if result else None

    @staticmethod
    @apply_charfix
    def is_mention(word: str) -> list:
        p_count = PuncMatcher.punc_count(word)
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
        p_count = PuncMatcher.punc_count(word)
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
    def is_in_parenthesis(word: str) -> list:
        if len(word) > 2:
            result = check_regex(word, "in_parenthesis")
            if result:
                if punc_count(word) < 3 and "'" not in word and re.match(r"^\([0-9]{1,2}\)$", word):
                    return [(word, "Numbered_Title")] if result else None

                else:
                    initial_parenthesis = word[0]
                    final_parenthesis = word[-1]
                    content = word[1:-1]
                    if all(char.isalpha() or char in ['.', '-'] for char in content):
                        return [(word[0], "Punc"), TokenProcessor.process_token(content), (word[-1], "Punc")]
                    processed_content = TokenProcessor.process_token(content)
                    if isinstance(processed_content, tuple):
                        processed_content = [processed_content]
                    return [(initial_parenthesis, "Punc")] + processed_content + [(final_parenthesis, "Punc")]


    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_initial_parenthesis(word: str, lower_word: str) -> list:
        result = check_regex(word, "initial_parenthesis")
        if result:
            parts = re.split(r"[)\]\}]", word)
            if word[0] == "(":
                parenthesis_content = parts[0] + ")"
            elif word[0] == "[":
                parenthesis_content = parts[0] + "]"
            elif word[0] == "{":
                parenthesis_content = parts[0] + "}"
            if re.match(r'^[\(\[\{]\d{1,2}[\)\]\}]$', parenthesis_content) and "'" not in word:  # Matches "(1)", "(20)", etc.
                numbered_title = [(parenthesis_content, "Numbered_Title")]
                remaining_part = parts[1].strip()
                processed_remaining = TokenProcessor.process_token(remaining_part) if remaining_part else []
                if isinstance(processed_remaining, tuple):
                    processed_remaining = [processed_remaining]
                return [(numbered_title + processed_remaining)] if processed_remaining else None

            processed_parenthesis = TokenPreProcess.is_in_parenthesis(parenthesis_content)
            remaining_part = parts[1].strip()
            processed_remaining = TokenProcessor.process_token(remaining_part) if remaining_part else []
            if isinstance(processed_remaining, tuple):
                processed_remaining = [processed_remaining]

            # Ensure processed_parenthesis is not None
            return [(processed_parenthesis or []) + processed_remaining] if processed_remaining else None

    @staticmethod
    def is_date_range(word: str) -> tuple:
        result = check_regex(word, "date_range")
        if result:
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
        if result:
            return (word, "Percentage_Numbers") if result else None

    @staticmethod
    @apply_charfix
    def is_percentage_numbers_chars(word: str) -> list:
        result = check_regex(word, "percentage_numbers_chars")
        if result:
            if word[-1] in puncs:
                initial = word[:-1]
                final = word[-1]
                processed_word = (initial, final)
                if isinstance(processed_word, tuple):
                    return [(TokenProcessor.process_token(initial)), (final, "Punc")] if result else None
            else:
                return [(word, "Percentage_Numbers")]

    @staticmethod
    def is_roman_number(word: str) -> tuple:
        result = check_regex(word, "roman_number")
        return (result, "Roman_Number") if result else None

    @staticmethod
    def is_bullet_list(word: str) -> tuple:
        result = check_regex(word, "bullet_list")
        return (result, "Bullet_List") if result else None

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
    def is_email(word: str) -> tuple:
        result = check_regex(word, "email")
        if result and any(dne in word for dne in LocalData.domains()) and word[0] not in puncs and word[-1] not in puncs:
            return (result, "Email") if result else None

    @staticmethod
    def is_url(word: str) -> tuple:
        if any(dne in word for dne in LocalData.domains()) and "@" not in word and word[0] not in puncs and word[-1] not in [")", "(", "[", "]"]:
            result = check_regex(word, "url_pattern")
            if "'" in word:
                word.split("'")
                return (result, "URL_Suffix") if result else None
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
    def is_trademark(word: str) -> tuple:
        result = check_regex(word, "trade_mark")
        return (result, "Trade_Mark") if result else None

    @staticmethod
    def is_currency(word: str) -> tuple:
        result = check_regex(word, "currency")
        return (result, "Currency") if result else None

    @staticmethod
    @apply_charfix
    def is_num_char_sequence(word: str) -> list:
        result = check_regex(word, "num_char_sequence")
        if result:
            separators = ["-", "|", "(", ")", ":", ";", "—", "\\",]
            # I may prefer using puncs here, dont know yet.
            for sep in separators:
                if sep in word:
                    parts = word.split(sep)

                    if len(parts) == 2 and parts[0] and parts[1]:
                        initial = TokenProcessor.process_token(parts[0])
                        final = TokenProcessor.process_token(parts[1])

                        if isinstance(initial, tuple):
                            initial = [initial]
                        if isinstance(final, tuple):
                            final = [final]

                        return [(initial + [(sep, "Punc")] + final)] if result else None

            if len(word) > 1 and word[-1] in separators:
                final_punc = word[-1]
                remaining_word = word[:-1]
                processed_word = TokenProcessor.process_token(remaining_word)

                if isinstance(processed_word, tuple):
                    processed_word = [processed_word]

                return [(processed_word + [(final_punc, "Punc")])] if result else None

            return [(result, "Num_Char_Sequence")] if result else [(word, "Num_Char_Sequence")]

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
            return (word, "Valid_Word") if word in LocalData.word_list() else None

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
            return (word_fixed, "English_Word") if word_fixed else None

    @staticmethod
    def is_smiley(word):
        return (word, "Smiley") if word in LocalData.smileys() else None

    @staticmethod
    def is_emoticon(word):
        # Ensure the word is not empty or a single punctuation mark
        if not word or all(char in string.punctuation for char in word):
            return None
        return (word, "Emoticon") if word in LocalData.emoticons() else None

    # Multi-Unit Tokens
    @staticmethod
    def is_multiple_smiley(word):
        if SmileyParser.consecutive_smiley(word) and not str(word[0:-1]).isalnum():
            return (word, "Multiple_Smiley")
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

    def is_fsp(word: str) -> list:
        if punc_count(word) == 1 and word[-1] in puncs:
            final_punc = word[-1]
            remaining_word = word[:-1]
            processed_word = TokenProcessor.process_token(remaining_word)
            if isinstance(processed_word, tuple):
                processed_word = [processed_word]
                return [(processed_word + [(final_punc, "Punc")])]
        else:
            return None


    @staticmethod
    @apply_charfix
    def is_isp(word: str) -> list:
        if len(word) > 1 and word[0] in puncs:
            initial_punc = word[0]
            remaining_word = word[1:]
            processed_word = TokenProcessor.process_token(remaining_word)

            result = [(initial_punc, "Punc")]
            if isinstance(processed_word, list):
                result.extend(processed_word)
            elif isinstance(processed_word, tuple):
                result.append(processed_word)
            return result
        else:
            return None


    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_mssp(word: str, lower_word: str) -> list:
        if len(word) > 2 and word[0] in puncs and word[-1] in puncs:
            initial_punc = word[0]
            final_punc = word[-1]
            remaining_word = lower_word[1:-1]

            processed_word = TokenProcessor.process_token(remaining_word)

            result = [(initial_punc, "Punc")]
            if isinstance(processed_word, list):
                result.extend(processed_word)
            elif isinstance(processed_word, tuple):
                result.append(processed_word)
            result.append((final_punc, "Punc"))

            return result
        return None

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
        else:
            return None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_fmp(word: str, lower_word: str) -> list:
        if punc_count(word) >= 2 and word[0] not in puncs:
            # Check for exceptions
            for exception in exception_list:
                if exception in word:
                    before_exception, exception_part, after_exception = word.partition(exception)
                    tokens = []
                    if before_exception:
                        tokens.append(TokenProcessor.process_token(before_exception))
                    tokens.append((exception_part, "Punc"))
                    if after_exception:
                        if after_exception in puncs:
                            tokens.append((after_exception, "Punc"))
                        else:
                            tokens.append(TokenProcessor.process_token(after_exception))
                    return tokens


        # Condition to check if all punctuation marks are the same
        fmp_regex = re.compile(rf"[{puncs}]{{2,}}$")
        if fmp_regex.search(word):
            first_punc_index = next((i for i, char in enumerate(word) if char in puncs), None)
            before_punc = word[:first_punc_index]
            from_punc = word[first_punc_index:]

            if from_punc in exception_list:
                return [TokenProcessor.process_token(before_punc), (from_punc, "Punc")]

            # Handle identical punctuation characters
            if len(set(from_punc)) == 1:  # All punctuation marks are the same
                if before_punc:
                    return [TokenProcessor.process_token(before_punc), (from_punc, "Punc")]
                else:
                    return [(from_punc, "Punc")]

            if len(word) > 1 and word not in exception_list:
                end_punc_count = 0
                for char in word[::-1]:
                    if char in puncs:
                        end_punc_count += 1

                if end_punc_count >= 2 and all(char not in puncs for char in word[:-end_punc_count]):
                    final_punc = word[-end_punc_count:]
                    remaining_word = word[:-end_punc_count]
                    lower_remaining_word = lower_word[:-end_punc_count]
                    processed_word = TokenProcessor.process_token(lower_remaining_word)
                    if isinstance(processed_word, tuple):
                        processed_word = [processed_word]
                    if processed_word:
                        processed_word[0] = (remaining_word, processed_word[0][1])
                    separated_puncs = [(char, "Punc") for char in final_punc]
                    return [processed_word + separated_puncs]

            return [TokenProcessor.process_token(word)]

    @staticmethod
    @apply_charfix
    def is_apostrophed(word: str) -> list:
        result = check_regex(word, "apostrophed")
        if result:
            if word[-1] in puncs:
                return [(word[:-1], "Apostrophed"), (word[-1], "Punc")]
            else:
                return [(word, "Apostrophed")] if result else None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_midp(word: str, lower_word: str) -> list:
        if len(word) > 2 and word not in exception_list and word[0] not in puncs and word[-1] not in puncs and punc_count(word) >= 2 and "_" not in word and  "-" not in word:
            mid_punc_pos = [i for i in range(1, len(word) - 1) if word[i] in puncs]

            if len(mid_punc_pos) == 1:
                mid_punc_idx = mid_punc_pos[0]
                initial_part = lower_word[:mid_punc_idx]
                mid_punc = word[mid_punc_idx]
                remaining_part = lower_word[mid_punc_idx + 1:]

                processed_initial = TokenProcessor.process_token(initial_part)
                processed_remaining = TokenProcessor.process_token(remaining_part)

                if isinstance(processed_initial, tuple):
                    processed_initial = [processed_initial]
                if isinstance(processed_remaining, tuple):
                    processed_remaining = [processed_remaining]

                return processed_initial + [(mid_punc, "Punc")] + processed_remaining
            else:
                return [TokenProcessor.process_token(word)]
        else:
            return None


    @staticmethod
    def is_punc(word):
        if word in exception_list:
            return [(word, "Punc")]
        return [(word, "Punc")] if all(char in puncs for char in word) else None


    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_underscored(word: str, lower_word: str) -> list:
        if "_" in word and len(word) > 3 and word[0] != "_" and word[-1] != "_":
            parts = lower_word.split("_")
            processed_parts = [TokenProcessor.process_token(part) for part in parts]
            if all(processed_part[1] == "Valid_Word" for processed_part in processed_parts):
                return [(word, "Underscored")]
        else:
            return None

    @staticmethod
    @apply_charfix
    @tr_lowercase
    def is_hyphenated(word: str, lower_word: str) -> list:
        if "-" in word and len(word) > 3 and word[0] != "-" and word[-1] != "-":
            parts = lower_word.split("-")
            processed_parts = [TokenProcessor.process_token(part) for part in parts]
            if all(processed_part[1] == "Valid_Word" for processed_part in processed_parts):
                return [(word, "Hyphenated")]
        else:
            return None


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
        underscore_check = TokenPreProcess.is_underscored(word)
        multiple_emoticon = TokenPreProcess.is_multiple_emoticon(word)
        if sum_foreign_char >= 1 and sum_punc == 0 and not has_digit and not hyphen_check and not multiple_emoticon and not underscore_check:
            return word, "Non_Latin"
        return None

    @staticmethod
    def is_one_char_fixable(word):
        extra_chars = ["¬","º", "0", "1"]
        for extra in extra_chars:
            if PuncMatcher.punc_pos(extra) != [0] or PuncMatcher.punc_pos(word) != [-1]:
                fixed_word = word.replace(extra, "")
                if TokenPreProcess.is_in_lexicon(fixed_word):
                    return fixed_word, "One_Char_Fixed"
        return None


# Lexicon-Based Matches
lexicon_based_methods = [
    TokenPreProcess.is_abbr,
    TokenPreProcess.is_in_exceptions,
    TokenPreProcess.is_in_lexicon,
    TokenPreProcess.is_in_eng_words,
    TokenPreProcess.is_emoticon,
    TokenPreProcess.is_number,
    TokenPreProcess.is_smiley,
    TokenPreProcess.is_multiple_smiley,
    TokenPreProcess.is_multiple_smiley_in,
    TokenPreProcess.is_multiple_emoticon,
    TokenPreProcess.is_non_latin,
    TokenPreProcess.is_one_char_fixable
]

# Regex-Based Matches
regex_based_methods = [
    TokenPreProcess.is_xml,
    TokenPreProcess.is_punc,
    TokenPreProcess.is_in_quotes,
    TokenPreProcess.is_in_parenthesis,
    TokenPreProcess.is_apostrophed,
    TokenPreProcess.is_url,
    TokenPreProcess.is_underscored,
    TokenPreProcess.is_hyphenated,
    TokenPreProcess.is_date_range,
    TokenPreProcess.is_date,
    TokenPreProcess.is_hour,
    TokenPreProcess.is_email,
    TokenPreProcess.is_email_punc,
    TokenPreProcess.is_mention,
    TokenPreProcess.is_hashtag,
    TokenPreProcess.is_copyright,
    TokenPreProcess.is_registered,
    TokenPreProcess.is_trademark,
    TokenPreProcess.is_currency,
    TokenPreProcess.is_percentage_numbers_chars,
    TokenPreProcess.is_percentage_numbers,
    TokenPreProcess.is_imp,
    TokenPreProcess.is_isp,
    TokenPreProcess.is_fsp,
    TokenPreProcess.is_fmp,
    TokenPreProcess.is_mssp,
    TokenPreProcess.is_msp,
    TokenPreProcess.is_midp,
    TokenPreProcess.is_roman_number,
    TokenPreProcess.is_bullet_list,
    TokenPreProcess.is_num_char_sequence,
    TokenPreProcess.is_three_or_more
]


class TokenProcessor:
    # Limit for recursion depth
    MAX_DEPTH = 100

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
    def process_token(token: str, output_format: str = 'tuple', depth: int = 0) -> tuple:
        if depth > TokenProcessor.MAX_DEPTH:
            return (token, "OOV")

        try:
            for check in lexicon_based_methods:
                result = check(token)
                if result:
                    return TokenProcessor.format_output(result, output_format) if result else None
            for check in regex_based_methods:
                result = check(token)
                if result:
                    return TokenProcessor.format_output(result, output_format) if result else None
        except Exception as e:
            print(f"Error processing token '{token}': {e}")

        return TokenProcessor.format_output((token, "OOV"), output_format)




