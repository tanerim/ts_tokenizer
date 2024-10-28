import sys
import multiprocessing
from tqdm import tqdm
import json
from concurrent.futures import ProcessPoolExecutor
from ts_tokenizer.token_handler import TokenProcessor, TokenPreProcess
from ts_tokenizer.char_fix import CharFix


def tokenize(line, return_format, output=False):
    """
    Tokenizes a single line and returns the result based on the specified return format.
    """
    try:
        # Strip whitespace and remove any invisible characters
        line = line.strip().replace('\u200b', '').replace('\ufeff', '')  # Remove zero-width spaces and BOM markers

        if not line:  # Skip processing if the line is empty or contains only invisible characters
            return None

        # First check if the line is an XML tag
        xml_tag = TokenPreProcess.is_xml(line)

        if xml_tag:
            if return_format == 'tagged':
                return json.dumps(xml_tag, ensure_ascii=False) if output else "\t".join(xml_tag)
            else:
                return line  # Return the original line (XML tag) unchanged

        # Proceed with tokenization if the line is not XML
        processed_tokens = [TokenProcessor.process_token(token) for token in line.split() if token]
        flat_tokens = []
        for token_list in processed_tokens:
            if isinstance(token_list, list):
                flat_tokens.extend(token_list)
            else:
                flat_tokens.append(token_list)

        # Handle output formats
        if return_format == 'tokenized':
            # Do not apply JSON formatting for 'tokenized'
            return '\n'.join([token[0] for token in flat_tokens])

        elif return_format == 'tagged':
            if output:
                return json.dumps([{"token": token[0], "tag": token[1]} for token in flat_tokens], ensure_ascii=False)
            return '\n'.join([f"{token[0]}\t{token[1]}" for token in flat_tokens])

        elif return_format == 'lines':
            if output:
                return json.dumps({"tokens": [token[0] for token in flat_tokens]}, ensure_ascii=False)
            return ' '.join([token[0] for token in flat_tokens])

        elif return_format == 'tagged_lines':
            if output:
                return json.dumps(
                    [{"token": token[0], "tag": token[1] if len(token) > 1 else None} for token in flat_tokens],
                    ensure_ascii=False)
            return [(token[0], token[1] if len(token) > 1 else None) for token in
                    flat_tokens]  # Return a list of tuples

    except (IndexError, TypeError):
        # Handle any string index out of range or type errors gracefully
        # print(f"Error processing line: {line}\nException: {e}", file=sys.stderr)
        return None  # Return None to indicate an error occurred


class TSTokenizer:

    @staticmethod
    def ts_tokenize(input_file=None, filename=None, output_format='tokenized', num_workers=None, verbose=False, output=False):
        if num_workers is None:
            num_workers = multiprocessing.cpu_count() - 1

        # Case 1: Handle piped input directly (input_text is provided)
        if input_file:
            for line in input_file.splitlines():
                result = tokenize(line, output_format, output)
                if result is not None:
                    print(result)
            return

        # Case 2: Handle file input (filename is provided)
        if filename:
            with open(filename, 'r', encoding='utf-8') as in_file:
                # If verbose mode is enabled, initialize progress bar
                if verbose:
                    total_lines = sum(1 for _ in in_file)
                    in_file.seek(0)
                    pbar = tqdm(total=total_lines, desc="Processing File")
                else:
                    pbar = None

                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    batch_size = 100
                    batch = []

                    # Process the file line by line
                    for line in in_file:
                        # Only strip spaces for non-XML tags and apply character fixes
                        if not TokenPreProcess.is_xml(line):
                            line = CharFix.fix(line.strip())  # Strip and fix characters for non-XML lines
                        else:
                            line = CharFix.fix(line)  # Apply CharFix without stripping spaces for XML tags

                        if line:  # Only process non-empty lines. Do not change
                            batch.append(line)

                        # When the batch size is reached, process the batch in parallel
                        if len(batch) >= batch_size:
                            futures = [executor.submit(tokenize, line, output_format, output) for line in batch]
                            for future in futures:
                                result = future.result()
                                if result is not None:
                                    print(result)
                            batch = []  # Clear batch after processing

                        # Update progress bar if verbose mode is enabled
                        if pbar:
                            pbar.update(min(len(batch), batch_size))

                    # Process remaining lines in the last batch
                    if batch:
                        futures = [executor.submit(tokenize, line, output_format, output) for line in batch]
                        for future in futures:
                            result = future.result()
                            if result is not None:
                                print(result)

                        # Update progress bar for the remaining lines
                        if pbar:
                            pbar.update(len(batch))

                # Close the progress bar if it was initialized
                if pbar:
                    pbar.close()


if __name__ == "__main__":
    import argparse
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
        '-j', '--json', action='store_true', help="Return the output as JSON")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode")
    parser.add_argument('-n', '--num-workers', type=int, help="Number of parallel workers", default=None)

    args = parser.parse_args()

    json_output = args.json  # Use the flag from args directly

    if not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
        if input_text:
            TSTokenizer.ts_tokenize(
                input_file=input_text,
                output_format=args.output,
                num_workers=args.num_workers,
                verbose=args.verbose,
                output=json_output  # Pass the correct json_output value
            )
        else:
            print("Error: No input received from stdin.", file=sys.stderr)
            sys.exit(1)
    elif args.filename:
        TSTokenizer.ts_tokenize(
            filename=args.filename,
            output_format=args.output,
            num_workers=args.num_workers,
            verbose=args.verbose,
            output=json_output  # Pass the correct json_output value
        )
    else:
        print("Usage: ts-tokenizer <filename> or pipe input via stdin (e.g., cat file.txt | ts-tokenizer)")
        sys.exit(1)
