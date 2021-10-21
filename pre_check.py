import re
import string

## Get exceptions ##
emojis = open('emoji_list.txt', 'r').read().split("\n")
abbrs = open('abbr.txt', 'r').read().split("\n")
emoticons = open('emoticon_list.txt', 'r').read().split("\n")
punctuations = open('punctuation.txt', 'r').read().split("\n")
ts_list = open('TS_Corpus_Turkish_Word_List.txt', 'r').read().split("\n")
####################
# List of regexs -I- Fully Checked
hour_regex = "[0-2][0-9]([:.]\d{2})$"
date_regex = "\d{2}[\.,:\\/]\d{2}[\.,:\\/]\d{4}"
url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
www_url_regex = r"^www\.[a-zA-Z]{2,}\.[a-zA-Z]{2,4}"
email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
hashtag = r"^#{1}[^#].*[\w.]$"
mention = r"^@{1}[^@].*[\w.]$"
ip_addr = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
comma_separated_number = r"^[\d]{1,},[\d]{1,}$"
dot_separated_number = r"^[\d]{1,}\.[\d]{1,}$"
# List of regexs -II- Not Fully Checked
final_many_punc = r"^.*[^\d,\w]{2,}$"
final_punc = r"^.*[^\d,\w]{1}$"
one_dot_in = r"[a-zçğüöıA-ZÇĞÜÖİ][^\d]{1,}\.{1}.*[a-zçğüöıA-ZÇĞÜÖİ][^\d]"
one_comma_in = r"[a-zçğüöıA-ZÇĞÜÖİ][^0-9]{1,},{1}.*[a-zçğüöıA-ZÇĞÜÖİ][^0-9]"
number = "\d*$"
in_quotes = r"[\"'`](.+?)[\"'`]"
quote_in = r"^[^\"'].*[\"'].*[^\"']$"
quote_initial = r"^[\"'`]{1}"
pat = r'[.?\-",]+'
PuncPattern = '|'.join(map(re.escape, punctuations))
####################

## Extended list of punctuations and others ##
parenthesis = ("(", ")", "{", "}", "[", "]")
quotes = ("\"", "'", "`", "”", "“")
roman = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "IXX",
        "XX", "XXX", "L", "LX", "LXX", "LXXX", "XC", "C", "D", "M")
alphabet = ("a", "b", "c", "ç", "d", "e", "f", "g", "ğ", "h", "ı", "i",
            "j", "k", "l", "m", "n", "o", "ö", "p", "r", "s", "ş", "t",
            "u", "ü", "v", "y", "z", "q", "w", "x",
            "A", "B", "C", "Ç", "D", "E", "F", "G", "Ğ", "H", "I", "İ",
            "J", "K", "L", "M", "N", "O", "Ö", "P", "R", "S", "Ş", "T",
            "U", "Ü", "V", "Y", "Z", "Q", "W", "X"
            )
numbers = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
exclamation_tweak = "(!)"
####################

class ts_check:
    def ts_tokenize(word) -> str:
        punc_count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
        punc_num = punc_count(word, string.punctuation)
# First check for any exception
####### ==> punctuation
        if punc_num == 1 and word in punctuations:
            return word.strip("\n"), "punctuation"
####### ==> abbr
        if word in abbrs:
            return word.strip("\n"), "abbr"
        if word+"." in abbrs:
            return word.strip("\n"), "abbr"
####### ==> emoji
        if word in emojis:
            return word.strip("\n"), "emoji"
###### ==> emoticon
        if word in emoticons:
            return word.strip("\n"), "emoticon"
####### ==> roman numeral
        if word in roman:
            return word.strip("\n"), "roman_numeral"
####### ==> e_mail
        if re.match(email_regex, word):
            return word.strip("\n"), "email"
####### ==> hashtag
        if re.match(hashtag, word):
            return word.strip("\n"), "hashtag"
####### ==> mention
        if re.match(mention, word):
            return word.strip("\n"), "mention"
####### ==> date
        if re.match(date_regex, word):
            return word.strip("\n"), "date"
####### ==> hour
        if re.match(hour_regex, word):
            return word.strip("\n"), "hour"
####### ==> number
        if re.match(number, word):
            return word.strip("\n"), "number"
####### ==> url
        if re.match(url_regex, word):
            return word.strip("\n"), "url"
####### ==> www_url
        if re.match(www_url_regex, word):
            return word.strip("\n"), "www_url"
####### ==> ip_addr
        if re.match(ip_addr, word):
            return word.strip("\n"), "ip_addr"
####### ==> comma_separated_number
        if re.match(comma_separated_number, word):
            return word.strip("\n"), "comma_separated_number"
####### ==> dot_separated_number
        if re.match(dot_separated_number, word):
            return word.strip("\n"), "dot_separated_number"
####### ==> breadcrumb
        if str(word).count("/") >= 2 and word[0:3] != "http":
            return word.strip("\n"), "breadcrumb"
        if str(word).count(">") >= 2 and word[0:3] != "http":
            return word.strip("\n"), "breadcrumb"
####### ==> exclamation_tweak_alone
        if str(word) == exclamation_tweak:
            return word.strip("\n"), "exclamation_tweak_alone"
####### ==> exclamation_tweak_word
        if str(word[-3:]) == exclamation_tweak:
            return word, "exclamation_tweak_word"
####### ==> in_parenthesis
        if str(word[0]) in parenthesis and str(word[-1]) in parenthesis:
            return word, "in_parenthesis"
####### ==> in_quotes
        if re.match(in_quotes, word):
            return word.strip("\n"), "in_quotes"
####### ==> punc_initial
        if punc_num == 1 and str(word[0]) in punctuations:
            return word.strip("\n"), "punc_initial"
####### ==> punc_final
        if punc_num == 1 and str(word[-1]) in punctuations:
            return word.strip("\n"), "punc_final"

        else:
            if str(word).lower() in ts_list:
                return word.strip("\n"), "token"
            else:
                return word.strip("\n"), "to_check"




