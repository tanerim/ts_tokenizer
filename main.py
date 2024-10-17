"""
Tokenizer for Turkish texts
tanersezerr@gmail.com
"""
import sys
from ts_tokenizer.tokenizer import TSTokenizer

def main():
    # If no arguments are provided, print usage
    if len(sys.argv) < 2:
        print("Usage: python main.py <args>")
        sys.exit(1)

    # Parse the arguments first, then call the tokenizer with the correct arguments
    args = TSTokenizer.parse_arguments()

    # Call the TSTokenizer method with the filename and output format
    TSTokenizer.ts_tokenize(filename=args.filename, output_format=args.output)

if __name__ == '__main__':
    main()
