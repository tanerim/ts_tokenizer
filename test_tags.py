import re
import sys
import string

# Define punctuation list including extra punctuation characters
puncs = re.escape(string.punctuation)
extra_puncs = ["–", "°", "—", "(", ")"]
puncs += re.escape(''.join(extra_puncs))

# Regular expression to match lines ending with two or more punctuation marks
pattern = re.compile(rf"[{puncs}]{{2,}}$")

# Read the file from command-line argument
f = open(sys.argv[1]).read().split("\n")

# Loop through lines and find those ending with two or more punctuation marks
for line in f:
    if pattern.search(line):
        print(line)
