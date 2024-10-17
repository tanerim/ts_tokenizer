import sys
import argparse
import multiprocessing
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from ts_tokenizer.token_handler import TokenProcessor, TokenPreProcess
from ts_tokenizer.char_fix import CharFix

# Tokenizer class definition
class TSTokenizer:

    @staticmethod
    def parse_arguments():
        """
        Parses command-line arguments.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-o", "--output", choices=["tokenized", "lines", "tagged", "tagged_lines"], default="tokenized",
            help="Specify the output format"
        )
        parser.add_argument("filename", nargs='?', help="Name of the file to process (optional if input is piped)")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
        parser.add_argument("-j", "--jobs", type=int, help="Number of parallel workers", default=multiprocessing.cpu_count() - 1)
        return parser.parse_args()

    @staticmethod
    def tokenize_line(line, return_format):
        # First check if the line is an XML tag
        xml_tag = TokenPreProcess.is_xml(line)
        if xml_tag:
            # If the return format is tagged, output it as a tagged XML tag
            if return_format == 'tagged':
                return "\t".join(xml_tag)  # Return as XML_Tag with tag
            else:
                return line  # Just return the original line (XML tag) unchanged

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
            return '\n'.join([token[0] for token in flat_tokens])
        elif return_format == 'tagged':
            return '\n'.join([f"{token[0]}\t{token[1]}" for token in flat_tokens])
        elif return_format == 'lines':
            return [token[0] for token in flat_tokens]
        elif return_format == 'tagged_lines':
            return [(token[0], token[1]) for token in flat_tokens]  # Returns a list of tuples

    @staticmethod
    def ts_tokenize(input_text=None, filename=None, output_format='tokenized'):
        args = TSTokenizer.parse_arguments()

        num_workers = args.jobs

        # If input is provided via stdin, process it directly
        if input_text is not None:  # Stdin input is passed here
            sys.exit(0)

        # If no piped input, process in word or file mode
        if filename:
            with open(filename, encoding='utf-8') as in_file:
                if args.verbose:
                    total_lines = sum(1 for _ in in_file)
                    in_file.seek(0)
                    pbar = tqdm(total=total_lines, desc="Processing File")
                else:
                    pbar = None

                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    batch_size = 100
                    batch = []

                    for line in in_file:
                        print(f"Processing line: {line.strip()}")
                        if not TokenPreProcess.is_xml(line):
                            line = CharFix.fix(line.strip())
                        else:
                            line = CharFix.fix(line)

                        if line:
                            batch.append(line)

                        if len(batch) >= batch_size:
                            futures = [executor.submit(TSTokenizer.tokenize_line, line, output_format) for line in batch]
                            for future in futures:
                                print(future.result())
                            batch = []

                        if pbar:
                            pbar.update(batch_size)

                    if batch:
                        futures = [executor.submit(TSTokenizer.tokenize_line, line, output_format) for line in batch]
                        for future in futures:
                            print(future.result())
                        if pbar:
                            pbar.update(len(batch))

                if pbar:
                    pbar.close()


if __name__ == "__main__":
    args = TSTokenizer.parse_arguments()
    TSTokenizer.ts_tokenize(filename=args.filename, output_format=args.output)

