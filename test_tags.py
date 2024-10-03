import string

def split_punc_and_email(s):
    puncs = string.punctuation
    i = 0
    # Split the prefix punctuation
    while i < len(s) and s[i] in puncs:
        i += 1
    # Split the suffix punctuation
    j = len(s) - 1
    while j >= 0 and s[j] in puncs:
        j -= 1
    # Return the split parts
    return s[:i], s[i:j+1], s[j+1:]

# Test case
s = '(yeni@eski.com)'
prefix, email, suffix = split_punc_and_email(s)
print(prefix)  # Output: (
print(email)   # Output: yeni@eski.com
print(suffix)  # Output: )
