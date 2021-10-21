import sys
import re
from pre_check import ts_check
from token_splitter import split_tokens

with open(sys.argv[1], 'r') as f:
    while True:
        next_line = f.readline().strip("\n")
        if not next_line:
            break
        if next_line[0] == "<" and next_line[-1] == ">":
            print(next_line, "XML_Tag")
        else:
            word = re.sub(r" {2,}", " ", next_line)
            word = re.sub(r"\t{1,}", " ", word)
            word = word.replace("'''", "\"")
            word = word.replace("''", "\"")
            for token in word.split(" "):
                if token != "":
                    pre_check = ts_check.ts_tokenize(token)
                    the_word = str(pre_check[0])
                    the_tag = str(pre_check[1])
                    if the_tag == "token" \
                        or the_tag == "abbr" \
                        or the_tag == "punctuation" \
                        or the_tag == "abbr" \
                        or the_tag == "emoji" \
                        or the_tag == "emoticon" \
                        or the_tag == "roman_numeral" \
                        or the_tag == "email" \
                        or the_tag == "hashtag" \
                        or the_tag == "mention" \
                        or the_tag == "date" \
                        or the_tag == "hour" \
                        or the_tag == "number" \
                        or the_tag == "url" \
                        or the_tag == "www_url" \
                        or the_tag == "ip_address" \
                        or the_tag == "breadcrumb" \
                        or the_tag == "comma_separated_number" \
                        or the_tag == "dot_separated_number" \
                        or the_tag == "exclamation_tweak_alone":
                        print(the_word, "<==>", the_tag)
                    elif the_tag == "exclamation_tweak_word":
                        print(split_tokens.exclamation_tweak_word(the_word), the_tag)
                    elif the_tag == "in_parenthesis":
                        print(split_tokens.parenthesis(the_word), the_tag)
                    elif the_tag == "punc_initial":
                        print(split_tokens.punc_initial(the_word), the_tag)
                    elif the_tag == "punc_final":
                        print(split_tokens.punc_final(the_word), the_tag)
                    elif the_tag == "in_quotes":
                        print(split_tokens.in_quotes(the_word), the_tag)


                    elif the_tag == "one_dot_in":
                        print(split_tokens.dot_in(the_word), the_tag)
                    else:
                        print(the_word, "<==>", the_tag)

            #else:
            #    continue


