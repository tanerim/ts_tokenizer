"""
ts-tokenizer
tanersezerr@gmail.com
"""
import sys
import argparse
import multiprocessing
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from ts_tokenizer.token_handler import TokenProcessor


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
        return parser.parse_args()

    @staticmethod
    def tokenize_line(line, return_format):
        """
        Tokenizes a single line and returns it in the specified format.
        """
        processed_tokens = [TokenProcessor.process_token(token) for token in line.split()]

        if return_format == 'tokenized':
            return '\n'.join([token[0] for token in processed_tokens])
        elif return_format == 'tagged':
            return '\n'.join([f"{token[0]}\t{token[1]}" for token in processed_tokens])
        elif return_format == 'lines':
            return ' '.join([token[0] for token in processed_tokens])
        elif return_format == 'tagged_lines':
            return ' '.join([str((token[0], token[1])) for token in processed_tokens])

    @staticmethod
    def ts_tokenize():
        """
        Main function to tokenize text from a file or command-line input.
        """
        args = TSTokenizer.parse_arguments()
        num_workers = max(1, multiprocessing.cpu_count() - 1)  # Ensure at least 1 worker

        if args.word:
            # Process word input from the command-line argument
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
                    futures = []
                    for line in in_file:
                        line = line.strip()
                        futures.append(executor.submit(TSTokenizer.tokenize_line, line, args.output))

                        if len(futures) >= num_workers:
                            for future in futures:
                                print(future.result())
                                if pbar:
                                    pbar.update(1)
                            futures.clear()

                    for future in futures:
                        print(future.result())
                        if pbar:
                            pbar.update(1)

                if pbar:
                    pbar.close()


if __name__ == "__main__":
    TSTokenizer.ts_tokenize()
