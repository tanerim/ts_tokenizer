import argparse
import requests
import json
import sys
import re
from ts_tokenizer.token_check import TokenCheck
from ts_tokenizer.parse_tokens import ParseTokens
from multiprocessing import Pool, cpu_count
from ts_tokenizer.char_fix import CharFix


def post_to_api(directive, data_input):
    url = "http://localhost:11434/api/chat"
    headers = {'Content-Type': 'application/json'}
    prompt = directive + "\n" + data_input
    # llama3:latest
    data = {
        "model": 'llama3:latest',
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return response

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

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", choices=["tokenized", "lines", "tagged", "details"],
                        default="tokenized", help="specify how to print the items")
    parser.add_argument("filename", help="the name of the file to process")
    parser.add_argument("--color", "-c", action="store_true", help="enable colored output")
    return parser.parse_args()

directive = """
You're working on a Turkish Tokenizer.
You're given a list of tokens. The data is in word + tag format. Tags, their explanation and a sample are as follows:

FSP ==> Final Single Punctuation ==> merhaba!
ISP ==> Final Single Punctuation ==> !merhaba
MSP ==> Multiside Punctuation ==> !merhaba.
FMP ==> Final Multiple Punctuation ==> merhaba!!
IMP ==> Initial Multiple Punctuation ==> !?merhaba
Initial_Quote ==> Initial Quote ==> "merhaba
In_Parenthesis ==> Inside Parenthesis ==> (merhaba)
In_Quotes ==> Inside Quotes ==> "merhaba"
Complex_Punc ==> Complex Punctuation ==> yeniden",gel

Focus on "Complex_Punc" tags.
I want you to check the given a list of tokens according to the given tags and samples.
Then generate a rule that defines a tokenization rule with the tag "Complex_Punc"
and write a python function that tokenizes Complex_Punc words according to Turkish.
But, do not use any libraries like NLTK, pyparsing, etc.
"""

girdiler = ""

#with open(sys.argv[1], 'r', encoding='utf-8') as file:
#    lines = file.read().strip().split('\n')
#    for word in lines:
#        token_candidates = TokenCheck.token_tagger(word, output='all', output_format='str')
#        print(token_candidates)
        #token_fixed = token_candidates[1]
        #tag = token_candidates[2]
        #if tag == "Complex_Punc":
        #    print(token_candidates[1])
        #    girdiler += f"{word} -> {token_fixed} (Tag: {tag})\n"


def process_word(word):
    token_candidates = TokenCheck.token_tagger(word, output='all')
    return token_candidates


def main():
    # Determine the number of available cores
    num_cores = cpu_count() - 1
    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        words = file.read().strip().split('\n')

        # Create a Pool of workers
        with Pool(num_cores) as pool:
            pool.apply_async(process_word)
            results = pool.map(process_word, words)
            for result in results:
                if result[2] != "Valid_Word":
                    print(result)


if __name__ == '__main__':
    main()

#ai_response = post_to_api(directive, girdiler)
#print(ai_response['message']['content'])


