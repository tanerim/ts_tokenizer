from ts_tokenizer.tokenizer import tokenize


def tagged_lines(text):
    return [tuple(line.split("\t")) for line in tokenize(text, "tagged").splitlines()]


def test_smiley_attached_to_word_start():
    assert tagged_lines(":)))ama") == [(":)))", "Smiley"), ("ama", "Valid_Word")]
    assert tagged_lines(":))ama") == [(":))", "Smiley"), ("ama", "Valid_Word")]
    assert tagged_lines(":)ama") == [(":)", "Smiley"), ("ama", "Valid_Word")]


def test_smiley_attached_to_word_end():
    assert tagged_lines("ama:)") == [("ama", "Valid_Word"), (":)", "Smiley")]
    assert tagged_lines("ama:))") == [("ama", "Valid_Word"), (":))", "Smiley")]


def test_smiley_attached_to_word_with_trailing_punctuation():
    assert tagged_lines("ama:))!") == [
        ("ama", "Valid_Word"),
        (":))", "Smiley"),
        ("!", "Punc"),
    ]


def test_emoticon_attached_to_word_start():
    assert tagged_lines("🚨🚨🚨ADIYAMAN") == [
        ("🚨", "Emoticon"),
        ("🚨", "Emoticon"),
        ("🚨", "Emoticon"),
        ("ADIYAMAN", "Valid_Word"),
    ]
