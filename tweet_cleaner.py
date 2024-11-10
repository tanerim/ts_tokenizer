from ts_tokenizer.data import word_list
from ts_tokenizer.char_fix import CharFix
from ts_tokenizer.tokenizer import tokenize
from ts_tokenizer.token_handler import TokenPreProcess
import sys

f = open(sys.argv[1]).read().split("\n")


for w in f:
    y = TokenPreProcess.is_midsp(w)
    if y:
        print(f"{w} ==> {y}")
