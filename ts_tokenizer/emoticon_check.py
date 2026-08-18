from .data import LocalData

class EmoticonParser:

    EMOJI_MODIFIER_RANGE = range(0x1F3FB, 0x1F400)
    VARIATION_SELECTORS = {"\uFE0E", "\uFE0F"}
    ZERO_WIDTH_JOINER = "\u200D"

    @classmethod
    def _is_emoji_base(cls, char):
        return char in LocalData.emoticons()

    @classmethod
    def _is_emoji_modifier(cls, char):
        return ord(char) in cls.EMOJI_MODIFIER_RANGE

    @classmethod
    def _consume_emoticon_cluster(cls, text, start_index):
        if start_index >= len(text) or not cls._is_emoji_base(text[start_index]):
            return None, start_index

        cluster = [text[start_index]]
        index = start_index + 1

        while index < len(text):
            char = text[index]

            if char in cls.VARIATION_SELECTORS or cls._is_emoji_modifier(char):
                cluster.append(char)
                index += 1
                continue

            if char == cls.ZERO_WIDTH_JOINER:
                if index + 1 < len(text) and cls._is_emoji_base(text[index + 1]):
                    cluster.append(char)
                    cluster.append(text[index + 1])
                    index += 2
                    continue
                break

            break

        return "".join(cluster), index

    @classmethod
    def emoticon_count(cls, word):
        emoticon_count = 0
        index = 0
        while index < len(word):
            cluster, next_index = cls._consume_emoticon_cluster(word, index)
            if cluster:
                emoticon_count += 1
                index = next_index
                continue
            index += 1
        return emoticon_count


    @classmethod
    def emoticon_check(cls, word):
        emoticon_count = cls.emoticon_count(word)
        return emoticon_count

    @classmethod
    def emoticon_tokenize(cls, text):
        tokens = []
        word = ""
        index = 0
        while index < len(text):
            cluster, next_index = cls._consume_emoticon_cluster(text, index)
            if cluster:
                if word:
                    tokens.append(word)
                    word = ""
                tokens.append(cluster)
                index = next_index
                continue

            word += text[index]
            index += 1

        if word:
            tokens.append(word)

        return "\n".join(tokens)
