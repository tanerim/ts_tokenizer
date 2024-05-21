"""
Tokenizer for Turkish text
Taner Sezer
"""
import re
import string
import argparse
import multiprocessing
from tqdm import tqdm
from ts_tokenizer.parse_tokens import ParseTokens
from ts_tokenizer.token_preprocess import TokenPreProcess
from ts_tokenizer.emoticon_check import EmoticonParser
from ts_tokenizer.smiley_check import SmileyParser
from ts_tokenizer.inner_punc import InnerPuncParser
from ts_tokenizer.punctuation_process import PuncTagCheck
from concurrent.futures import ThreadPoolExecutor

tokenization_functions = {
    "Initial_Quote": ParseTokens.tokenize_initial_quote,
    "ISP": ParseTokens.tokenize_ISP,
    "FSP": ParseTokens.tokenize_FSP,
    "MSP": ParseTokens.tokenize_MSP,
    "FMP": ParseTokens.tokenize_FMP,
    "IMP": ParseTokens.tokenize_IMP,
    "In_Parenthesis": ParseTokens.tokenize_in_parenthesis,
    "In_Quotes": ParseTokens.tokenize_in_quotes,
    "Complex_Punc": ParseTokens.tokenize_complex_punc,
    "Multiple_Emoticon": EmoticonParser.emoticon_tokenize,
    "Multiple_Smiley": SmileyParser.smiley_tokenize,
    "Mis_Hyphenated": ParseTokens.tokenize_mishyphenated,
    "Inner_Punc": InnerPuncParser.tokenize_Inner_Punc,
    "Hour": ParseTokens.tokenize_hour,
    "Date": ParseTokens.tokenize_date
}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=["tokenized", "lines", "tagged", "details"],
                        default="tokenized", help="specify how to print the items")
    parser.add_argument("filename", help="the name of the file to process")
    parser.add_argument("--color", "-c", action="store_true", help="enable colored output")
    return parser.parse_args()


def details(in_word, fixed_in_cand, tag):
    if tag == "OOV" and not any(c in string.punctuation for c in in_word if c != "-"):
        pre_token = PuncTagCheck.punc_tag_check(fixed_in_cand)
        return in_word, fixed_in_cand, pre_token
    elif tag == "OOV" and any(char in string.punctuation for char in fixed_in_cand):
        pre_token = PuncTagCheck.punc_tag_check(fixed_in_cand)
        return in_word, fixed_in_cand, pre_token
    elif tag == "OOV" and EmoticonParser.emoticon_count(in_word) >= 2:
        return in_word, fixed_in_cand, "Multiple_Emoticon"
    elif tag == "OOV":
        return in_word, fixed_in_cand, tag
    else:
        return in_word, fixed_in_cand, tag


def tagged(in_word, fixed_in_cand, tag):
    if tag == "OOV" and any(char in string.punctuation for char in fixed_in_cand):
        return in_word, fixed_in_cand, PuncTagCheck.punc_tag_check(fixed_in_cand)[0]
    elif tag == "OOV" and EmoticonParser.emoticon_count(fixed_in_cand) >= 2:
        return in_word, fixed_in_cand, tag
    else:
        return in_word, fixed_in_cand, tag


# noinspection PyArgumentList
def tokenized(in_word, fixed_in_cand, tag):
    pre_token = tagged(in_word, fixed_in_cand, tag)
    tag = pre_token[2]
    if tag in tokenization_functions:
        return tokenization_functions[tag](fixed_in_cand)
    elif tag == "OOV":
        if fixed_in_cand and (fixed_in_cand[0] in string.punctuation or fixed_in_cand[-1] in string.punctuation):
            if tag in tokenization_functions and tag != "Inner_Punc":
                return tokenization_functions[tag](fixed_in_cand)
            return InnerPuncParser.tokenize_Inner_Punc(fixed_in_cand)
        elif EmoticonParser.emoticon_count(fixed_in_cand) >= 2 and tag != "Inner_Punc":
            tokenized_emoticon = EmoticonParser.emoticon_tokenize(fixed_in_cand)
            return tokenization_functions.get(tokenized_emoticon, fixed_in_cand)
        else:
            return fixed_in_cand
    else:
        return fixed_in_cand


def process_tokens(args, word):
    result = TokenPreProcess.token_tagger(word)
    in_word, fixed_in_cand, tag = result
    if args.output == "tagged":
        return tagged(in_word, fixed_in_cand, tag)
    elif args.output == "details":
        return details(in_word, fixed_in_cand, tag)
    elif args.output == "tokenized":
        return tokenized(in_word, fixed_in_cand, tag)


def main():
    args = parse_arguments()
    num_workers = multiprocessing.cpu_count() - 1

    with open(args.filename, encoding='utf-8') as in_file:
        lines = in_file.readlines()
        total_lines = len(lines)
        pbar = tqdm(total=total_lines, desc="Processing File")

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            for line in lines:
                pbar.update(1)  # Update progress bar for each line
                if re.match(r'^\s*(<|</).*>\s*$', line):
                    continue  # Skip lines matching the regex
                else:
                    # Process each word in the line individually
                    words = line.split()
                    results = list(executor.map(lambda w: process_tokens(args, w), words))
                    for token in results:
                        if args.output == "tagged":
                            print("\t".join(token))
                        else:
                            print(token)
        pbar.close()


if __name__ == '__main__':
    main()
