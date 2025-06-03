import sys
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from multiprocessing import Pool
import plotly.express as px
import re

# Türkçe dışı karakter kontrolü için uygun karakter kümesi
TURKISH_CHARS = set("abcçdefgğhıijklmnoöprsştuüvyzABCDEFGHIJKLMNOPQRSTUVWXYZÇĞİÖŞÜ")
PUNCS = set(string.punctuation)

# Öznitelik çıkarımı
def extract_features(batch):
    features = []
    for token in batch:
        length = len(token)
        num_count = sum(c.isdigit() for c in token)
        punct_count = sum(c in PUNCS for c in token)
        non_tr_chars = sum(c not in TURKISH_CHARS for c in token if c.isalpha())

        initial_punc = int(len(token) > 0 and token[0] in PUNCS)
        final_punc = int(len(token) > 0 and token[-1] in PUNCS)
        between_punc = sum(c in PUNCS for c in token[1:-1])

        punct_positions = [i/length for i, c in enumerate(token) if c in PUNCS] if punct_count > 0 else [0.0]
        punct_mean_pos = np.mean(punct_positions)

        features.append([
            length, num_count, punct_count,
            non_tr_chars, initial_punc, final_punc,
            between_punc, punct_mean_pos
        ])
    return np.array(features)

# Paralel işlem fonksiyonu
def process_batch(batch):
    return extract_features(batch)

# Veriyi oku
tokens = open(sys.argv[1], encoding='utf-8').read().splitlines()
batch_size = 500_000
batches = [tokens[i:i + batch_size] for i in range(0, len(tokens), batch_size)]

# Paralel öznitelik çıkarımı
with Pool() as pool:
    all_features = np.vstack(pool.map(process_batch, batches))

# Normalize et
scaler = StandardScaler()
features_scaled = scaler.fit_transform(all_features)

# Kümeleme
n_clusters = 7
kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=batch_size)
labels = kmeans.fit_predict(features_scaled)

# t-SNE (örnekle 1M)
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=1000)
sample_size = min(len(tokens), 1_000_000)
tsne_result = tsne.fit_transform(features_scaled[:sample_size])

# Görselleştir
fig = px.scatter(
    x=tsne_result[:, 0],
    y=tsne_result[:, 1],
    color=labels[:sample_size],
    hover_name=tokens[:sample_size],
    title="t-SNE: Gürültülü Dizilerin Küme Temsili",
    labels={"x": "t-SNE Bileşeni 1", "y": "t-SNE Bileşeni 2"}
)

fig.show()

np.save("features_scaled.npy", features_scaled)
np.save("labels.npy", labels)
with open("tokens.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(tokens))
