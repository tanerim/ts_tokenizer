from ts_tokenizer.token_handler import TokenProcessor
import re
import string

puncs = re.escape(string.punctuation)
extra_puncs = ["–", "°", "—", "(", ")"]
puncs += re.escape(''.join(extra_puncs))

class oov_parser:
    def __init__(self):
        pass

    @staticmethod
    def isp_parser(word: str) -> tuple:
        if word[0] in puncs:
            return (word[0], "Punc"), TokenProcessor.process_token(word[1:])


word = "!yeniden,eski"

print(oov_parser.isp_parser(word))


def is_isp(word: str) -> list:
    if word[0] in puncs:
        initial_punc = word[0]
        processed_word = TokenProcessor.process_token(initial_punc)
        if isinstance(processed_word, tuple):
            return (word[0], "Punc"), TokenProcessor.process_token(word[1:])

    elif len(word) > 1 and word[0] in puncs and all(char not in puncs for char in word[1:]):
        initial_punc = word[0]
        remaining_word = word[1:]
        processed_word = TokenProcessor.process_token(remaining_word)
        if isinstance(processed_word, tuple):
            processed_word = [processed_word]