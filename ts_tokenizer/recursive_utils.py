def mssp_recursive(token):
    tokens = []
    initial_punc = token[0]
    tokens.append((initial_punc, "Punc"))
    final_punc = token[-1]
    tokens.append((final_punc, "Punc"))
    token = token[1:-1]
    from ts_tokenizer.token_processor import TokenProcessor
    tokens.append((TokenProcessor.process_token(token)[0], TokenProcessor.process_token(token)[1]))
    return tokens


print(mssp_recursive(".yeni."))