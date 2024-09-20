from .token_check import TokenCheck

def recursive_token_tagger(token):
    tagged_tokens = []
    tag = TokenCheck.token_tagger(token)
    if tag is not None:
        if tag == "MSSP":
            tagged_tokens.append(token)
            return tagged_tokens

print(recursive_token_tagger("(2024)"))