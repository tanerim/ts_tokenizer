from ts_tokenizer.token_handler import TokenPreProcess
from ts_tokenizer.char_fix import CharFix
word = '<text id="0012">'
print(TokenPreProcess.is_xml(word))

print(CharFix.fix(word))


