import logging
from ts_tokenizer.char_fix import CharFix

# Character replacements
reps = [("â", "a"), ("Â", "A"), ("î", "i"), ("Î", "İ"), ("û", "u"), ("Û", "U")]

# Setup logging to output both to CLI and to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("output"),  # Save output to 'output' file
        logging.StreamHandler()         # Also print to CLI
    ]
)

# Function to fix the word and check against the word list
def process_line(line, imlis):
    word = CharFix.fix(line)
    for old, new in reps:
        word = word.replace(old, new)
    if word in imlis:
        return line  # Return the original form of the input word
    return None

# Main function

# Read the input words and the word list to check against
input_words = open("ts_tokenizer/data/TS_Corpus_Turkish_Word_List.txt").read().split("\n")
imli_words = set(open("imli/all_imli_uniq").read().split("\n"))
u_words = []

# Loop over each word in the imli word list
for word in imli_words:
    if "î" in word:
        u_word = word.replace("û", "u")
        if u_word in input_words:
            u_words.append(word)
            print(word)


