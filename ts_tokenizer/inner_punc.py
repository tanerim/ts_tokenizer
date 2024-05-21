import re
import string
num_suffix = ["ıncı", "inci", "üncü", "uncu"]


class InnerPuncParser:
    def __init__(self):
        self.puncs = re.escape(string.punctuation)
        self.pattern = r'^(?P<initial>[%s]*)(?P<word>.*?)(?P<final>[%s]*)$' % (self.puncs, self.puncs)

    @classmethod
    def ord_number(cls, word):
        if "'" in word:
            word_parts = word.split("'")
            if word_parts[0].isdigit() and word_parts[1] in num_suffix:
                return word, "Ord_Number"

    @classmethod
    def tokenize_Inner_Punc(cls, word):
        if word.count("'") == 1 and not word.startswith("'") and not word.endswith("'"):
            return word
        # Find the index of each punctuation character in the word
        index_list = [i for i, char in enumerate(word) if char in string.punctuation]
        # Initialize an empty string to store the result
        result = ""
        # Initialize the start index for slicing
        start = 0
        for index in index_list:
            # Append the substring from start to index, and then append a newline
            result += word[start:index] + '\n'
            # Append the punctuation and another newline
            result += word[index] + '\n'
            # Update the start index for the next slice
            start = index + 1
        # Append the remaining substring after the last index
        result += word[start:]
        return result.strip()
