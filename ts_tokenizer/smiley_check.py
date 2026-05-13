from .data import LocalData


class SmileyParser:
    @classmethod
    def sorted_smileys(cls):
        return sorted(LocalData.smileys(), key=lambda smiley: (-len(smiley), smiley))

    @classmethod
    def smiley_count(cls, text):
        smiley_count = 0
        for smiley in cls.sorted_smileys():
            smiley_count += text.count(smiley)
        return smiley_count

    @classmethod
    def smiley_split(cls, text):
        segments = []
        i = 0
        while i < len(text):
            matched_smiley = None
            for smiley in cls.sorted_smileys():
                if text.startswith(smiley, i):
                    matched_smiley = smiley
                    break

            if matched_smiley:
                segments.append((matched_smiley, True))
                i += len(matched_smiley)
                continue

            start = i
            i += 1
            while i < len(text):
                if any(text.startswith(smiley, i) for smiley in cls.sorted_smileys()):
                    break
                i += 1
            segments.append((text[start:i], False))

        return segments

    @classmethod
    def smiley_tokenize(cls, text):
        tokenized = [segment for segment, is_smiley in cls.smiley_split(text) if is_smiley]
        return "\n".join(tokenized)

    @classmethod
    def consecutive_smiley(cls, text):
        if not text:
            return False

        segments = cls.smiley_split(text)
        return len(segments) > 1 and all(is_smiley for _, is_smiley in segments)
