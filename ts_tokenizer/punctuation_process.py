import re
import string
from typing import Union, Optional

puncs = re.escape(string.punctuation)
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
            return "MSP"  # Multi_Side_Punc
        elif len(initial_punc) == 1 and not final_punc:
            return "ISP"  # Initial_Single_Punc
        elif len(final_punc) == 1 and not initial_punc:
            return "FSP"  # Final_Single_Punc
        elif len(initial_punc) >= 2:
            return "IMP"  # Initial_Multi_Punc
        elif len(final_punc) >= 2:
            return "FMP"  # Final_Multi_Punc
        return None

    @classmethod
    def inner_punctuation(cls, word: str) -> Optional[Union[bool, str]]:
        match = re.match(PuncPattern, word)
        if not match:
            return False
        inner_puncs = re.findall(r'(?<=\w)[^\s\w-]+(?=\w)', word)
        if inner_puncs:
            return "Inner_Punc"
        return False

    @classmethod
    def apostrophed(cls, word: str) -> Optional[Union[bool, str]]:
        match = re.match(PuncPattern, word)
        if not match:
            return None
        punc_positions = cls.punc_pos(word)
        if cls.punc_count(word) == 1 and punc_positions and punc_positions[0] != 0 and "'" in word:
            return "apostrophes_in"
        return None


class PuncTagCheck:

    @classmethod
    def punc_tag_check(cls, word: str) -> tuple:
        punc_count = PuncMatcher.punc_count(word)
        punc_loc = PuncMatcher.punc_pos(word)
        apostrophe = PuncMatcher.apostrophed(word)
        complex_punc = PuncMatcher.find_punctuation(word)
        inner_punc = PuncMatcher.inner_punctuation(word)

        if apostrophe:
            return "Apostrophe", word, punc_count, punc_loc

        if complex_punc and inner_punc:
            return "Complex_Punc", word, punc_count, punc_loc

        if inner_punc:
            return inner_punc, word, punc_count, punc_loc

        if complex_punc:
            s_word = ""
            if complex_punc == "MSP":
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

        return word, punc_count, punc_loc
