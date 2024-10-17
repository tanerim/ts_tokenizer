"""
ts-tokenizer Command-Line Interface
Author: tanersezerr@gmail.com
"""

import sys
from ts_tokenizer.tokenizer import TSTokenizer

def main():
    # Check if input is piped via stdin
    if not sys.stdin.isatty():  # If input is coming from stdin (i.e., piped input)
        input_text = sys.stdin.read().strip()
        if not input_text:
            print("Error: No input received from stdin.")
            sys.exit(1)

        # Tokenize the input text from stdin
        try:
            TSTokenizer.ts_tokenize(input_text=input_text)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif len(sys.argv) < 2:
        print("Usage: ts-tokenizer <filename> or pipe input via stdin (e.g., echo 'text' | ts-tokenizer)")
        sys.exit(1)
    else:
        # Tokenize from the provided file
        try:
            TSTokenizer.ts_tokenize()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()
