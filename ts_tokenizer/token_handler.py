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
extra_puncs = ["–", "°", "—"]
puncs += re.escape(''.join(extra_puncs))
domains_pattern = '|'.join([re.escape(domain[1:]) for domain in LocalData.domains()])
# Create a dict of RegExps
# noinspection RegExpRedundantEscape
REGEX_PATTERNS = {
    "hashtag": re.compile(r'^#[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F]{1,139}$'),
    "mention": re.compile(r'^@[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F]{1,15}$'),
    "email": re.compile(rf'^[^{puncs}][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+(?<![{puncs}])$'),
    "email_punc": re.compile(r'\b[' + re.escape(string.punctuation) + r']*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[' + re.escape(string.punctuation) + r']*\b'),
    "hour": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9]$"),
    "hour_suffix": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9](?:'te|'de|'da|'den|'dan|'ten|'tan|'deki|'daki)$"),
    "hour_12": re.compile(r"^(0[0-9]|1[0-9]|2[0-3])[:.][0-5][0-9]([AP]M)$"),
    "percentage_numbers_initial": re.compile(r'^%\d{1,3}(?:[.,]\d+)?$'),
    "percentage_numbers_final": re.compile(r'^\d{1,3}(?:[.,]\d+)*%$'),
    "percentage_numbers_chars": re.compile(r'^%\d{1,3}(?:[.,]\d+)*\D.*$'),
    "single_hyphen": re.compile(rf'^[^{puncs}]+-[^{puncs}]+$'),
    "multi_hyphen": re.compile(rf'^[^{puncs}]+(-[^{puncs}]+)+$'),
    "single_underscore": re.compile(rf'^[^{puncs}]+_[^{puncs}]+$'),
    "multi_underscore": re.compile(rf'^[^{puncs}]+(_[^{puncs}]+)+$'),
    "date_range": re.compile(r'^(?:(?:0[1-9]|[1-2][0-9]|3[0-1])\.(?:0[1-9]|1[0-2])\.\d{4})-(?:(?:0[1-9]|[1-2][0-9]|3[0-1])\.(?:0[1-9]|1[0-2])\.\d{4})$'),
    "year_range": re.compile(r'^(?:[1-9]\d{3})-(?:[1-9]\d{3})$'),
    "in_parenthesis": re.compile(r'^[(\[{]+[^()\[\]{}]*[)\]}]+}$'),
    "numbered_title": re.compile(r'^\((\d{1,2})\)|^\[(\d{1,2})\]|^{(\d{1,2})\}'),
    "in_quotes": re.compile(r'^[\'"][^\'"]*[\'"]$'),
    "copyright": re.compile(r'(^©[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9]+$)|(^[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9]+©$)'),
    "registered": re.compile(r'(^®[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9]+$)|(^[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9]+®$)'),
    "trade_mark": re.compile(r'(^™[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9]+$)|(^[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9]+™$)'),
    "bullet_list": re.compile(r'^•[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9]+$'),
    "three_or_more": re.compile(r'^([{}])\1{{2,}}$'.format(re.escape(string.punctuation))),
    "roman_number": re.compile(r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?$'),
    "apostrophed": re.compile(r"^([a-zA-ZıiİüÜçÇöÖşŞğĞ]+)'([a-zA-ZıiİüÜçÇöÖşŞğĞ]+)$"),
    "currency": re.compile(rf"^(?:[{re.escape(''.join(LocalData.currency_symbols()))}]\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?|\d{{1,3}}(?:[.,]\d{{3}})*([.,]\d+)?[{re.escape(''.join(LocalData.currency_symbols()))}])$"),
    "full_url": re.compile(r'^((http|https)\:\/\/)[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F\.\/\?\:@\-=#]+\.([a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F\&\/\?\:@\-=#])+'),
    "web_url": re.compile(r'^((www)\.)[a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F\.\/\?\:@\-=#]+\.([a-zA-ZıiİüÜçÇöÖşŞğĞ0-9_\uFE0F\&\/\?\:@\-=#])+'),
    "num_char_sequence": re.compile(r'\d+[\w\s]*'),
}

exception_list = ["(!)", "..."]

MATH_OPERATORS = {'+', '-', '*', '/', '%', '^', '**', '=', '!=', '==', '>', '<', '>=', '<=', '+=', '-=', '*=', '/=',
                  '%=', '√', '∑', 'π', '∞', '∩', '∪', '⊆', '⊂', '∈', '∉', '∧', '∨', '¬', '|', '!'}


def check_regex(word, pattern):
    # print(f"Checking {pattern} for word: {word}")
    return word if REGEX_PATTERNS[pattern].search(CharFix.fix(word)) else None


def punc_count(word: str) -> int:
    return sum(1 for char in word if char in puncs)


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

    # Regex Based Tokens
    # These functions get the input token, checks against to regular expressions defined above and
    # return word, tag as tuple

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
    def is_numbered_title(word: str) -> list:
        # Check if the word matches the "numbered_title" regex pattern
        result = check_regex(word, "numbered_title")
        if result:
            # Extract the numbered title using regex
            match = re.match(r'^\((\d{1,2})\)|^\[(\d{1,2})]|^{(\d{1,2})}', word)
            if match:
                # Get the numbered part (e.g., `(12)`, `[6]`, `{3}`)
                numbered_title = match.group(0)
                # Get the remaining text after the numbered title
                rest = word[len(numbered_title):]

                # Create the result list with the numbered title token
                tokens = [(numbered_title, "Numbered_Title")]

                # Process the remaining text if it exists
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
    def is_date_range(word: str) -> list:
        result = check_regex(word, "date_range") or check_regex(word, "year_range")
        if result:
            return [(result, "Date_Range")] if result else None

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
        return [(word, "Emoticon")] if word in LocalData.emoticons() else None

    # Multi-Unit Tokens
    @staticmethod
    def is_multiple_smiley(word: str) -> list:
        if SmileyParser.consecutive_smiley(word) and not str(word[0:-1]).isalnum():
            smiley_tokens = SmileyParser.smiley_tokenize(word).split("\n")
            smiley_list = [(smiley, "Smiley") for smiley in smiley_tokens]
            return smiley_list
        return None

    @staticmethod
    def is_multiple_smiley_in(word: str) -> list:
        if SmileyParser.consecutive_smiley(word) and any(char.isalnum() for char in word):
            for i, char in enumerate(word):
                if char in puncs:
                    initial_part = word[:i]
                    smileys = word[i:]
                    processed_word = TokenProcessor.process_token(initial_part)
                    if isinstance(processed_word, tuple):
                        processed_word = [processed_word]
                    smiley_tokens = SmileyParser.smiley_tokenize(smileys).split("\n")
                    smiley_list = [(smiley, "Smiley") for smiley in smiley_tokens]
                    return processed_word + smiley_list
        return None

    @staticmethod
    def is_multiple_emoticon(word):
        return (word, "Multiple_Emoticon") if EmoticonParser.emoticon_count(word) >= 2 else None

    @staticmethod
    def is_number(word: str) -> list:
        # Check if the entire word is a number
        if word.isdigit():
            return [(word, "Number")]

        if PuncMatcher.punc_count(word) == 1 and word.endswith("."):
            if all(char.isdigit() for char in word[:-1]):
                return [(word, "Ordinal_Number")]

        if PuncMatcher.punc_count(word) == 1 and ("," in word or "." in word):
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
            # Process the main part of the word
            if main_word:
                processed_main_word = TokenProcessor.process_token(main_word)
                if isinstance(processed_main_word, tuple):
                    tokens.append(processed_main_word)
                else:
                    tokens.extend(processed_main_word)

            # Process each punctuation mark in the trailing punctuation separately
            for char in trailing_punc:
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
    TokenPreProcess.is_hour_suffix,
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
