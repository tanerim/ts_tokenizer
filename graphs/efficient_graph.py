import sys
import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import string
from multiprocessing import Pool
import plotly.express as px

puncs = string.punctuation


def extract_features(strings_batch):
    features = []
    for string in strings_batch:
        length = len(string)
        num_count = sum(char.isdigit() for char in string)
        punct_count = sum(char in puncs for char in string)

        # Initialize punctuation position features
        initial_punc = 0
        final_punc = 0
        between_punc = 0

        # Initialize punctuation type features
        punc_types = {
            'period': 0, 'comma': 0, 'semicolon': 0, 'colon': 0, 'exclamation': 0,
            'question': 0, 'parentheses': 0, 'brackets': 0, 'braces': 0
        }

        if len(string) > 0:
            if string[0] in puncs:
                initial_punc = 1
            if string[-1] in puncs:
                final_punc = 1
            for i, char in enumerate(string[1:-1], start=1):
                if char in puncs:
                    between_punc += 1

                    # Increment specific punctuation type count
                    if char == '.':
                        punc_types['period'] += 1
                    elif char == ',':
                        punc_types['comma'] += 1
                    elif char == ';':
                        punc_types['semicolon'] += 1
                    elif char == ':':
                        punc_types['colon'] += 1
                    elif char == '!':
                        punc_types['exclamation'] += 1
                    elif char == '?':
                        punc_types['question'] += 1
                    elif char in '()':
                        punc_types['parentheses'] += 1
                    elif char in '[]':
                        punc_types['brackets'] += 1
                    elif char in '{}':
                        punc_types['braces'] += 1

        # Combine all features into a single list
        feature_vector = [length, num_count, punct_count, initial_punc, final_punc, between_punc] + list(punc_types.values())
        features.append(feature_vector)

    return np.array(features)


# Function to process tokens in batches
def process_batch(strings_batch):
    features = extract_features(strings_batch)
    return features


# Load and split tokens into manageable batches
batch_size = 1_000_000  # Adjust this size based on memory limits
tokens = open(sys.argv[1]).read().split("\n")
batches = [tokens[i:i + batch_size] for i in range(0, len(tokens), batch_size)]

# Use multiprocessing to parallelize feature extraction
with Pool() as pool:
    features_list = pool.map(process_batch, batches)

# Concatenate all features from batches
all_features = np.vstack(features_list)

# Standardize features
scaler = StandardScaler()
all_features_scaled = scaler.fit_transform(all_features)

# Perform MiniBatchKMeans (more efficient for large data)
n_clusters = 7
kmeans = MiniBatchKMeans(n_clusters=n_clusters, batch_size=100_000_000)
kmeans.fit(all_features_scaled)

# Use t-SNE for dimensionality reduction (for a sample of the data)
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=1000)
tsne_result = tsne.fit_transform(all_features_scaled[:1_000_000])  # Visualize only a sample

# Interactive Plotly visualization with hover data (showing the actual tokens)
fig = px.scatter(
    x=tsne_result[:, 0],
    y=tsne_result[:, 1],
    color=kmeans.labels_[:1_000_000],
    hover_name=tokens[:1_000_000],  # Display actual tokens when hovering
    title="t-SNE of Sampled Clusters with Token Hover",
    labels={"x": "t-SNE Component 1", "y": "t-SNE Component 2"},
)

# Show the interactive plot
fig.show()
