"""
Tokenizer for Turkish text - Taner Sezer
tanersezerr@gmail.com
"""
import sys
from ts_tokenizer.tokenizer import TSTokenizer


def extract_tokens(text):
    tokens = TSTokenizer.tokenize(text)
    return tokens

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <args>")
        sys.exit(1)

    # Call the TSTokenizer main method which handles argument parsing and processing
    TSTokenizer.ts_tokenize()


if __name__ == '__main__':
    main()
