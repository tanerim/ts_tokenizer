from importlib import import_module

__version__ = "0.2.2"

_EXPORT_MAP = {
    "tokenize": (".tokenizer", "tokenize"),
    "TSTokenizer": (".tokenizer", "TSTokenizer"),
    "CharFix": (".char_fix", "CharFix"),
    "fix": (".char_fix", "fix"),
    "tr_lowercase": (".char_fix", "tr_lowercase"),
    "fix_quote": (".char_fix", "fix_quote"),
    "TokenProcessor": (".token_handler", "TokenProcessor"),
    "TokenPreProcess": (".token_handler", "TokenPreProcess"),
    "LocalData": (".data", "LocalData"),
    "get_data": (".data", "get_data"),
    "emoticons_data": (".data", "emoticons_data"),
    "smileys_data": (".data", "smileys_data"),
    "abbrs_data": (".data", "abbrs_data"),
    "word_list_data": (".data", "word_list_data"),
    "correction_mark_data": (".data", "correction_mark_data"),
    "exception_words_data": (".data", "exception_words_data"),
    "eng_word_list_data": (".data", "eng_word_list_data"),
    "domains_data": (".data", "domains_data"),
    "currency_symbols_data": (".data", "currency_symbols_data"),
}


def __getattr__(name):
    try:
        module_name, attr_name = _EXPORT_MAP[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name, __name__)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(list(globals().keys()) + list(_EXPORT_MAP.keys()))


__all__ = [
    "__version__",
    "tokenize",
    "TSTokenizer",
    "CharFix",
    "fix",
    "tr_lowercase",
    "fix_quote",
    "TokenProcessor",
    "TokenPreProcess",
    "LocalData",
    "get_data",
    "emoticons_data",
    "smileys_data",
    "abbrs_data",
    "word_list_data",
    "correction_mark_data",
    "exception_words_data",
    "eng_word_list_data",
    "domains_data",
    "currency_symbols_data",
]
