import os
from typing import FrozenSet

from .char_fix import CharFix

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

# Read lists for Emoticons, Smileys, Abbreviations and Valid Word List Extracted from TS Corpus

emoticons = set(line.strip() for line in open(os.path.join(data_dir, 'emoticons.txt')))
smileys = set(line.strip() for line in open(os.path.join(data_dir, 'smileys.txt')))
abbrs = set(CharFix.tr_lowercase(line.strip()) for line in open(os.path.join(data_dir, 'abbr_list.txt')))
candidate_abbrs = set(line.strip() for line in open(os.path.join(data_dir, 'cand_abbr_list.txt')))
word_list = set(line.strip() for line in open(os.path.join(data_dir, 'TS_Corpus_Turkish_Word_List.txt')))
exception_words = set(line.strip() for line in open(os.path.join(data_dir, 'exceptions.txt')))
eng_words = set(line.strip() for line in open(os.path.join(data_dir, 'eng_word_list.txt')))
domains = set(line.strip() for line in open(os.path.join(data_dir, 'domains.txt')))
currencies = set(line.strip() for line in open(os.path.join(data_dir, 'currency_symbols.txt')))
correction_mark = set(line.strip() for line in open(os.path.join(data_dir, 'corection_mark.txt')))


class LocalData:
    @staticmethod
    def emoticons():
        return emoticons

    @staticmethod
    def smileys():
        return smileys

    @staticmethod
    def abbrs():
        return abbrs

    @staticmethod
    def candidate_abbrs():
        return candidate_abbrs

    @staticmethod
    def word_list():
        return word_list

    @staticmethod
    def correction_mark():
        return correction_mark

    @staticmethod
    def exception_words():
        return exception_words

    @staticmethod
    def eng_word_list():
        return eng_words

    @staticmethod
    def domains():
        return domains

    @staticmethod
    def currency_symbols():
        return currencies


DATASETS = {
    "emoticons": LocalData.emoticons,
    "smileys": LocalData.smileys,
    "abbrs": LocalData.abbrs,
    "word_list": LocalData.word_list,
    "correction_mark": LocalData.correction_mark,
    "exception_words": LocalData.exception_words,
    "eng_word_list": LocalData.eng_word_list,
    "domains": LocalData.domains,
    "currency_symbols": LocalData.currency_symbols,
}


def get_data(name: str) -> FrozenSet[str]:
    try:
        dataset = DATASETS[name]()
    except KeyError as exc:
        available = ", ".join(sorted(DATASETS))
        raise ValueError(f"Unknown dataset: {name}. Available datasets: {available}") from exc
    return frozenset(dataset)


def emoticons_data() -> FrozenSet[str]:
    return get_data("emoticons")


def smileys_data() -> FrozenSet[str]:
    return get_data("smileys")


def abbrs_data() -> FrozenSet[str]:
    return get_data("abbrs")


def word_list_data() -> FrozenSet[str]:
    return get_data("word_list")


def correction_mark_data() -> FrozenSet[str]:
    return get_data("correction_mark")


def exception_words_data() -> FrozenSet[str]:
    return get_data("exception_words")


def eng_word_list_data() -> FrozenSet[str]:
    return get_data("eng_word_list")


def domains_data() -> FrozenSet[str]:
    return get_data("domains")


def currency_symbols_data() -> FrozenSet[str]:
    return get_data("currency_symbols")


__all__ = [
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
