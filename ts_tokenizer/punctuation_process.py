import re
import string
from typing import Union, Optional
from .char_fix import CharFix
from .data import LocalData
from .date_check import DateCheck


puncs = re.escape(string.punctuation)

extra_puncs = ["–", "'", "°", "—"]
for p in extra_puncs:
    puncs = puncs + p

PuncPattern = r'^(?P<initial>[%s]*)(?P<word>.*?)(?P<final>[%s]*)$' % (puncs, puncs)


class PuncMatcher:

    @classmethod
    def punc_count(cls, word: str) -> int:
        return sum(1 for char in word if char in string.punctuation)

    @classmethod
    def punc_pos(cls, word: str) -> list:
        return [i for i, char in enumerate(word) if char in string.punctuation]

    @classmethod
    def find_punctuation(cls, word: str) -> Optional[Union[bool, str]]:
        match = re.match(PuncPattern, word)
        if not match:
            return None

        initial_punc = match.group('initial')
        final_punc = match.group('final')

        if initial_punc and final_punc:
            if len(initial_punc) == 1 and len(final_punc) == 1:
                return "MSSP"  # Multi-Side Single Punctuation
            else:
                return "MSP"  # Multi-Side Punctuation
        elif initial_punc:
            if len(initial_punc) == 1:
                return "ISP"  # Initial_Single_Punc
            else:
                return "IMP"  # Initial_Multi_Punc
        elif final_punc:
            if len(final_punc) == 1 and PuncMatcher.punc_count(word) == 1:
                return "FSP"  # Final_Single_Punc
            else:
                return "FMP"  # Final_Multi_Punc
        return None

    @classmethod
    def inner_punctuation(cls, word: str) -> Optional[Union[bool, str]]:
        # Count the punctuations in the word
        punc_count = PuncMatcher.punc_count(word)

        if PuncMatcher.hyphen_in(word):
            return PuncMatcher.hyphenated(word)

        # Check if the word has no punctuation at the start and end, but punctuation inside
        if punc_count == 1 and word[0] not in string.punctuation and word[-1] not in string.punctuation and "-" not in word:
            return "Inner_Single_Punc"

        # Check if there are multiple punctuations inside the word and no punctuation at the start or end
        elif punc_count >= 2:
            # Check if there are punctuations within the middle of the word
            inner_punctuation = any(char in string.punctuation for char in word[1:-1])
            # Date range (assumed implementation of is_date to check valid date)
            parts = word.split("-")
            if all(DateCheck.is_date(part) for part in parts):
                return "Date_Range"
            #else:
            if inner_punctuation:
                return "Inner_Multiple_Punc"
        elif "°" in word:
            if word.count("°") == 1 and word[-1] == "°":
                return "Celcius"
            elif word.count("°") == 2 and word[-1] == "°":
                return "Celcius_Range"
            else:
                return "Coordinate"

        return None

    @classmethod
    def apostrophed(cls, word: str) -> Optional[Union[bool, str]]:
        match = re.match(r"\b\w+'[a-zA-Z]+\b", word)
        if match:
            punc_positions = cls.punc_pos(word)
            if cls.punc_count(word) == 1 and punc_positions and "'" in word and word[-1] != "'":
                return "apostrophes_in"
        return None

    @staticmethod
    def hyphenated(word):
        # Check for hyphenated words where both parts exist in the word list
        if ("-" in word and word.count("-") == 1 and word[0] != "-" and word[-1] != "-"
                and not any(c in string.punctuation for c in word if c != "-")):
            parts = word.split("-")
            if all(CharFix.tr_lowercase(part) in LocalData.word_list() for part in parts):
                return "Hyphenated"  # Valid hyphenated word

    @staticmethod
    def hyphen_in(word):
        parts = word.split("-")
        cleaned_word = CharFix.fix(word)
        hyphen_count = word.count("-")

        if "-" not in word:
            return None

        if hyphen_count >= 2:

            if word[0] != "-" and word[-1] != "-":
                return "Multi_Hyphenated"

        elif hyphen_count == 1:
            if all(part.isdigit() for part in parts):
                tag = "Year_Range" if all(len(part) == 4 for part in parts) else "Numeric_Hyphenated"
                return tag

            elif PuncMatcher.hyphenated(word):
                return "Hyphenated"

            elif word[0] == "-" and word[-1] != "-":
                # You could handle specific cases, like if you want to treat these words differently
                return "Hyphen_Initial"

            elif word[0] != "-" and word[-1] == "-":
                # You could handle specific cases, like if you want to treat these words differently
                return "Hyphen_Final"

            elif any(part.isdigit() or any(c.isalpha() for c in part) for part in parts):
                return "Single_Hyphenated"

        elif word.count("-") >= 2:
            return word, cleaned_word, "Multi_Hyphens"

        return None


class PuncTagCheck:

    @classmethod
    def punc_tag_check(cls, word: str) -> tuple:
        word = CharFix.fix(word)
        punc_count = PuncMatcher.punc_count(word)
        punc_loc = PuncMatcher.punc_pos(word)
        hyphen_check = PuncMatcher.hyphen_in(word)
        inner_punc = PuncMatcher.inner_punctuation(word)
        apostrophe = PuncMatcher.apostrophed(word)
        complex_punc = PuncMatcher.find_punctuation(word)

        if hyphen_check:
            return PuncMatcher.hyphen_in(word), word, punc_count, punc_loc

        if apostrophe:
            return "Apostrophe", word, punc_count, punc_loc

        if complex_punc:
            s_word = ""
            if complex_punc == "MSSP":
                s_word = (word[0], word[1:-1], word[-1])
            elif complex_punc == "MSP":
                s_word = (word[0], word[1:-1], word[-1])
            elif complex_punc == "ISP":
                s_word = (word[0], word[1:])
            elif complex_punc == "FSP":
                s_word = ("FSP", word[0:-1], word[-1])
            elif complex_punc == "FMP":
                p_start = punc_loc[0]
                s_word = (word[0:p_start], word[p_start:])
            elif complex_punc == "IMP":
                p_end = punc_loc[-1] + 1
                s_word = (word[0:p_end], word[p_end:])
            return complex_punc, word, s_word, punc_count, punc_loc

        if inner_punc:
            return inner_punc, word, punc_count, punc_loc

        return word, punc_count, punc_loc
