import re
import string

puncs = re.escape(string.punctuation)
PuncPattern = r'^(?P<initial>[%s]*)(?P<word>.*?)(?P<final>[%s]*)$' % (puncs, puncs)

class PuncMatcher:

    @classmethod
    def punc_count(cls, word):
        return sum(1 for char in word if char in string.punctuation)

    @classmethod
    def punc_pos(cls, word):
        return [i for i, char in enumerate(word) if char in string.punctuation]

    @classmethod
    def find_punctuation(cls, word):
        match = re.match(PuncPattern, word)
        if not match:
            return None

        initial_punc = match.group('initial')
        final_punc = match.group('final')

        if len(initial_punc) == 1 and not re.match(r'^[%s]+$' % puncs, final_punc):
            return "ISP"  # ==> "Initial_Single_Punc"

        elif len(final_punc) == 1 and not re.match(r'^[%s]+$' % puncs, initial_punc):
            return "FSP"  # ==> "Final_Single_Punc"

        elif len(initial_punc) >= 1 and len(final_punc) >= 1:
            return "MSP"  # ==> Multi_Side_Punc

        elif len(initial_punc) >= 2 and not re.match(r'^[%s]+$' % puncs, final_punc):
            return "IMP"  # ==> "Initial_Multi_Punc"

        elif len(final_punc) >= 2 and not re.match(r'^[%s]+$' % puncs, initial_punc):
            return "FMP"  # ==> "Final_Multi_Punc"


    @classmethod
    def inner_punctuation(cls, word):
        match = re.match(PuncPattern, word)
        if not match:
            return None
        inner_puncs = re.findall(r'(?<=\w)[^\s\w-]+(?=\w)', word)
        if inner_puncs:  # Check for inner punctuations
            return "Inner_Punc"  # ==> "Inner_Punc"


class PuncTagCheck:

    @classmethod
    def punc_tag_check(cls, word):
        punc_count = PuncMatcher.punc_count(word)
        punc_loc = PuncMatcher.punc_pos(word)
        complex_punc = PuncMatcher.find_punctuation(word)
        inner_punc = PuncMatcher.inner_punctuation(word)
        s_word = ""

        if complex_punc and inner_punc:
            return "Complex_Punc", word, punc_count, punc_loc

        elif inner_punc:
            return inner_punc, word, punc_count, punc_loc

        elif complex_punc:
            if complex_punc == "MSP":
                s_word = "MSP", word[0], word[1:-1], word[-1]
            elif complex_punc == "ISP":
                s_word = word[0], word[1:]
            elif complex_punc == "FSP":
                s_word = "FSP", word[0:-1], word[-1]
            elif complex_punc == "FMP":
                p_start = punc_loc[0]
                s_word = word[0:p_start], word[p_start:]
            elif complex_punc == "IMP":
                p_end = punc_loc[-1] + 1
                s_word = word[0:p_end], word[p_end:]
            return complex_punc, word, s_word, punc_count, punc_loc

        else:
            return word, punc_count, punc_loc,
