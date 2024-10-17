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
        parser.add_argument("filename", help="Name of the file to process")
        parser.add_argument("-w", "--word", action="store_true", help="Enable CLI input mode")
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
    def ts_tokenize():
        args = TSTokenizer.parse_arguments()
        num_workers = args.jobs

        if args.word:
            word = sys.argv[-1]
            print(TSTokenizer.tokenize_line(word, args.output))
        else:
            # Process file input
            with open(args.filename, encoding='utf-8') as in_file:
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
                        # Only strip spaces for non-XML tags
                        if not TokenPreProcess.is_xml(line):
                            line = CharFix.fix(line.strip())  # Strip whitespace and fix characters for non-XML lines
                        else:
                            line = CharFix.fix(line)  # Just apply CharFix without stripping spaces for XML tags

                        if line:  # Only process non-empty lines
                            batch.append(line)

                        if len(batch) >= batch_size:
                            futures = [executor.submit(TSTokenizer.tokenize_line, line, args.output) for line in batch]
                            for future in futures:
                                print(future.result())
                            batch = []  # Clear batch after processing

                        if pbar:
                            pbar.update(batch_size)

                    # Process remaining lines in the last batch
                    if batch:
                        futures = [executor.submit(TSTokenizer.tokenize_line, line, args.output) for line in batch]
                        for future in futures:
                            print(future.result())
                        if pbar:
                            pbar.update(len(batch))

                if pbar:
                    pbar.close()


if __name__ == "__main__":
    TSTokenizer.ts_tokenize()
