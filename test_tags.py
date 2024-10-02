from ts_tokenizer.token_handler import TokenPreProcess, TokenProcessor
import sys

f = open(sys.argv[1]).read().split('\n')

tokens = []
for line in f:
    if TokenPreProcess.is_xml(line):
        print("\t".join(TokenPreProcess.is_xml(line)))
        continue
    for word in line.split(' '):
        token = TokenProcessor.process_token(word)
        # print(f"{token[0]}\t{token[1]}")
        print("\t".join(token))
