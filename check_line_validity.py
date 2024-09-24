from ts_tokenizer.token_check import TokenCheck
import sys

in_file = open(sys.argv[1]).readlines()

for line in in_file:
    valids = []
    oov = []
    for word in line.split():
        tag = TokenCheck.token_tagger(word)
        if tag == "Valid_Word":
            valids.append(word)
        else:
            oov.append(word)
    len_valid = len(valids)
    len_oov = len(oov)

    # Check if there are any words in total to avoid division by zero
    total_words = len_valid + len_oov
    if total_words > 0:
        valid_ratio = len_valid / total_words
        if valid_ratio >= 0.9:
            output = line + "\t" + str(valid_ratio)
            print(output.replace("\n", ""))
        else:
            output = line + "\t" + "Noisy_Data"
            print(output.replace("\n", ""))


