import sys
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, normalizers
from tokenizers.normalizers import NFC, Lowercase

# Get vocabulary size from user
vocab_size = int(input("Vocabulary Size: \n"))

# Load and normalize the corpus
corpus = []
with open(sys.argv[1], encoding="utf-8") as f:
    for line in f:
        corpus.append(line.strip())

# Initialize WordPiece tokenizer
tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
tokenizer.normalizer = normalizers.Sequence([NFC(), Lowercase()])
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

# Train tokenizer
trainer = trainers.WordPieceTrainer(
    vocab_size=vocab_size,
    show_progress=True,
    special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
)
tokenizer.train_from_iterator(corpus, trainer)

# Save tokenizer to JSON
tokenizer.save(f"turkish_wordpiece_tokenizer_{vocab_size}.json")

# Export vocabulary
vocab = tokenizer.get_vocab()
sorted_vocab = sorted(vocab.items(), key=lambda x: x[1])  # sort by token ID

with open(f"turkish_wordpiece_{vocab_size}.txt", "w", encoding="utf-8") as f:
    for token, idx in sorted_vocab:
        f.write(f"{token}\t{idx}\n")
