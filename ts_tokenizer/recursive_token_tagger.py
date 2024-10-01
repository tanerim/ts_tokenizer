import re
import string
from .token_processor import TokenProcessor

puncs = re.escape(string.punctuation)

extra_puncs = ["–", "'", "°", "—"]
for p in extra_puncs:
    puncs = puncs + p

PuncPattern = r'^(?P<initial>[%s]*)(?P<word>.*?)(?P<final>[%s]*)$' % (puncs, puncs)


def find_punctuation(word):
    match = re.match(PuncPattern, word)
    if not match:
        return None

    initial_punc = match.group('initial')
    final_punc = match.group('final')
    return initial_punc, final_punc


def isp_recursive(token):
    part_one = token[0]
    part_two = token[1:]
    print(part_one, part_two)


def mssp_recursive(token):
    tokens = []
    initial_punc = token[0]
    tokens.append((initial_punc, "Punc"))
    final_punc = token[-1]
    tokens.append((final_punc, "Punc"))
    token = token[1:-1]
    tokens.append((TokenProcessor.process_token(token)[0], TokenProcessor.process_token(token)[1]))
    return tokens


print(mssp_recursive(".yeni."))
