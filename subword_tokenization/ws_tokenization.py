# cumle = "Defne kahvaltısını yaptı, sonra okula gitti."
cumle = "Defne okulda e-posta göndermeyi öğrenmiş."
# boşluk karakterini yeni satır karakteriyle değiştir
ws_tokenized = cumle.replace(" ", "\n")
print(ws_tokenized)

import re

cumle = "Defne okulda e-posta göndermeyi öğrenmiş."
# Noktalama işaretlerini kelimelerden ayır ve her bir tokenı yeni satıra yaz
tokens = re.findall(r"\w+|[^\w\s]", cumle)
tokens_2 = re.findall(r"\w+|[.,!?;]", cumle)
ws_tokenized = "\n".join(tokens)
ws_tokenized_2 = "\n".join(tokens_2)
print("#" * 20)

print(ws_tokenized)
print("#" * 20)
print(ws_tokenized_2)

print("#" * 20)


import string

cumle = "Defne okulda e-posta göndermeyi öğrenmiş."
tokens = []
token = ""

for char in cumle:
    if char in string.punctuation:
        if token:
            tokens.append(token)
            token = ""
        tokens.append(char)  # Noktalama işaretini ayrı bir token olarak ekle
    elif char.isspace():
        if token:
            tokens.append(token)
            token = ""
    else:
        token += char

if token:  # Son token varsa ekle
    tokens.append(token)

# Her tokenı satıra yaz
print("\n".join(tokens))


dictionary = {"Defne", "kahvaltı", "yaptı", "sonra", "okul", "git"}
cumle = "Defne kahvaltısını yaptı, sonra okula gitti."
tokens = cumle.split()
matched = []
for token in tokens:
   if token in dictionary:
       matched.append(token)
   else:
       matched.append("[OOV]")
print("\n".join(matched))
