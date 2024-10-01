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
    print(part_one, TokenProcessor.process_token(part_two))


print(isp_recursive(".yeni"))
