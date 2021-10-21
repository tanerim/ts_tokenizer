import string
punctuations = ("\"", "'", "`", ".", ",", "!", "$", "%", "&", "*",
                "+", "-", "/", "\\", ":", ";", "<", ">", "=", "?",
                "~", "|", "^", "_")
quotes = ("\"", "'", "`", "”", "“")
TS_Word_List = open('TS_Corpus_Turkish_Word_List.txt', 'r').read().split("\n")
abbrs = open('abbr.txt', 'r').read().split("\n")

# Find the index of punctuation in given word
def find_punc_index(word):
    for punc in punctuations:
        punc_index = next((i for i, ch in enumerate(word) if ch in punc), None)
        if punc_index is not None:
            return punc_index

class split_tokens:
    # Completed #
    def in_quotes(word) -> str:
        if word[0] in quotes and word[-1] in quotes:
            return word[0], word[1:-1], word[-1]

    # Completed #
    def punc_initial(word) -> str:
        return word[0], word[1:]

    # Completed #
    def punc_final(word) -> str:
        return word[0:-1], word[-1]

    # Completed #
    def parenthesis(word) -> str:
        if word[-3:] != "(!)":
            part_1 = word[0]
            part_2 = word[1:-1]
            part_3 = word[-1]
            word = part_1, part_2, part_3
        else:
            part_1 = word[0]
            part_2 = word[1:-1]
            part_3 = word[-1]
            word = part_1, part_2, part_3
        return word

    # Completed #
    def multi_emoji(word) -> str:
        for emoji in word:
            print(emoji, "emoji")

    # Completed #
    def exclamation_tweak_word(word) -> str:
        part_1 = word[0:-3]
        part_2 = word[-3:]
        exclamation_tweak_tokenized = part_1, part_2
        return exclamation_tweak_tokenized
####################################################

    # Completed #
    def dot_in(word) -> str:
        word_split = word.split(".")
        the_dot = "."
        # If two pieces form a valid word eg. son.dan
        if str(word_split[0] + word_split[1]).lower() in TS_Word_List:
            part_1 = word_split[0]
            part_2 = word_split[1]
            word = part_1 + part_2
            return word

        # If (first piece and dot) in abbr list eg. Doç.Dr
        if word_split[0] + "." in abbrs:
            part_1 = word_split[0] + "."
            # "abbr"
            if word_split[1] in abbrs:
                part_2 = word_split[1]
                # "abbr"
            elif str(word_split[1]).lower() in TS_Word_List:
                part_2 = word_split[1]
                # "token"
            elif str(word_split[1]).lower() not in TS_Word_List:
                part_2 = word_split[1]
                # "OOV"
            word = (part_1, part_2)
            return ",".join(word).split(",")

        # If first piece in abbr list
        # TBMM.Yeni
        if word_split[0] in abbrs:
            part_1 = word_split[0]
            # "abbr"
            if word_split[1] in abbrs:
                part_2 = word_split[1]
                # "abbr"
            elif str(word_split[1]).lower() in TS_Word_List:
                part_2 = word_split[1]
                # "token"
            elif str(word_split[1]).lower() not in TS_Word_List:
                part_2 = word_split[1]
                # "OOV"
            word = (part_1, the_dot, part_2)
            return ",".join(word).split(",")

        # If first part is a valid token
        if str(word_split[0]).lower() in TS_Word_List:
            part_1 = word_split[0]
            # "token"
            if str(word_split[1]).lower() in TS_Word_List:
                part_2 = word_split[1]
                # "token"
            elif str(word_split[1]).lower() not in TS_Word_List:
                part_2 = word_split[1]
                # "OOV"
            word = (part_1, the_dot, part_2)
            return ",".join(word).split(",")

        # If first part is not a valid token
        if str(word_split[0]).lower() not in TS_Word_List:
            part_1 = word_split[0]
            # "OOV"
            if str(word_split[1]).lower() in TS_Word_List:
                part_2 = word_split[1]
                # "token"
            elif str(word_split[1]).lower() not in TS_Word_List:
                part_2 = word_split[1]
                #"OOV"
            word = (part_1, the_dot, part_2)
            return ",".join(word).split(",")
############################################

    # Completed #
    def comma_in(word) -> str:
        word_split = word.split(",")
        the_comma = ","

        # if first piece is token
        if word_split[0] in TS_Word_List:
            part_1 = word_split[0]
            # "token"
            if word_split[1] in abbrs:
                part_2 = word_split[1]
                # "abbr"
            if str(word_split[1]).lower() in TS_Word_List:
                part_2 = word_split[1]
                # "token"
            if str(word_split[1]).lower() not in TS_Word_List:
                part_2 = word_split[1]
                # "OOV"
            word = (part_1, the_comma, part_2)
            return word

        # if first piece is OOV
        if word_split[0] not in TS_Word_List:
            part_1 = word_split[0]
            # "OVV"
            if word_split[1] in abbrs:
                part_2 = word_split[1]
                # "abbr"
            if str(word_split[1]).lower() in TS_Word_List:
                part_2 = word_split[1]
                # "token"
            if str(word_split[1]).lower() not in TS_Word_List:
                part_2 = word_split[1]
                # "OOV"
            word = (part_1, the_comma, part_2)
            return word
##################################



    # Completed #
    def multi_punctuation(word) -> str:
        if word[-3:] == "(!)":
            return split_tokens.exclamation_tweak(word)
        else:
            punc_location = find_punc_index(word)
            part1 = word[0:punc_location]
            part2 = word[punc_location:]
            multi_punc_tokenized = part1,part2
            return (multi_punc_tokenized)
    ##################################

    def num_of_initial_punc(word):
        matches = []
        while True:
            for char in word:
                if char in punctuations:
                    matches.append(char)
            return len(matches)
#            else:
#                sil = len(matches)
#               return "".join(matches) + "\n" + word[sil:]