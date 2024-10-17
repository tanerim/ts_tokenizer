"""
ts-tokenizer Command-Line Interface
Author: tanersezerr@gmail.com
"""

import sys
import argparse
from ts_tokenizer.tokenizer import TSTokenizer

def main():
    parser = argparse.ArgumentParser(description="ts-tokenizer")
    parser.add_argument(
        'filename',
        nargs='?',
        help="Name of the file to process (optional if input is piped)"
    )
    parser.add_argument(
        '-o', '--output',
        choices=['tokenized', 'lines', 'tagged', 'tagged_lines'],
        default='tokenized',
        help="Specify the output format"
    )
    parser.add_argument('-w', '--word', action='store_true', help="Enable CLI input mode")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode")
    parser.add_argument('-j', '--jobs', type=int, help="Number of parallel workers")

    args = parser.parse_args()

    if not sys.stdin.isatty():  # Piped input detected
        input_text = sys.stdin.read().strip()
        if not input_text:
            print("Error: No input received from stdin.", file=sys.stderr)
            sys.exit(1)

        # Tokenize the input text from stdin
        try:
            TSTokenizer.ts_tokenize(input_text=input_text, output_format=args.output)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.filename:
        try:
            TSTokenizer.ts_tokenize(filename=args.filename, output_format=args.output)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: ts-tokenizer <filename> or pipe input via stdin (e.g., echo 'text' | ts-tokenizer)")
        sys.exit(1)


if __name__ == '__main__':
    main()
