# Tuples for character replacement
REPLACEMENTS_CHAR = [
    ("þ", "ş"), ("Þñ", "ı"), ("ð", "ğ"), ("ɪ", "ı"), ("ý", "ı"), ("ḡ", "ğ"), ("¤", "ğ"), ("а", "a"), ("ƒ", "a"),
    ("œ", "i"), ("ð", "ğ"), ("ǧ", "ğ"), ("е", "e"), ("åÿ", "ş"), ("ș", "ş"), ("ɑ", "a"), ("о", "o"),
    ("Ã¶", "ö"), ("Ã¼", "ü"), ("Ã§", "ç"), ("Ä±", "ı"), ("›", "ı"), ("Ý", "İ"), ("Ã", "Ö"), ("Ð", "Ğ"), ("ġ", "Ş"),
    ("ÃŸ", "ş"), ("�", "ö"), ("…", "..."), ("»", ">"), ("«", "<"), ("s¸", "ş"), ("Ģ", "ş"), ("Þ", "Ş"), ("Ġ", "İ"),
    ("\\u011f", "ğ"), ("\\u00fc", "ü"), ("\\u0131", "ı"), ("\\u015f", "ş"), ("\\u00e7", "ç"), ("\\u00f6", "ö"),
    ("\\u0130", "İ"), ("\\u00dc", "Ü"), ("\\u015e", "Ş"), ("\\u00c7", "Ç")
]

# Tuples for html entities replacement
REPLACEMENTS_HTML = [
    ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", "\""), ("&nbsp;", " "), ("&Uuml;", "Ü"),
    ("&uuml;", "ü"), ("&Ouml;", "Ö"), ("&ouml;", "ö"), ("&Ccedil;", "Ç"), ("&ccedil;", "ç"),
    ("&Iuml;", "İ"), ("&iuml;", "i"), ("&ETH;", "Ğ"), ("&eth;", "ğ"), ("&THORN;", "Ş"), ("&thorn;", "ş"),
    ("&Auml;", "Ä"), ("&auml;", "ä"), ("&szlig;", "ß"), ("&rsquo;", "'"), ("&lsquo;", "‘")
]

# Tuples for quotation mark replacement
REPLACEMENTS_QUOTE = [
    ("“", "\""), ("”", "\""), ("’’", "\""), ("‘‘", "\""), ("‘’", "\""), ("‘’", "\""), ("", "\""), ("", "\""),
    ("''", "\""), ("", "\""), ("â", "'"), ("‘", "'"), ("’", "'"), ("", "'"), ("â€™", "'"), ("â€š", ","),
    ("'", "'"), ("’", "'"), ("'", "'"), ("’", "'"), ("'", "'"), ("’", "'"), ("\\u2018", "\""), ("\\u2019", "'"),
    ("\\u201c", "'"), ("\\u201d", "'")
]


def replace(word: str, replacements: list) -> str:
    try:
        for old, new in replacements:
            word = word.replace(old, new)
        return word
    except Exception as e:
        print(f"Error in replacing characters: {e}")
        return word


def char_check(word: str) -> str:
    return replace(word, REPLACEMENTS_CHAR)


class CharFix:

    @staticmethod
    def tr_lowercase(word: str) -> str:
        conversion = {'I': 'ı', 'İ': 'i'}
        for key, value in conversion.items():
            word = word.replace(key, value)
        return word.lower()

    @staticmethod
    def html_entity_replace(word: str) -> str:
        return replace(word, REPLACEMENTS_HTML)

    @staticmethod
    def fix_quote(word: str) -> str:
        return replace(word, REPLACEMENTS_QUOTE)

    @staticmethod
    def fix(word: str) -> str:
        word = char_check(word)
        word = CharFix.html_entity_replace(word)
        word = CharFix.fix_quote(word)
        return word
