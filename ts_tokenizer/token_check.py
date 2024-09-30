import json
import re
from .token_preprocess import TokenPreProcess
from .char_fix import CharFix
from .punctuation_process import PuncTagCheck, PuncMatcher

class TokenCheck:
    @staticmethod
    def token_tagger(token: str, output: str = 'tag', output_format: str = 'tuple') -> object:
        token_tags = {
            "XML_Tag": ("single", TokenPreProcess.is_xml),
            "Valid_Word": ("single", TokenPreProcess.is_in_lexicon),
            "Exception_Word": ("single", TokenPreProcess.is_in_exceptions),
            "Eng_Word": ("single", TokenPreProcess.is_in_eng_words),
            "Abbr": ("single", TokenPreProcess.is_abbr),
            "Date": ("single", TokenPreProcess.is_date),
            "Hour": ("single", TokenPreProcess.is_hour),
            "Currency": ("single", TokenPreProcess.is_currency),
            "In_Parenthesis": ("recursive", TokenPreProcess.is_in_parenthesis),
            "In_Quotes": ("recursive", TokenPreProcess.is_in_quotes),
            "Smiley": ("single", TokenPreProcess.is_smiley),
            "Multiple_Smiley_In": ("recursive", TokenPreProcess.is_multiple_smiley_in),
            "Multiple_Smiley": ("recursive", TokenPreProcess.is_multiple_smiley),
            "Punc": ("single", TokenPreProcess.is_punc),
            "Email_Punc": ("recursive", TokenPreProcess.is_email_punc),
            "Email": ("single", TokenPreProcess.is_email),
            "Inner_Char": ("recursive", TokenPreProcess.is_inner_char),
            "Number": ("single", TokenPreProcess.is_number),
            "Non_Prefix_URL": ("single", TokenPreProcess.is_non_prefix_url),
            "Prefix_URL": ("single", TokenPreProcess.is_prefix_url),
            "Emoticon": ("single", TokenPreProcess.is_emoticon),
            "Mention": ("single", TokenPreProcess.is_mention),
            "HashTag": ("single", TokenPreProcess.is_hashtag),
            "Percentage_Numbers": ("single", TokenPreProcess.is_percentage_numbers),
            "Percentage_Number_Chars": ("single", TokenPreProcess.is_percentage_numbers_chars),
            "Roman_Number": ("single", TokenPreProcess.is_roman_number),
            "Underscored": ("recursive", TokenPreProcess.is_underscored),
            "Copyright": ("single", TokenPreProcess.is_copyright),
            "Registered": ("single", TokenPreProcess.is_registered),
            "Three_or_More": ("recursive", TokenPreProcess.is_three_or_more),
            "One_Char_Fixed": ("single", TokenPreProcess.is_one_char_fixable),
            "Non_Latin": ("recursive", TokenPreProcess.is_non_latin),
            "Multiple_Emoticon": ("recursive", TokenPreProcess.is_multiple_emoticon),
        }

        # Check if given param word is a string
        if not isinstance(token, str):
            return "OOV_Non_Char"

        # First fix Char Problems
        token_char_fixed = CharFix.fix(token)

        # Check for recursive tokens
        for tag, (process_type, check_method) in token_tags.items():
            if process_type == "recursive":
                check_result = check_method(token_char_fixed)
                if check_result:
                    # Call recursive_tag to handle further breakdown and tagging
                    return TokenCheck.recursive_tag(token_char_fixed)

        # Handle Single Processes
        for tag, (process_type, check_method) in token_tags.items():
            if process_type == "single":
                check_result = check_method(token_char_fixed)
                if isinstance(check_result, tuple):
                    token_char_fixed = check_result[0]
                    result = (token, token_char_fixed, tag)
                    break
                elif check_result:
                    result = (token, token_char_fixed, tag)
                    break
        else:
            # Check for punctuation tags
            punc_result = PuncTagCheck.punc_tag_check(token_char_fixed)
            if punc_result and PuncMatcher.punc_count(token_char_fixed) == 1 and "-" in token_char_fixed:
                result = (token, token_char_fixed, "OOV")
            elif punc_result and PuncMatcher.punc_count(token_char_fixed) >= 1:
                result = (token, token_char_fixed, punc_result[0])
            else:
                # If no tag is found, mark it as OOV
                result = (token, token_char_fixed, "OOV")

        # Output based on the format
        if output == 'tag':
            return result[2]
        return TokenCheck.format_output(result, output_format)

    @staticmethod
    def recursive_tag(token):
        """
        Recursively tag the token if it contains parentheses, quotes, or other nested components.
        """
        # Split the token into parts based on punctuation
        tokens = re.findall(r'\w+|[^\w\s]', token)
        tagged_tokens = []
        inner_token = token[1:-1]  # Strip surrounding punctuation (for example)
        tagged_tokens.append(TokenCheck.token_tagger(inner_token))
        return tagged_tokens

    @staticmethod
    def format_output(result, output_format):
        if output_format == 'tuple':
            return result
        elif output_format == 'list':
            return list(result)
        elif output_format == 'json':
            return json.dumps({"input_token": result[0], "fixed_token": result[1], "tag": result[2]})
        elif output_format == 'string':
            return f"{result[0]}\t{result[1]}\t{result[2]}"
