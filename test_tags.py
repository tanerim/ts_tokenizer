from ts_tokenizer.char_fix import CharFix

import sys

f = open(sys.argv[1]).read().split('\n')

for line in f:
    print(CharFix.fix(line))