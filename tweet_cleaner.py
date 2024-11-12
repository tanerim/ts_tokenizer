from ts_tokenizer.data import word_list
from ts_tokenizer.char_fix import CharFix
from ts_tokenizer.tokenizer import tokenize
from ts_tokenizer.token_handler import TokenPreProcess
import sys
import re

f = open(sys.argv[1]).read().split("\n")

# Define the Roman numeral pattern.
pattern = re.compile(r'\b(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))\.?\b', re.IGNORECASE)

# Open the file safely using 'with'.
with open(sys.argv[1], 'r') as file:
    for line in file:
        # Find all Roman numeral matches in the line.
        matches = re.findall(pattern, line.strip())
        # Print only the full match (the first element of each tuple).
        for match in matches:
            print(match[0])


#for w in f:
#    y = TokenPreProcess.is_roman_number(w)
#    if y:
#        print(f"{w} ==> {y}")
