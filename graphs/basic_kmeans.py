import sys
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import string
import seaborn as sns
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


# Read input strings (assumed to be one word per line)
strings = open(sys.argv[1]).read().split("\n")
puncs = string.punctuation

# Function to extract features from strings
def extract_features(strings):
    features = []
    for string in strings:
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

        # Combine all features into a single list (including punctuation types)
        feature_vector = [
            length, num_count, punct_count, initial_punc, final_punc, between_punc
        ] + list(punc_types.values())
        features.append(feature_vector)

    return np.array(features)

# Extract features
features = extract_features(strings)

# Define feature names (adding punctuation type names)
feature_names = [
    "length", "num_count", "punct_count", "initial_punc", "final_punc", "between_punc",
    "period", "comma", "semicolon", "colon", "exclamation", "question", "parentheses", "brackets", "braces"
]

# Create a DataFrame for easier visualization
df = pd.DataFrame(features, columns=feature_names)

# Visualize the distribution of each feature
plt.figure(figsize=(10, 6))
sns.histplot(data=df, kde=True)
plt.title('Feature Distributions')
plt.show()

# Standardize features for clustering
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Visualize heatmap of features
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', linewidths=.5, xticklabels=feature_names, yticklabels=feature_names)
plt.title('Feature Correlation Heatmap')
plt.show()

# Elbow Method for optimal clusters
distortions = []
K = range(1, 10)
for k in K:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(features_scaled)
    distortions.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K, distortions, 'bx-')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
plt.title('Elbow Method showing the optimal k')
plt.show()

# Perform KMeans with optimal clusters (adjust this based on Elbow Method result)
n_clusters = 7
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(features_scaled)

# Get cluster labels
labels = kmeans.labels_

# Print some strings from each cluster
for i in range(n_clusters):
    cluster_strings = [strings[j] for j in range(len(strings)) if labels[j] == i]
    print(f"Cluster {i}:")
    print("Sample strings:", cluster_strings[:5])  # print first 5 samples from each cluster

# Visualize the silhouette score
silhouette_avg = silhouette_score(features_scaled, labels)
print(f"Silhouette Score: {silhouette_avg}")

# Visualizing clusters with PCA (2D Projection)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(features_scaled)
plt.figure(figsize=(10, 7))
plt.scatter(pca_result[:, 0], pca_result[:, 1], c=labels, cmap='tab10')
plt.title('PCA of Clusters')
plt.show()

# Visualizing clusters with t-SNE (2D Projection)
tsne = TSNE(n_components=2)
tsne_result = tsne.fit_transform(features_scaled)
plt.figure(figsize=(10, 7))
plt.scatter(tsne_result[:, 0], tsne_result[:, 1], c=labels, cmap='tab10')
plt.title('t-SNE of Clusters')
plt.show()
