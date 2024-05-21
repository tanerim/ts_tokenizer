from .token_check import TokenCheck
from .char_fix import CharFix
from .emoticon_check import EmoticonParser

# The order of tag-function in token_checks dictionary is important


class TokenPreProcess:
    @staticmethod
    def token_tagger(word):
        token_tags = {
            "Valid_Word": TokenCheck.is_in_lexicon,
            "Exception_Word": TokenCheck.is_in_exceptions,
            "Eng_Word": TokenCheck.is_in_eng_words,
            "Date": TokenCheck.is_date,
            "Hour": TokenCheck.is_hour,
            "In_Parenthesis": TokenCheck.is_in_parenthesis,
            "In_Quotes": TokenCheck.is_in_quotes,
            "Smiley": TokenCheck.is_smiley,
            "Inner_Char": TokenCheck.is_inner_char,
            "Abbr": TokenCheck.is_abbr,
            "Number": TokenCheck.is_number,
            "Non_Prefix_URL": TokenCheck.is_non_prefix_url,
            "Prefix_URL": TokenCheck.is_prefix_url,
            "Emoticon": TokenCheck.is_emoticon,
            "Mention": TokenCheck.is_mention,
            "HashTag": TokenCheck.is_hashtag,
            "Percentage_Numbers": TokenCheck.is_percentage_numbers,
            "Percentage_Number_Chars": TokenCheck.is_percentage_numbers_chars,
            # "Formula": TokenCheck.is_formula,
            "Num_Char_Seq": TokenCheck.is_num_char_sequence,
            "Multiple_Smiley": TokenCheck.is_multiple_smiley,
            "Punc": TokenCheck.is_punc,
            "Underscored": TokenCheck.is_underscored,
            "Hyphenated": TokenCheck.is_hyphenated,
            "Hyphen_In": TokenCheck.is_hyphen_in,
            # "Mis_Hyphenated": TokenCheck.is_mishpyhenated,
            "Multiple_Emoticon": TokenCheck.is_multiple_emoticon,
            "Copyright": TokenCheck.is_copyright,
            "Email": TokenCheck.is_email,
            "Registered": TokenCheck.is_registered,
            "Three_or_More": TokenCheck.is_three_or_more
        }
        # Check if given param word is string
        if not isinstance(word, str):
            return None
        for tag, check_method in token_tags.items():
            if check_method(CharFix.char_fix(word)):
                return word, CharFix.char_fix(word), tag
        else:
            return word, CharFix.char_fix(word), "OOV"
