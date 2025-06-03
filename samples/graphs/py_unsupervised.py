import numpy as np
import pandas as pd

# Data Path
features = np.load("features_scaled.npy")  # Normalize edilmiş öznitelikler
labels = np.load("labels.npy")  # Küme etiketleri
tokens = open("tokens.txt", encoding="utf-8").read().splitlines()  # Diziler

# Feature Set
columns = [
    "length", "num_count", "punct_count", "non_tr_chars",
    "initial_punc", "final_punc", "between_punc", "punct_mean_pos"
]

# Generate DataFrame
df = pd.DataFrame(features, columns=columns)
df["label"] = labels
df["token"] = tokens

table_rows = []

# Number of Clusters
n_clusters = len(np.unique(labels))

for i in range(n_clusters):
    cluster_df = df[df["label"] == i]
    sample_tokens = cluster_df["token"].sample(min(5, len(cluster_df)), random_state=42).tolist()

    row = {
        "Küme": i,
        "Dizi Sayısı": len(cluster_df),
        "Ortalama Uzunluk": round(cluster_df["length"].mean(), 2),
        "Sayı İçerme": round(cluster_df["num_count"].mean(), 2),
        "Punct. Sayısı": round(cluster_df["punct_count"].mean(), 2),
        "Türkçe Dışı Karakter": round(cluster_df["non_tr_chars"].mean(), 2),
        "Başta Punct.": round(cluster_df["initial_punc"].mean(), 2),
        "Sonda Punct.": round(cluster_df["final_punc"].mean(), 2),
        "Ortalama Punct. Konumu": round(cluster_df["punct_mean_pos"].mean(), 2),
        "Örnek Diziler": ", ".join(sample_tokens)
    }

    table_rows.append(row)

# Generate Final DF
table_df = pd.DataFrame(table_rows)

# Save as CSV
table_df.to_csv("tablo7.csv", index=False)

print(table_df.to_string(index=False))
