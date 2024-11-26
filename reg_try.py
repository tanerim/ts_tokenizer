import re
import string
import sys
from ts_tokenizer.data import LocalData
from ts_tokenizer.char_fix import CharFix
from ts_tokenizer.token_handler import TokenProcessor, TokenPreProcess


word = "Mu¬Sun"

print(TokenPreProcess.is_one_char_fixable(word))


from ts_tokenizer.token_handler import TokenPreProcess

word = "ParÃ§a"

print(TokenProcessor.process_token(word))

from ts_tokenizer.tokenizer import tokenize

print(tokenize(word, output="list", return_format="tagged"))
