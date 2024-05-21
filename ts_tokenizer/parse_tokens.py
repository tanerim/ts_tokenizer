import re
import string
from .data import LocalData
from .token_preprocess import TokenCheck
from .punctuation_process import PuncMatcher


FMP_exception_list = ["(!)", "...", "!!!"]


class ParseTokens:
    @classmethod
    def are_consecutive_chars(cls, chars):
        if len(chars) <= 1:
            return True
        for i in range(1, len(chars)):
            if chars[i] != chars[i - 1] + 1:
                return False
        return True

    @classmethod
    def split_punctuation_and_chars(cls, word):
        patterns = ["...", "(!)", "!!!"] + list(LocalData.smileys())
        pattern_regex = '|'.join(map(re.escape, patterns))
        tokens = re.split('(' + pattern_regex + ')', word)
        return [token for token in tokens if token]

    @classmethod
    def tokenize_initial_quote(cls, word):
        word_list = list(word)
        index_list = [0, len(word)]
        for index in index_list:
            if index < len(word):
                word_list[index] = '\n' + word_list[index] + '\n'
        return ''.join(word_list).lstrip().rstrip()

    @classmethod
    def tokenize_in_quotes(cls, word):
        word_list = list(word)
        index_list = [0, len(word) - 1]
        for index in index_list:
            if index < len(word):
                word_list[index] = '\n' + word_list[index] + '\n'
        return ''.join(word_list).lstrip().rstrip()

    @classmethod
    def tokenize_ISP(cls, word):
        if word and word[0] in string.punctuation:
            return word[0] + '\n' + word[1:]
        return word

    @classmethod
    def tokenize_IMP(cls, word):
        word_list = list(word)
        index = 0
        if any(smiley in word for smiley in LocalData.smileys()):
            return '\n'.join(cls.split_punctuation_and_chars(word))
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
    def tokenize_FSP(cls, word):
        if word and word[-1] in string.punctuation:
            return word[:-1] + '\n' + word[-1]
        return word

    @classmethod
    def tokenize_MSP(cls, word):
        word_list = list(word)
        index_list = [i for i, char in enumerate(word) if char in string.punctuation]
        for index in index_list:
            if 0 <= index < len(word):
                word_list[index] = '\n' + word_list[index] + '\n'
        return ''.join(word_list).strip()

    @classmethod
    def tokenize_FMP(cls, word):
        word_list = list(word)
        PuncCount = PuncMatcher.punc_count(word)
        index_list = [len(word) - PuncCount]

        if any(smiley in word for smiley in LocalData.smileys()):
            return '\n'.join(cls.split_punctuation_and_chars(word))
        else:
            for exception in FMP_exception_list:
                if exception in word:
                    parts = [p for p in word.split(exception) if p]  # Avoid empty strings
                    return '\n'.join(parts + [exception] if parts else [exception])

            if PuncCount != len(word):  # Check if entire word is not punctuation
                for index in index_list:
                    if 0 < index < len(word):  # Avoid inserting newline at start
                        word_list[index] = '\n' + word_list[index]

            return ''.join(word_list).strip()

    @classmethod
    def tokenize_complex_punc(cls, word):
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
    def tokenize_in_parenthesis(cls, word):
        if word in FMP_exception_list:
            return word
        elif word.startswith("(!)"):
            return ParseTokens.tokenize_FSP(word)
        else:
            word_list = list(word)
            index_list = [0, len(word) - 1]
            for index in index_list:
                if index < len(word):
                    word_list[index] = '\n' + word_list[index] + '\n'
            return ''.join(word_list).lstrip().rstrip()

    @classmethod
    def tokenize_mishyphenated(cls, word):
        word = word.replace("-", "")
        return word

    @classmethod
    def tokenize_hour(cls, word):
        if TokenCheck.check_regex(word, "hour"):
            return word

    @classmethod
    def tokenize_date(cls, word):
        if word[-1] in string.punctuation and word[-2:] != "..":
            tokenized_date = ''.join((word[0:-1], "\n", word[-1])).lstrip().rstrip()
            return tokenized_date
        else:
            return word
