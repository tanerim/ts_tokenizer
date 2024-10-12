import os

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')

# Read lists for Emoticons, Smileys, Abbreviations and Valid Word List Extracted from TS Corpus

emoticons = set(line.strip() for line in open(os.path.join(data_dir, 'emoticons.txt')))
smileys = set(line.strip() for line in open(os.path.join(data_dir, 'smileys.txt')))
abbrs = set(line.strip() for line in open(os.path.join(data_dir, 'abbr_list.txt')))
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
    def word_list():
        return word_list

    @staticmethod
    def correction_mark():
        return word_list

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
