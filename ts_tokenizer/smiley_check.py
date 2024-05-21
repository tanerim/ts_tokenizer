from .data import LocalData


class SmileyParser:
    @classmethod
    def smiley_count(cls, text):
        smiley_count = 0
        for smiley in LocalData.smileys():
            smiley_count += text.count(smiley)
        return smiley_count

    @classmethod
    def smiley_tokenize(cls, text):
        tokenized = []
        i = 0
        while i < len(text):
            found_smiley = False
            for smiley in LocalData.smileys():
                if text[i:i+len(smiley)] == smiley:
                    tokenized.append(smiley)
                    i += len(smiley)
                    found_smiley = True
                    break
            if not found_smiley:
                i += 1
        return "\n".join(tokenized)

    @classmethod
    def consecutive_smiley(cls, text):
        if not text:
            return False

        found_smileys = []
        i = 0
        while i < len(text):
            for smiley in LocalData.smileys():
                if text[i:i + len(smiley)] == smiley:
                    found_smileys.append((i, smiley))
                    i += len(smiley) - 1  # Adjust index to continue after the current smiley
                    break
            i += 1

        if len(found_smileys) <= 1:
            return False

        for i in range(1, len(found_smileys)):
            # Check if the current smiley starts immediately after the previous one
            if found_smileys[i][0] != found_smileys[i - 1][0] + len(found_smileys[i - 1][1]):
                return False
        return True
