from ts_tokenizer.token_handler import TokenPreProcess

check_methods = [
            # First Check for SGML tags |
            TokenPreProcess.is_xml,

            # Lexicon Based Tokens
            TokenPreProcess.is_in_lexicon,
            TokenPreProcess.is_abbr,
            TokenPreProcess.is_in_exceptions,
            TokenPreProcess.is_in_eng_words,
            TokenPreProcess.is_smiley,
            TokenPreProcess.is_emoticon,
            TokenPreProcess.is_number,

            # Specific Cases for Punctuation Use
            TokenPreProcess.is_in_quotes,
            TokenPreProcess.is_in_parenthesis,
            TokenPreProcess.is_underscored,
            TokenPreProcess.is_email,
            TokenPreProcess.is_email_punc,
            TokenPreProcess.is_prefix_url,
            TokenPreProcess.is_non_prefix_url,
            TokenPreProcess.is_multiple_smiley_in,
            TokenPreProcess.is_multiple_smiley,
            TokenPreProcess.is_date_range,
            TokenPreProcess.is_date,
            TokenPreProcess.is_hour,

            # Basic Regex Tokens
            TokenPreProcess.is_mention,
            TokenPreProcess.is_hashtag,
            TokenPreProcess.is_copyright,
            TokenPreProcess.is_registered,
            TokenPreProcess.is_currency,
            TokenPreProcess.is_percentage_numbers_chars,
            TokenPreProcess.is_percentage_numbers,

            # Various Status for Punctuation
            TokenPreProcess.is_apostrophed,

            # These need recursive handling
            TokenPreProcess.is_fsp,
            TokenPreProcess.is_isp,
            TokenPreProcess.is_mssp,
            TokenPreProcess.is_msp,
            TokenPreProcess.is_midp,
            TokenPreProcess.is_imp,
            TokenPreProcess.fmp,

            # Raw Punctuation
            TokenPreProcess.is_punc,
            TokenPreProcess.is_roman_number,

            TokenPreProcess.is_multiple_emoticon,
            TokenPreProcess.is_three_or_more,
            TokenPreProcess.is_inner_char,
            TokenPreProcess.is_non_latin,
            TokenPreProcess.is_one_char_fixable,
            # TokenPreProcess.is_num_char_sequence
        ]


class TokenProcessor:

    def __init__(self):
        pass

    @staticmethod
    def format_output(result, output_format):
        if output_format == 'tuple':
            return result
        elif output_format == 'list':
            return list(result)
        elif output_format == 'string':
            return f"{result[0]}\t{result[1]}"

    @staticmethod
    def process_token(token: str, output_format: str = 'tuple') -> tuple:
        for check in check_methods:
            result = check(token)
            if result:
                return TokenProcessor.format_output(result, output_format)

        # If no checks match, return "OOV" with the requested output format
        oov_result = (token, "OOV")
        return TokenProcessor.format_output(oov_result, output_format)
