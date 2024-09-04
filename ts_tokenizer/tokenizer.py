import sys
import argparse
import json
import string
from ts_tokenizer.token_check import TokenCheck
from ts_tokenizer.parse_tokens import ParseTokens
from ts_tokenizer.emoticon_check import EmoticonParser
from ts_tokenizer.inner_punc import InnerPuncParser
from ts_tokenizer.punctuation_process import PuncTagCheck
from ts_tokenizer.token_preprocess import TokenPreProcess
import re
import multiprocessing
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

tokenization_functions = {
    "Initial_Quote": ParseTokens.tokenize_initial_quote,
    "ISP": ParseTokens.tokenize_isp,
    "FSP": ParseTokens.tokenize_fsp,
    "MSP": ParseTokens.tokenize_msp,
    "FMP": ParseTokens.tokenize_fmp,
    "IMP": ParseTokens.tokenize_imp,
    "In_Parenthesis": ParseTokens.tokenize_in_parenthesis,
    "In_Quotes": ParseTokens.tokenize_in_quotes,
    "Complex_Punc": ParseTokens.tokenize_complex_punc,
    # "Multiple_Emoticon": EmoticonParser.emoticon_tokenize,
    # "Multiple_Smiley": SmileyParser.smiley_tokenize,
    "Mis_Hyphenated": ParseTokens.tokenize_mishyphenated,
    "Inner_Punc": ParseTokens.tokenize_inner_punc,
}


def tokenized(in_word, fixed_in_cand, tag):
    pre_token = tagged(in_word, fixed_in_cand, tag)
    tag = pre_token[2]

    # Check lexicon, exceptions, and English words
    if TokenPreProcess.is_in_lexicon(fixed_in_cand):
        return fixed_in_cand
    elif TokenPreProcess.is_in_exceptions(fixed_in_cand):
        return fixed_in_cand
    elif TokenPreProcess.is_in_eng_words(fixed_in_cand):
        return fixed_in_cand

    # Process based on the tag
    if tag in tokenization_functions:
        return tokenization_functions[tag](fixed_in_cand)
    elif tag == "OOV":
        if fixed_in_cand and (fixed_in_cand[0] in string.punctuation or fixed_in_cand[-1] in string.punctuation):
            if tag in tokenization_functions and tag != "Inner_Punc":
                return tokenization_functions[tag](fixed_in_cand)
            return InnerPuncParser.tokenize_inner_punc(fixed_in_cand)
        elif EmoticonParser.emoticon_count(fixed_in_cand) >= 2 and tag != "Inner_Punc":
            tokenized_emoticon = EmoticonParser.emoticon_tokenize(fixed_in_cand)
            return tokenization_functions.get(tokenized_emoticon, fixed_in_cand)
        else:
            return fixed_in_cand
    else:
        return fixed_in_cand


def tagged(in_word: object, fixed_in_cand: object, tag: object) -> object:
    if tag == "OOV" and any(char in string.punctuation for char in fixed_in_cand):
        return in_word, fixed_in_cand, PuncTagCheck.punc_tag_check(fixed_in_cand)
    elif tag == "OOV" and EmoticonParser.emoticon_count(fixed_in_cand) >= 2:
        return in_word, fixed_in_cand, tag
    else:
        return in_word, fixed_in_cand, tag


def process_tokens(args, word):
    result = TokenCheck.token_tagger(word, "all")
    in_word, fixed_in_cand, tag = result
    if args.output == "tagged":
        return tagged(in_word, fixed_in_cand, tag)
    elif args.output == "tokenized":
        return tokenized(in_word, fixed_in_cand, tag)


class TSTokenizer:

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--output", choices=["tokenized", "lines", "tagged"],
                            default="tokenized", help="Specify the output format")
        parser.add_argument("filename", help="Name of the file to process")
        parser.add_argument("-w", "--word", action="store_true", help="Enable cli input mode")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
        return parser.parse_args()

    @staticmethod
    def tokenize(text, return_format='tokenized'):
        tokens = text.split()
        processed_tokens = []

        for token in tokens:
            tag = TokenCheck.token_tagger(token, output='all')
            processed_tokens.append(tag)

        if return_format == 'tokenized':
            return ' '.join([token])
        elif return_format == 'lines':
            return '\n'.join([token])
        elif return_format == 'tagged':
            return ' '.join([f"{token}/{token}" for token in processed_tokens])


    @staticmethod
    def process_line(line, return_format):
        return TSTokenizer.tokenize(line, return_format)

    @staticmethod
    def ts_tokenize():
        args = TSTokenizer.parse_arguments()
        num_workers = multiprocessing.cpu_count() - 1
        if args.word:
            word = sys.argv[-1]
            if re.match(r'^\s*(<|</).*>\s*$', word):
                print(word)
            else:
                print(process_tokens(args, word))
        else:
            with open(args.filename, encoding='utf-8') as in_file:
                lines = in_file.readlines()
                total_lines = len(lines)
                pbar = tqdm(total=total_lines, desc="Processing File") if args.verbose else None
                with ThreadPoolExecutor(max_workers=num_workers) as executor:
                    for line in lines:
                        if re.match(r'^\s*(<|</).*>\s*$', line):
                            continue  # Skip lines matching the regex
                        words = line.split()
                        results = list(executor.map(lambda w: process_tokens(args, w), words))
                        for token in results:
                            if args.output == "tagged":
                                print("\t".join(token))
                            else:
                                print(token)
                            if args.verbose:
                                pbar.update(1)

                if pbar:
                    pbar.close()
