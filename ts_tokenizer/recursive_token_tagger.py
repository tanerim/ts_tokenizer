from token_preprocess import TokenPreProcess
def recursive_token_tagger(token):
    tagged_tokens = []
    if TokenPreProcess.is_in_parenthesis(token):
        print(token)
        recursive_process = "Parse token"
        return recursive_process, tagged_tokens

print(recursive_token_tagger("(2024)"))