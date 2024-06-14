import sys
from ts_tokenizer.token_check import TokenCheck

def process_word(word):
    token_candidates = TokenCheck.token_tagger(word, output='all', output_format='string')
    return token_candidates

def main():
    # Determine the number of available cores
    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        lines = file.read().strip().splitlines()
        for word in lines:
            print(process_word(word))


if __name__ == '__main__':
    main()
