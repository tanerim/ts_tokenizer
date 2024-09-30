from ts_tokenizer.token_preprocess import TokenPreProcess
from ts_tokenizer.punctuation_process import PuncTagCheck


class TokenProcessor:

    def __init__(self):
        pass
    @staticmethod
    def process_token(token):
        check_methods = [
            # Lexicon Based Tokens
            TokenPreProcess.is_in_lexicon,
            TokenPreProcess.is_abbr,
            TokenPreProcess.is_in_exceptions,
            TokenPreProcess.is_in_eng_words,
            TokenPreProcess.is_smiley,
            TokenPreProcess.is_emoticon,
            TokenPreProcess.is_number,
            TokenPreProcess.is_punc,

            # Basic Regex Tokens
            TokenPreProcess.is_xml,
            TokenPreProcess.is_mention,
            TokenPreProcess.is_hashtag,
            TokenPreProcess.is_copyright,
            TokenPreProcess.is_registered,
            TokenPreProcess.is_currency,
            TokenPreProcess.is_in_quotes,
            TokenPreProcess.is_in_parenthesis,
            TokenPreProcess.is_num_char_sequence,
            TokenPreProcess.is_date_range,
            TokenPreProcess.is_date,
            TokenPreProcess.is_hour,
            TokenPreProcess.is_percentage_numbers_chars,
            TokenPreProcess.is_percentage_numbers,
            TokenPreProcess.is_roman_number,
            TokenPreProcess.is_email_punc,
            TokenPreProcess.is_email,
            TokenPreProcess.is_prefix_url,
            TokenPreProcess.is_non_prefix_url,
            TokenPreProcess.is_multiple_smiley,
            TokenPreProcess.is_multiple_smiley_in,
            TokenPreProcess.is_multiple_emoticon,
            TokenPreProcess.is_underscored,
            TokenPreProcess.is_three_or_more,
            TokenPreProcess.is_inner_char,
            TokenPreProcess.is_non_latin,
            TokenPreProcess.is_one_char_fixable
        ]

        for check in check_methods:
            result = check(token)
            if result:
                return result
            else:
                return PuncTagCheck.punc_tag_check(token)
        return token, "OOV"  # Default return if no checks match
