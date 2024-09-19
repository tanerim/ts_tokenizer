import re
import unicodedata
# Tuples for character replacement
REPLACEMENTS_CHAR = [
    ("þ", "ş"), ("Þñ", "ı"), ("ð", "ğ"), ("ɪ", "ı"), ("ḡ", "ğ"), ("¤", "ğ"), ("а", "a"), ("ƒ", "a"),
    ("œ", "i"), ("ð", "ğ"), ("ǧ", "ğ"), ("е", "e"), ("åÿ", "ş"), ("ș", "ş"), ("ɑ", "a"), ("о", "o"), ("í", "i"),
    ("Ã¶", "ö"), ("Ã¼", "ü"), ("Ã§", "ç"), ("Ä±", "ı"), ("›", "ı"), ("Ý", "İ"), ("Ã", "Ö"), ("Ð", "Ğ"), ("ġ", "Ş"),
    ("ÃŸ", "ş"), ("�", "ü"), ("…", "..."), ("»", ">"), ("«", "<"), ("s¸", "ş"), ("Ģ", "ş"), ("Þ", "Ş"), ("Ġ", "İ"),
    ("\\u011f", "ğ"), ("\\u00fc", "ü"), ("\\u0131", "ı"), ("\\u015f", "ş"), ("\\u00e7", "ç"), ("\\u00f6", "ö"),
    ("\\u0130", "İ"), ("\\u00dc", "Ü"), ("\\u015e", "Ş"), ("\\u00c7", "Ç"), ("&#252;", "ü"), ("ģ", "ş"), ("ä±", "ı"),
    ("õ", "ı"), ("ﬂ", "ş"), ("ä°", "i"), ("đ", "i"),
    # Funny Char Problem
    ("ýº", "ış"), ("ºý", "şı"), ("üº", "üş"), ("ºü", "şü"), ("aº", "aş"), ("ºa", "şa"),
    ("uº", "uş"), ("ºu", "şu"), ("eº", "eş"), ("ºe", "şe"), ("ıº", "ış"), ("ºı", "şı"),
    ("iº", "iş"), ("ºi", "şi"), ("öº", "öş"), ("ºö", "şö"), ("oº", "oş"), ("ºo", "şo"),
    ("Ä°","İ"),
    ("ý", "ı"),
    # Fix Unicoed Chars
    ("і", "i"),
    # Fix Dashes - Need a better solution
    ("-", "-"), ("–", "-"), ("⁄", "/"), ("-", "-"),
    # punctuation_process.py line 178 - fails if not replaced
    # needs a better solution
    ("°°", "°")
]

# Tuples for html entities replacement
# Non-Breaking space &nbsp; is handled by removing.
REPLACEMENTS_HTML = [
    ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", "\""), ("&nbsp;", ""), ("&Uuml;", "Ü"),
    ("&uuml;", "ü"), ("&Ouml;", "Ö"), ("&ouml;", "ö"), ("&Ccedil;", "Ç"), ("&ccedil;", "ç"),
    ("&Iuml;", "İ"), ("&iuml;", "i"), ("&ETH;", "Ğ"), ("&eth;", "ğ"), ("&THORN;", "Ş"), ("&thorn;", "ş"),
    ("&Auml;", "Ä"), ("&auml;", "ä"), ("&szlig;", "ß"), ("&rsquo;", "'"), ("&lsquo;", "‘"), ("&ndash;", "-")
]

# Tuples for quotation mark replacement
REPLACEMENTS_QUOTE = [
    ("“", "\""), ("”", "\""), ("’’", "\""), ("‘‘", "\""), ("‘’", "\""), ("‘’", "\""), ("", "\""), ("", "\""),
    ("''", "\""), ("", "\""), ("â", "'"), ("‘", "'"), ("’", "'"), ("", "'"), ("â€™", "'"), ("â€š", ","),
    ("’", "'"), ("’", "'"), ("’", "'"), ("\\u2018", "\""), ("\\u2019", "'"), ("˵", "'"), ("˶", "'"), ("'", "'"),
    ("\\u201c", "'"), ("\\u201d", "'"), ("ʼ", "'"),  ("``", "'"), ("´", "'"), ("`", "'"), ("´", "'"), ("’", "'")
]

REPLACEMENTS_CONTROL_CHAR = [
    ("\u200a", ""), ("\u200b", ""), ("\u200c", ""),
    ("\u200d", ""), ("\u200e", ""), ("\u200f", "")
 ]



class CharFix:
    _compiled_pattern_char = re.compile("|".join(map(re.escape, dict(REPLACEMENTS_CHAR).keys())))
    _compiled_pattern_control = re.compile("|".join(map(re.escape, dict(REPLACEMENTS_CONTROL_CHAR).keys())))
    _compiled_pattern_html = re.compile("|".join(map(re.escape, dict(REPLACEMENTS_HTML).keys())))
    _compiled_pattern_quote = re.compile("|".join(map(re.escape, dict(REPLACEMENTS_QUOTE).keys())))

    @staticmethod
    def batch_replace(word: str, compiled_pattern, replacements: dict) -> str:
        return compiled_pattern.sub(lambda match: replacements[match.group(0)], word)

    @staticmethod
    def char_check(word: str) -> str:
        return CharFix.batch_replace(word, CharFix._compiled_pattern_char, dict(REPLACEMENTS_CHAR))

    @staticmethod
    def tr_lowercase(word: str) -> str:
        conversion = {'I': 'ı', 'İ': 'i'}
        for key, value in conversion.items():
            word = word.replace(key, value)
        return word.lower()

    @staticmethod
    def remove_unicode_controls(word: str) -> str:
        return CharFix.batch_replace(word, CharFix._compiled_pattern_control, dict(REPLACEMENTS_CONTROL_CHAR))

    @staticmethod
    def html_entity_replace(word: str) -> str:
        return CharFix.batch_replace(word, CharFix._compiled_pattern_html, dict(REPLACEMENTS_HTML))

    @staticmethod
    def fix_quote(word: str) -> str:
        return CharFix.batch_replace(word, CharFix._compiled_pattern_quote, dict(REPLACEMENTS_QUOTE))


    @staticmethod
    def fix(word: str) -> str:
        word = unicodedata.normalize('NFKC', word)  # Normalize Unicode
        word = CharFix.char_check(word)  # Apply character fixes
        word = CharFix.remove_unicode_controls(word)  # Remove control characters
        word = CharFix.html_entity_replace(word)  # Replace HTML entities
        word = CharFix.fix_quote(word)  # Fix quotes
        return word