import sys
import argparse
import string
import re
import multiprocessing
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from ts_tokenizer.token_check import TokenCheck
from ts_tokenizer.parse_tokens import ParseTokens
from ts_tokenizer.emoticon_check import EmoticonParser
from ts_tokenizer.punctuation_process import PuncTagCheck, PuncMatcher
from ts_tokenizer.token_preprocess import TokenPreProcess

# Tokenization functions for different cases
tokenization_functions = {
    "XML_Tag": ParseTokens.tokenize_xml,
    "Initial_Quote": ParseTokens.tokenize_initial_quote,
    "ISP": ParseTokens.tokenize_isp,
    "FSP": ParseTokens.tokenize_fsp,
    "MSSP": ParseTokens.tokenize_mssp,
    "MSP": ParseTokens.tokenize_msp,
    "FMP": ParseTokens.tokenize_fmp,
    "IMP": ParseTokens.tokenize_imp,
    "In_Parenthesis": ParseTokens.tokenize_in_parenthesis,
    "In_Quotes": ParseTokens.tokenize_in_quotes,
    "Complex_Punc": ParseTokens.tokenize_complex_punc,
    "Mis_Hyphenated": ParseTokens.tokenize_mishyphenated,
    "Inner_Punc": ParseTokens.tokenize_inner_punc,
    "Date": ParseTokens.tokenize_date,
    "One_Char_Fixed": ParseTokens.tokenize_one_char_fixed
}

# Handles tokenized output and processes based on token tags


def tokenized(in_word, fixed_in_cand, tag):
    pre_token = tagged(in_word, fixed_in_cand, tag)
    tag = pre_token[2]

    # Lexicon, exceptions, and English word checks
    if TokenPreProcess.is_in_lexicon(fixed_in_cand) or TokenPreProcess.is_in_exceptions(fixed_in_cand) or TokenPreProcess.is_in_eng_words(fixed_in_cand):
        return fixed_in_cand

    # Process token based on tag
    if tag in tokenization_functions:
        return tokenization_functions[tag](fixed_in_cand)
    elif tag == "OOV":
        if fixed_in_cand and (fixed_in_cand[0] in string.punctuation or fixed_in_cand[-1] in string.punctuation):
            return tokenization_functions.get(tag, ParseTokens.tokenize_inner_punc)(fixed_in_cand)
        elif EmoticonParser.emoticon_count(fixed_in_cand) >= 2:
            return EmoticonParser.emoticon_tokenize(fixed_in_cand)
    return fixed_in_cand


# Handles the tagging logic for tokens
def tagged(in_word, fixed_in_cand, tag):
    if tag == "OOV" and "-" in in_word:
        return in_word, fixed_in_cand, PuncMatcher.hyphen_in(fixed_in_cand)
    if tag == "OOV" and any(char in string.punctuation for char in fixed_in_cand):
        return in_word, fixed_in_cand, PuncTagCheck.punc_tag_check(fixed_in_cand)
    elif tag == "OOV" and EmoticonParser.emoticon_count(fixed_in_cand) >= 2:
        return in_word, fixed_in_cand, tag
    return in_word, fixed_in_cand, tag


# Main function to process a word and return tagged/tokenized result
def process_tokens(args, word):
    result = TokenCheck.token_tagger(word, "all")
    in_word, fixed_in_cand, tag = result
    if args.output == "tagged":
        return tagged(in_word, fixed_in_cand, tag)
    elif args.output == "tokenized":
        return tokenized(in_word, fixed_in_cand, tag)
    elif args.output == "lines":
        return tokenized(in_word, fixed_in_cand, tag)


# Tokenizer class definition
class TSTokenizer:

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument("-o", "--output", choices=["tokenized", "lines", "tagged"], default="tokenized", help="Specify the output format")
        parser.add_argument("filename", help="Name of the file to process")
        parser.add_argument("-w", "--word", action="store_true", help="Enable CLI input mode")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
        return parser.parse_args()

    @staticmethod
    def tokenize(text, return_format='tokenized'):
        """
        Tokenizes the input text and returns it in the specified format.
        """
        tokens = text.split()
        processed_tokens = []

        for token in tokens:
            tag_result = TokenCheck.token_tagger(token, output='all')
            processed_tokens.append(tag_result)

        # Return the processed tokens based on the return format
        if return_format == 'tokenized':
            return ' '.join([token[1] for token in processed_tokens])  # tokenized result
        elif return_format == 'lines':
            return '\n'.join([token[1] for token in processed_tokens])  # returns each token on a new line
        elif return_format == 'tagged':
            return ' '.join([f"{token[0]}/{token[2]}" for token in processed_tokens])  # original/tagged-token
        elif return_format == 'details':
            return ' '.join([f"{token[0]}/{token[2]}" for token in processed_tokens])  # detils

    @staticmethod
    def process_line(line, return_format):
        return TSTokenizer.tokenize(line, return_format)

    @staticmethod
    def ts_tokenize():
        args = TSTokenizer.parse_arguments()
        num_workers = multiprocessing.cpu_count() - 1

        if args.word:
            word = sys.argv[-1]
            print(process_tokens(args, word))
        else:
            with open(args.filename, encoding='utf-8') as in_file:
                lines = in_file.readlines()

                pbar = tqdm(total=len(lines), desc="Processing File") if args.verbose else None

                with ThreadPoolExecutor(max_workers=num_workers) as executor:
                    for line in lines:
                        # xml_pattern = r'(<[^<> ]*) ([^<>]*>)'
                        xml_pattern = r'(<[^<> ]*[^<>]*?>)|(<[^<> ]*)|(/[^<>]*>)'

                        if re.search(xml_pattern, line):
                            if args.output == "tagged":
                                print(" ".join((line, "XML_Tag")).replace("\n", " "))
                            else:
                                print(line)

                        else:
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


if __name__ == "__main__":
    TSTokenizer.ts_tokenize()
