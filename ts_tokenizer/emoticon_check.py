from .data import LocalData


class EmoticonParser:

    @classmethod
    def emoticon_count(cls, word):
        emoticon_count = 0
        for emoticon in LocalData.emoticons():
            if emoticon in word:
                emoticon_count += 1
        return emoticon_count

    @classmethod
    def emoticon_check(cls, word):
        emoticon_count = cls.emoticon_count(word)
        return emoticon_count

    @classmethod
    def emoticon_tokenize(cls, text):
        tokens = []
        word = ""
        for char in text:
            if char in LocalData.emoticons():
                if word:
                    tokens.append(word)
                    word = ""
                tokens.append(char)
            else:
                word += char
        if word:
            tokens.append(word)

        return "\n".join(tokens)
