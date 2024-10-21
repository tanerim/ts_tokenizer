import sys
import argparse
from ts_tokenizer.tokenizer import TSTokenizer

def main():
    parser = argparse.ArgumentParser(description="Tokenizer Script")
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
    parser.add_argument(
        '-s', '--string', action='store_true', default=True, help="Return the output as a string (default)"
    )
    parser.add_argument(
        '-j', '--json', action='store_true', help="Return the output as JSON"
    )
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode")
    parser.add_argument('-n', '--num-workers', type=int, help="Number of parallel workers", default=None)

    args = parser.parse_args()

    # Case 1: Piped input detected
    if not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
        if not input_text:
            print("Error: No input received from stdin.", file=sys.stderr)
            sys.exit(1)

        try:
            # Tokenize the input text from stdin
            TSTokenizer.ts_tokenize(input_file=input_text, output_format=args.output, num_workers=args.num_workers)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Case 2: Filename provided
    elif args.filename:
        try:
            TSTokenizer.ts_tokenize(filename=args.filename, output_format=args.output, num_workers=args.num_workers)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Case 3: No input provided
    else:
        print("Usage: ts-tokenizer <filename> or pipe input via stdin (e.g., cat file.txt | ts-tokenizer)")
        sys.exit(1)


if __name__ == '__main__':
    main()
