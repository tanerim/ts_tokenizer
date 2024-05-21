# Tuples for character replacement
REPLACEMENTS_CHAR = [
    ("þ", "ş"), ("Þñ", "ı"), ("ð", "ğ"), ("ɪ", "ı"), ("ý", "ı"), ("ḡ", "ğ"), ("¤", "ğ"), ("а", "a"), ("ƒ", "a"),
    ("œ", "i"), ("ð", "ğ"), ("ǧ", "ğ"), ("е", "e"), ("åÿ", "ş"), ("ș", "ş"), ("ɑ", "a"), ("о", "o"),
    ("Ã¶", "ö"), ("Ã¼", "ü"), ("Ã§", "ç"), ("Ä±", "ı"), ("›", "ı"), ("Ý", "İ"), ("Ã", "Ö"), ("Ð", "Ğ"), ("ġ", "Ş"),
    ("ÃŸ", "ş"), ("�", "ö"), ("…", "..."), ("»", ">"), ("«", "<"), ("s¸", "ş"), ("Ģ", "ş"), ("Þ", "Ş"), ("Ġ", "İ"),
]

# Tuples for html entities replacement
REPLACEMENTS_HTML = [
    ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", "\""), ("&nbsp;", ""), ("&Uuml;", "Ü")
]

# Tuples for quotation mark replacement
REPLACEMENTS_QUOTE = [
    ("“", "\""), ("”", "\""), ("’’", "\""), ("‘‘", "\""), ("‘’", "\""), ("‘’", "\""), ("", "\""), ("", "\""),
    ("''", "\""), ("", "\""), ("â", "'"), ("‘", "'"), ("’", "'"), ("", "'"), ("â€™", "'"), ("â€š", ","),
    ("'", "'"), ("’", "'"), ("'", "'"), ("’", "'"), ("'", "'"), ("’", "'")
]


class CharFix:
    @staticmethod
    def fix_tr_lowercase(word):
        conversion = {'I': 'ı', 'İ': 'i'}
        for key, value in conversion.items():
            word = word.replace(key, value)
        return word.lower()

    @staticmethod
    def replace(word, replacements):
        try:
            for old, new in replacements:
                word = word.replace(old, new)
            return word
        except Exception as e:
            print(f"Error in replacing characters: {e}")
            return word

    @staticmethod
    def char_check(word):
        return CharFix.replace(word, REPLACEMENTS_CHAR)

    @staticmethod
    def html_entity_replace(word):
        return CharFix.replace(word, REPLACEMENTS_HTML)

    @staticmethod
    def fix_quote(word):
        return CharFix.replace(word, REPLACEMENTS_QUOTE)

    @staticmethod
    def char_fix(word):
        word = CharFix.char_check(word)
        word = CharFix.html_entity_replace(word)
        word = CharFix.fix_quote(word)
        return word
