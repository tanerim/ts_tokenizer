import re
import html
import unicodedata
# Tuples for character replacement
REPLACEMENTS_CHAR = [
    ("þ", "ş"), ("Þñ", "ı"), ("ð", "ğ"), ("ɪ", "ı"), ("ḡ", "ğ"), ("¤", "ğ"), ("а", "a"), ("ƒ", "a"),
    ("œ", "i"), ("ǧ", "ğ"), ("е", "e"), ("åÿ", "ş"), ("ș", "ş"), ("ɑ", "a"), ("о", "o"), ("í", "i"), ("ü", "ü"),
    ("Ã¶", "ö"), ("Ã¼", "ü"), ("Ã1/4", "ü"), ("Ã1/4", "ü"), ("Ã§", "ç"), ("Ä±", "ı"), ("›", "ı"), ("Ý", "İ"), ("Ã", "Ö"), ("Ð", "Ğ"), ("ġ", "Ş"),
    ("ÃŸ", "ş"), ("�", "ü"), ("…", "..."), ("»", ">"), ("«", "<"), ("s¸", "ş"), ("Ģ", "ş"), ("Þ", "Ş"), ("Ġ", "İ"), ("İ", "İ"), ("İ̇", "İ"),
    ("\\u011f", "ğ"), ("\\u00fc", "ü"), ("\\u0131", "ı"), ("\\u015f", "ş"), ("\\u00e7", "ç"), ("\\u00f6", "ö"), ("Ğ","Ğ"), ("Ç", "Ç"),
    ("\\u0130", "İ"), ("\\u00dc", "Ü"), ("\\u015e", "Ş"), ("\\u00c7", "Ç"), ("&#252;", "ü"), ("ģ", "ş"), ("ä±", "ı"), ("i̇", "i"), ("ì", "ı"),
    ("õ", "ı"), ("ﬂ", "ş"), ("ä°", "i"), ("đ", "i"), ('\\u2022', ''), ("ğ", "ğ"), ("ş̧", "ş"), ("ğ̆", "ğ"), ("Ş", "Ş"), ("Ş̧", "Ş"), ("ﬀ", "ff"), ("\\\\'", "'"),
    # Funny Char Problem
    ("ýº", "ış"), ("ºý", "şı"), ("üº", "üş"), ("ºü", "şü"), ("aº", "aş"), ("ºa", "şa"),
    ("uº", "uş"), ("ºu", "şu"), ("eº", "eş"), ("ºe", "şe"), ("ıº", "ış"), ("ºı", "şı"),
    ("iº", "iş"), ("ºi", "şi"), ("öº", "öş"), ("ºö", "şö"), ("oº", "oş"), ("ºo", "şo"),
    ("  ̊", "°"), ("ā", "â"), ("á", "â"), ("ç", "ç"), ("ğ", "ğ"), ("ﬁ", "ş"), ("ş", "ş"),
    ("Ä°", "İ"),
    ("ý", "ı"),
    # Fix Unicoed Chars
    ("і", "i"),
    # Fix Dashes - Need a better solution
    ("-", "-"), ("–", "-"), ("⁄", "/"), ("-", "-"), ("—-", "-"), ("﴾", "("), ("﴿", ")"), ("-", "-"), ("­","-"), ("−", "-"),
    # punctuation_process.py line 178 - fails if not replaced
    # needs a better solution
    ("°°", "°"), ("_\uFE0F", "_"),
    # extra replacements
    ("<200a>", ""), ("<200b>", ""), ("<200c>", ""), ("<200d>", ""), ("<200e>", ""),
    ("<202a>", ""), ("<202b>", ""), ("<202c>", ""), ("<202d>", ""), ("<202e>", "")
]

# Tuples for html entities replacement
# Non-Breaking space &nbsp; is handled by removing.
REPLACEMENTS_HTML = [
    ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", "\""), ("&nbsp;", ""), ("&Uuml;", "Ü"),
    ("&uuml;", "ü"), ("&Ouml;", "Ö"), ("&ouml;", "ö"), ("&Ccedil;", "Ç"), ("&ccedil;", "ç"),
    ("&Iuml;", "İ"), ("&iuml;", "i"), ("&ETH;", "Ğ"), ("&eth;", "ğ"), ("&THORN;", "Ş"), ("&thorn;", "ş"),
    ("&Auml;", "Ä"), ("&auml;", "ä"), ("&szlig;", "ß"), ("&rsquo;", "'"), ("&lsquo;", "‘"), ("&ndash;", "-"),
    ("&raquo;&raquo;", ">"), ("&lrm;", ""), ("&rlm;", ""), ("&raquo;", ">"), ("&laquo;", "<")
]

