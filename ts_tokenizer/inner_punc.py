import re
import string
from typing import Union, Optional

num_suffix = ["ıncı", "inci", "üncü", "uncu"]


class InnerPuncParser:
    def __init__(self):
        self.puncs = re.escape(string.punctuation)
        self.pattern = r'^(?P<initial>[%s]*)(?P<word>.*?)(?P<final>[%s]*)$' % (self.puncs, self.puncs)

    @classmethod
    def ord_number(cls, word: str) -> Optional[Union[bool, tuple]]:
        if "'" in word:
            word_parts = word.split("'")
            if word_parts[0].isdigit() and word_parts[1] in num_suffix:
                return word, "Ord_Number"
