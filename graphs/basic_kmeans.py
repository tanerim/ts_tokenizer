import sys
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import string
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

# Enable interactive mode
# plt.ioff()

pd.set_option('display.max_rows', None)
# Assume you have a list of strings
strings = open(sys.argv[1]).read().split("\n")
puncs= string.punctuation
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

        # Combine all features into a single list
        # feature_vector = [length, num_count, punct_count, initial_punc, final_punc, between_punc] + list(punc_types.values())
        feature_vector = [length, num_count, punct_count, initial_punc, final_punc, between_punc]
        features.append(feature_vector)

    return np.array(features)

# Extract features
features = extract_features(strings)
# feature_names = [
#    "length", "num_count", "punct_count", "initial_punc", "final_punc", "between_punc",
#    "period", "comma", "semicolon", "colon", "exclamation", "question", "parentheses", "brackets", "braces"
# ]
feature_names = ["length", "num_count", "punct_count", "initial_punc", "final_punc", "between_punc"]
df = pd.DataFrame(features, columns=feature_names)
# print(df.to_csv(sep="\t", index=False))
# Set up the matplotlib figure
plt.figure(figsize=(10, 8))

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(df, annot=True, fmt="d", cmap='coolwarm', linewidths=.5, xticklabels=feature_names, yticklabels=feature_names)

# Add labels and title, if needed
plt.title('Feature Heatmap')
plt.ylabel('Index of Entry')
plt.xlabel('Feature Type')

# Show plot
plt.show()


# Standardize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Set the number of clusters (at most the number of samples)
# n_clusters = min(len(strings), 7)
n_clusters = 7

# Perform K-means clustering
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(features_scaled)

# Get cluster labels
labels = kmeans.labels_

for i in range(n_clusters):
    cluster_strings = [strings[j] for j in range(len(strings)) if labels[j] == i]
    print(f"Cluster {i}:")
    print("Sample strings:", cluster_strings[:5])  # print first 5 samples from each cluster

cluster_names = {
    0: "Minimal_Punctuation",
    1: "High_Punctuation",
    2: "Mixed_Features",
    3: "Numeric_Strings",
    4: "Short_Texts",
    5: "Long_Texts"
}

# Print cluster labels for each string
# for string, label in zip(strings, labels):
#      print(f"{cluster_names[label]}\t{string}")

# Elbow Method
#wcss = []
#for i in range(1, 11):
#    kmeans = KMeans(n_clusters=i, random_state=42)
#    kmeans.fit(features_scaled)
#    wcss.append(kmeans.inertia_)

#plt.figure(figsize=(10, 5))
#plt.plot(range(1, 11), wcss, marker='o')
#plt.title('Elbow Method')
#plt.xlabel('Number of clusters')
#plt.ylabel('WCSS')
#plt.savefig('elbow_method.png')
#plt.show()

# # Silhouette Method
# silhouette_scores = []
# for i in range(2, 11):
#     kmeans = KMeans(n_clusters=i, random_state=42)
#     kmeans.fit(features_scaled)
#     score = silhouette_score(features_scaled, kmeans.labels_)
#     silhouette_scores.append(score)
#
# plt.figure(figsize=(10, 5))
# plt.plot(range(2, 11), silhouette_scores, marker='o')
# plt.title('Silhouette Method')
# plt.xlabel('Number of clusters')
# plt.ylabel('Silhouette Score')
# plt.show()