# Tuples for quotation mark replacement
REPLACEMENTS_QUOTE = [
    ("\"'", "'"), ("\"\"", "\""), (" ́", "'"), ("ʹ", "'"), ("ʺ", "\""), ("““", "\""),
    ("\"\"", "\""), ("“", "'"), ("„", "\""), ("”", "\""), ("’’", "\""), ("‘‘", "\""), ("‘’", "\""), ("‘’", "\""), ("", "\""), ("", "\""),
    ("''", "\""), ("", "\""), ("â", "'"), ("‘", "'"), ("’", "'"), ("", "'"), ("â€™", "'"), ("â€š", ","), ("‚", "'"),
    ("’", "'"), ("’", "'"), ("’", "'"), ("\\u2018", "\""), ("\\u2019", "'"), ("˵", "'"), ("˶", "'"), ("'", "'"),
    ("\\u201c", "'"), ("\\u201d", "'"), ("ʼ", "'"), ("``", "'"), ("´", "'"), ("`", "'"), ("´", "'"), ("’", "'"), ("′′", "'"), ("′", "'"),
    ("‟", "'"), ("́", "'"), ("″", "\""), ("„", "'"), ("”", "'")
]

REPLACEMENTS_CONTROL_CHAR = [
    ("\u200a", ""), ("\u200b", ""), ("\u200c", ""),
    ("\u200d", ""), ("\u200e", ""), ("\u200f", ""),
    ("\u0091", "‘"), ("\u0092", "‘"), ("\u0093", "‘"),
    ("\u0094", "‘"), ("\u0095", "‘"), ("\u0096", "‘")
 ]


class CharFix:
    _compiled_pattern_char = re.compile("|".join(map(re.escape, dict(REPLACEMENTS_CHAR).keys())))
    _compiled_pattern_control = re.compile("|".join(map(re.escape, dict(REPLACEMENTS_CONTROL_CHAR).keys())))
    _compiled_pattern_html = re.compile("|".join(map(re.escape, dict(REPLACEMENTS_HTML).keys())))
    _compiled_pattern_quote = re.compile("|".join(map(re.escape, dict(REPLACEMENTS_QUOTE).keys())))

    @staticmethod
    def batch_replace(word: str, compiled_pattern, replacements: dict, max_iterations=10) -> str:
        for _ in range(max_iterations):
            new_word = compiled_pattern.sub(lambda match: replacements[match.group(0)], word)
            if new_word == word:
                break  # Exit early if no changes are made
            word = new_word
        return word

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
    def remove_diacritics(word: str) -> str:
        normalized = unicodedata.normalize('NFD', word)
        return ''.join(c for c in normalized if not unicodedata.combining(c))

    @staticmethod
    def replace_diacritics(word: str) -> str:
        replacements = {"́": "'"}
        return ''.join(replacements.get(c, c) for c in word)

    @staticmethod
    def balance_quotes(word: str) -> str:
        # Handle empty word case
        if not word:
            return word

        # Count occurrences of quotes
        single_quote_count = word.count("'")
        double_quote_count = word.count("\"")

        # Ensure quotes are balanced
        if single_quote_count % 2 != 0:
            word = word.replace("'", "\"", 1)  # Replace the first unmatched single quote with double quote

        if double_quote_count % 2 != 0:
            word = word.replace("\"", "'", 1)  # Replace the first unmatched double quote with single quote

        return word

    @staticmethod
    def replace_all(word: str) -> str:
        word = CharFix.remove_unicode_controls(word)  # Remove control characters
        # word = CharFix.replace_diacritics(word)
        word = CharFix.fix_quote(word)
        word = CharFix.char_check(word)  # Apply character fixes
        word = CharFix.html_entity_replace(word)  # Replace HTML entities
        # word = CharFix.balance_quotes(word)
        return html.unescape(word)
        #return word

    @staticmethod
    def fix(word: str) -> str:
        return CharFix.replace_all(word)
