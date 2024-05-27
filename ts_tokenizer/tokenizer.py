import argparse
import json
from ts_tokenizer.token_check import TokenCheck
from ts_tokenizer.parse_tokens import ParseTokens


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=["tokenized", "lines", "tagged", "details"],
                        default="tokenized", help="specify how to print the items")
    parser.add_argument("filename", help="the name of the file to process")
    parser.add_argument("--color", "-c", action="store_true", help="enable colored output")
    return parser.parse_args()

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
    #"Multiple_Emoticon": EmoticonParser.emoticon_tokenize,
    #"Multiple_Smiley": SmileyParser.smiley_tokenize,
    "Mis_Hyphenated": ParseTokens.tokenize_mishyphenated,
    #"Inner_Punc": InnerPuncParser.tokenize_Inner_Punc,
}



class TSTokenizer:
    def __init__(self):
        pass

    @staticmethod
    def tokenize(text, return_format='tokenized'):
        tokens = text.split()  # Basic whitespace tokenization; replace with a more complex logic if needed
        processed_tokens = []

        for token in tokens:
            tag = TokenCheck.token_tagger(token, output='all')
            #tag = TokenPreProcess.token_tagger(fixed_token, output='all')
            processed_tokens.append(tag)

        if return_format == 'tokenized':
            return ' '.join([token[1] for token in processed_tokens])
        elif return_format == 'lines':
            return '\n'.join([token[1] for token in processed_tokens])
        elif return_format == 'tagged':
            return ' '.join([f"{token[1]}/{token[2]}" for token in processed_tokens])
        elif return_format == 'details':
            return json.dumps([{
                'original': token[0],
                'fixed': token[1],
                'tag': token[2]
            } for token in processed_tokens], ensure_ascii=False)


def process_line(line, return_format):
    return TSTokenizer.tokenize(line, return_format)


def main():
    args = parse_arguments()

    with open(args.filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:

            results = process_line(line, args.output)

            output = '\n'.join(results)

    if args.color:
        # Optional: Add code for colored output if needed
        pass

    print(output)


if __name__ == "__main__":
    main()
