import numpy as np
import pandas as pd

# Data Path
features = np.load("features_scaled.npy")  # Normalized Features
labels = np.load("labels.npy")  # Cluster Labels
tokens = open("tokens.txt", encoding="utf-8").read().splitlines()  # Strings

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
        "Cluster": i,
        "Length": len(cluster_df),
        "Average Length": round(cluster_df["length"].mean(), 2),
        "Number Existence": round(cluster_df["num_count"].mean(), 2),
        "Punct Count": round(cluster_df["punct_count"].mean(), 2),
        "Non-Turkish Chars": round(cluster_df["non_tr_chars"].mean(), 2),
        "Initial Punct": round(cluster_df["initial_punc"].mean(), 2),
        "Final Punct": round(cluster_df["final_punc"].mean(), 2),
        "Average Punct": round(cluster_df["punct_mean_pos"].mean(), 2),
        "Sample Strings": ", ".join(sample_tokens)
    }

    table_rows.append(row)

# Generate Final DF
table_df = pd.DataFrame(table_rows)

# Save as CSV
table_df.to_csv("tablo.csv", index=False)

print(table_df.to_string(index=False))
