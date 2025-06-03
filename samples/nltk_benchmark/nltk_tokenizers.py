# -------------------------------------------|
# Use Python NLTK Tokenizers to create a     |
# Benchmark for comparison - ts -            |
# -------------------------------------------|
# w_tokenized_tokens = word_tokenize(text)   |
# w_punct_tokens = wordpunct_tokenize(text)  |
# -------------------------------------------|
# wht_spc_tokenizer = WhitespaceTokenizer()  |
# tokenizer = TreebankWordTokenizer()        |
# -------------------------------------------|

import argparse
import multiprocessing
from tqdm import tqdm
from nltk.tokenize import word_tokenize, wordpunct_tokenize, WhitespaceTokenizer, TreebankWordTokenizer


parser = argparse.ArgumentParser(description='Tokenization with different built-in methods of NLTK.')
parser.add_argument('filename', type=str, help='Input file')
parser.add_argument('--tok', type=str, choices=['wt', 'wpt', 'ws', 'tb'], default='ws',
                    help='Tokenization methods are as follows'
                         '(wt: word_tokenize,'
                         'pt: wordpunct_tokenize,'
                         'ws: WhitespaceTokenizer,'
                         'tb: TreebankWordTokenizer)')
args = parser.parse_args()

with open(args.filename, encoding='utf-8') as f:
    in_file = f.read().split("\n")


if args.tok == 'wt':
    tokenizer = word_tokenize
elif args.tok == 'wpt':
    tokenizer = wordpunct_tokenize
elif args.tok == 'ws':
    tokenizer = WhitespaceTokenizer().tokenize
elif args.tok == 'tb':
    tokenizer = TreebankWordTokenizer().tokenize


# Function to process each line using the chosen tokenizer
def process_line(line):
    tokens = tokenizer(line)
    return tokens


# Main processing using multiprocessing
def main():
    try:
        with open(args.filename, encoding='utf-8') as file:
            infile = file.read().split("\n")
        num_workers = multiprocessing.cpu_count() - 1
        with multiprocessing.Pool(processes=num_workers) as pool:
            results = pool.imap(process_line, infile, chunksize=100)
            for tokens in tqdm(results, total=len(infile), desc="Processing lines", unit="lines"):
                for token in tokens:
                    print(token)
    except FileNotFoundError:
        print(f"Error: File {args.filename} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
