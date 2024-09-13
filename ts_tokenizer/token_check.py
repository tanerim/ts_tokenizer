import json
from .token_preprocess import TokenPreProcess
from .char_fix import CharFix
from .punctuation_process import PuncTagCheck, PuncMatcher


class TokenCheck:
    # The order of token_tags list directly changes tho output
    # Please modify it carefully
    def __init__(self):
        pass

    @staticmethod
    def token_tagger(token: str, output: str = 'tag', output_format: str = 'tuple') -> object:
        token_tags = {
            "One_Char_Fixed": TokenPreProcess.is_one_char_fixable,
            "Valid_Word": TokenPreProcess.is_in_lexicon,
            "Exception_Word": TokenPreProcess.is_in_exceptions,
            "Eng_Word": TokenPreProcess.is_in_eng_words,
            "Date": TokenPreProcess.is_date,
            "Hour": TokenPreProcess.is_hour,
            "Currency_Initial": TokenPreProcess.is_currency_initial,
            "Currency_Final": TokenPreProcess.is_currency_final,
            "In_Parenthesis": TokenPreProcess.is_in_parenthesis,
            "In_Quotes": TokenPreProcess.is_in_quotes,
            "Smiley": TokenPreProcess.is_smiley,
            "Punc": TokenPreProcess.is_punc,
            "Email_Punc": TokenPreProcess.is_email_punc,
            "Email": TokenPreProcess.is_email,
            "Inner_Char": TokenPreProcess.is_inner_char,
            "Abbr": TokenPreProcess.is_abbr,
            "Number": TokenPreProcess.is_number,
            "Non_Prefix_URL": TokenPreProcess.is_non_prefix_url,
            "Prefix_URL": TokenPreProcess.is_prefix_url,
            "Emoticon": TokenPreProcess.is_emoticon,
            "Mention": TokenPreProcess.is_mention,
            "HashTag": TokenPreProcess.is_hashtag,
            "Percentage_Numbers": TokenPreProcess.is_percentage_numbers,
            "Percentage_Number_Chars": TokenPreProcess.is_percentage_numbers_chars,
            "Roman_Number": TokenPreProcess.is_roman_number,
            "Multiple_Smiley": TokenPreProcess.is_multiple_smiley,
            "Underscored": TokenPreProcess.is_underscored,
            "Copyright": TokenPreProcess.is_copyright,
            "Registered": TokenPreProcess.is_registered,
            "Three_or_More": TokenPreProcess.is_three_or_more,
            "Hyphen_In": TokenPreProcess.is_hyphen_in,
            "Numeric_Hyphenated": TokenPreProcess.is_hyphen_in,
            "Alphanumeric_Hyphenated": TokenPreProcess.is_hyphen_in,
            "Hyphenated": TokenPreProcess.is_hyphenated,
            "Num_Char_Seq": TokenPreProcess.is_num_char_sequence,
            "Mis_Hyphenated": TokenPreProcess.is_mis_hyphenated,
            "Foreign_Word": TokenPreProcess.is_foreign_word,
            "Multiple_Emoticon": TokenPreProcess.is_multiple_emoticon,
            # "Formula": TokenPreProcess.is_formula,
        }

        # Check if given param word is a string
        if not isinstance(token, str):
            return "OOV_Non_Char"

        # First fix Char Problems
        token_char_fixed = CharFix.fix(token)

        # Then, check the token against the predefined tags
        for tag, check_method in token_tags.items():
            if check_method(token_char_fixed):
                result = (token, token_char_fixed, tag)
                break
        else:
            # Then, check for punctuation tags
            punc_result = PuncTagCheck.punc_tag_check(token_char_fixed)
            if punc_result and PuncMatcher.punc_count(token_char_fixed) >= 1:
                result = (token, token_char_fixed, punc_result[0])
            else:
                # If no tag is found, mark it as OOV
                result = (token, token_char_fixed, "OOV")

        if output == 'tag':
            return result[2]

        if output == 'all':
            if output_format == 'tuple':
                return result
            elif output_format == 'list':
                return list(result)
            elif output_format == 'json':
                return json.dumps({"input_token": result[0], "fixed_token": result[1], "tag": result[2]})
            elif output_format == 'string':
                return f"{result[0]}\t{result[1]}\t{result[2]}"
