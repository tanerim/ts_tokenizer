from ts_tokenizer.data import word_list
from ts_tokenizer.char_fix import CharFix
from ts_tokenizer.tokenizer import tokenize

line = "A_a1daki maddeyi okuyun! FEN kurallar1na ayk1r1 olarak yap1lm1_ binalara Yap1 Kay1t Belgesi verildi + Yap1 depreme dayan1ks1zsa, sorumluluk malikte denildi¶ 0ktidar, y1k1l1rsa sorumlu sizsiniz dedi ve ~5 milyar$ tahsil etti+2018 seçimlerinde oy için yap1ld1"

tok_line = tokenize(line, "lines")

fixed_tweet = []

def replace_patterns(word):
    # Define all the possible replacements in order of priority
    replacements = [
        ("1ks1", "ıksı"),
        ("A_a1", "Aşağı"),
        ("1_", "ış"),
        ("1", "ı")
    ]

    # Apply all replacements iteratively
    for old, new in replacements:
        word = word.replace(old, new)
    return word


for word in line.split():
    word = word.replace(",", " ,")


    # First, check the word itself in word_list
    if CharFix.tr_lowercase(word) in word_list:
        fixed_tweet.append(word)
    else:
        # Apply replacements and check the transformed word
        transformed_word = replace_patterns(word)
        if CharFix.tr_lowercase(transformed_word) in word_list:
            fixed_tweet.append(transformed_word)
        else:
            # If no match, just keep the original word
            fixed_tweet.append(word)

print(" ".join(fixed_tweet))
