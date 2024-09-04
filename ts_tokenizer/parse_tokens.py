import re
import string
from .data import LocalData
from .punctuation_process import PuncMatcher
from typing import Union, Optional


FMP_exception_list = ["(!)", "...", "!!!"]


class ParseTokens:
    @classmethod
    def are_consecutive_chars(cls, chars: str) -> bool:
        if len(chars) <= 1:
            return True
        for i in range(1, len(chars)):
            if chars[i] != chars[i - 1] + 1:
                return False
        return True

    @classmethod
    def split_punctuation_and_chars(cls, word: str) -> list:
        patterns = ["...", "(!)", "!!!"] + list(LocalData.smileys())
        pattern_regex = '|'.join(map(re.escape, patterns))
        tokens = re.split('(' + pattern_regex + ')', word)
        return [token for token in tokens if token]

    @classmethod
    def tokenize_initial_quote(cls, word: str) -> list:
        word_list = list(word)
        index_list = [0, len(word)]
        for index in index_list:
            if index < len(word):
                word_list[index] = '\n' + word_list[index] + '\n'
        return ''.join(word_list).lstrip().rstrip()

    @classmethod
    def tokenize_in_quotes(cls, word: str) -> list:
        word_list = list(word)
        index_list = [0, len(word) - 1]
        for index in index_list:
            if index < len(word):
                word_list[index] = '\n' + word_list[index] + '\n'
        return ''.join(word_list).lstrip().rstrip()

    @classmethod
    def tokenize_isp(cls, word: str) -> str:
        if word and word[0] in string.punctuation:
            return word[0] + '\n' + word[1:]
        return word

    @classmethod
    def tokenize_imp(cls, word: str) -> str:
        word_list = list(word)
        index = 0
        if any(smiley in word for smiley in LocalData.smileys()):
            return '\n'.join(cls.split_punctuation_and_chars(word))
        if word.startswith("(!)"):
            return "\n".join(("(!)", word[3:]))

        else:
            while index < len(word_list):
                if word_list[index] in string.punctuation:
                    index += 1
                    word_list.insert(index, '\n')
                    index += 1
                else:
                    break
        return ''.join(word_list).strip()

    @classmethod
    def tokenize_fsp(cls, word: str) -> str:
        if word and word[-1] in string.punctuation:
            return word[:-1] + '\n' + word[-1]
        return word

    @classmethod
    def tokenize_msp(cls, word: str) -> str:
        word_list = list(word)
        index_list = [i for i, char in enumerate(word) if char in string.punctuation]
        for index in index_list:
            if 0 <= index < len(word):
                word_list[index] = f"\n{word_list[index]}\n"
        return ''.join(word_list).strip()

    @classmethod
    def tokenize_fmp(cls, word: str) -> str:
        punc_count = PuncMatcher.punc_count(word)
        punc_positions = PuncMatcher.punc_pos(word)
        first_punc_pos = punc_positions[0]
        char_part = word[:first_punc_pos]
        punc_part = word[first_punc_pos:]

        if punc_part in LocalData.smileys():
            return f"{char_part}\n{punc_part}"
        elif punc_part in FMP_exception_list:
            return f"{char_part}\n{punc_part}"
        elif any(punc_part.startswith(exc) for exc in FMP_exception_list):
            return f"{char_part}\n" + "\n".join(cls.split_punctuation_and_chars(punc_part))
        elif len(punc_part) == punc_count:
            return f"{char_part}\n" + "\n".join(punc_part)

        # If the entire word is not punctuation
        if PuncMatcher.punc_count(word) != len(word):
            word_list = list(word)
            for index in punc_positions:
                if 0 < index < len(word):  # Avoid inserting newline at start
                    word_list[index] = '\n' + word_list[index]

            return ''.join(word_list).strip()

    @classmethod
    def tokenize_complex_punc(cls, word: str) -> str:
        # Exception case: one char + dot + one char + dot (e.g., "M.S.")
        if len(word) == 4 and all([word[0].isalpha(), word[1] == '.', word[2].isalpha(), word[3] == '.']):
            return word

        word_list = list(word)
        index_adjustment = 0
        for index in range(len(word)):
            if word[index] in string.punctuation and word[index] != "'":
                # Insert newline before and after the punctuation, adjusting index for the newly inserted characters
                word_list.insert(index + index_adjustment, '\n')
                index_adjustment += 1
                word_list.insert(index + index_adjustment + 1, '\n')
                index_adjustment += 1

        return ''.join(word_list).strip()

    @classmethod
    def tokenize_in_parenthesis(cls, word: str) -> str:
        if word in FMP_exception_list:
            return word
        elif word.startswith("(!)"):
            return ParseTokens.tokenize_fsp(word)
        else:
            word_list = list(word)
            index_list = [0, len(word) - 1]
            for index in index_list:
                if index < len(word):
                    word_list[index] = '\n' + word_list[index] + '\n'
            return ''.join(word_list).lstrip().rstrip()

    @classmethod
    def tokenize_mishyphenated(cls, word: str) -> str:
        word = word.replace("-", "")
        return word

    @classmethod
    def tokenize_inner_punc(cls, word: str) -> str:
        # Define exceptions
        exceptions = ["...", "(!)"]
        # If the word contains exactly one apostrophe not at the start or end
        if word.count("'") == 1 and not word.startswith("'") and not word.endswith("'"):
            return word

        # If the word contains exactly one punctuation character
        elif PuncMatcher.punc_count(word) == 1:
            # Get the position of the punctuation
            punc_pos = PuncMatcher.punc_pos(word)[0]
            # Split the word into three parts: before punctuation, punctuation, after punctuation
            first_part = word[:punc_pos]
            punc = word[punc_pos]
            second_part = word[punc_pos + 1:]
            # Return the parts separated by newlines
            return f"{first_part}\n{punc}\n{second_part}"

        elif PuncMatcher.punc_count(word) == 3:
            for exception in exceptions:
                if exception in word:
                    punc_pos = word.index(exception)
                    first_part = word[:punc_pos]
                    punc = exception
                    second_part = word[punc_pos + 3:]
                    return f"{first_part}\n{punc}\n{second_part}"

        # Default case: tokenize the word normally
        result = ""
        start = 0
        index_list = [i for i, char in enumerate(word) if char in string.punctuation]
        for index in index_list:
            result += word[start:index] + '\n'
            result += word[index] + '\n'
            start = index + 1
        result += word[start:]
        return result.strip().replace("\n\n", "\n")
