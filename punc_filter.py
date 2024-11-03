import re
import string

PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]


sample = "Koca Ali… Koca Ali, be!.. İsteseymiş bir günde bitirirmiş (!) ama ne yazık ki vakti yokmuş (!)."


print(punctuation_filter(sample))
