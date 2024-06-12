import sys
import numpy as np
import re
import pandas as pd
import string
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from multiprocessing import Pool, cpu_count

puncs = string.punctuation
pd.set_option('display.max_rows', None)


def read_file(filename):
    """Read words from a file, each word per line."""
    with open(filename, 'r') as file:
        words = file.read().splitlines()
    return words


def extract_features_segment(tokens):
    features = []
    for token in tokens:
        length = len(token)
        digit_count = len(re.findall(r'\d', token))
        punc_count = len(re.findall(r'[^\w\s]', token))
        first_punc_pos = next((i for i, char in enumerate(token) if re.match(r'[^\w\s]', char)), -1)
        last_punc_pos = next((i for i, char in enumerate(reversed(token)) if re.match(r'[^\w\s]', char)), -1)
        parenthesis_count = len(re.findall(r'[()]', token))
        digit_proportion = digit_count / length if length > 0 else 0
        punc_proportion = punc_count / length if length > 0 else 0
        starts_with_digit = 1 if token and token[0].isdigit() else 0
        ends_with_digit = 1 if token and token[-1].isdigit() else 0
        consecutive_punc = max(len(m) for m in re.findall(r'[^\w\s]+', token)) if re.findall(r'[^\w\s]+', token) else 0
        consecutive_digits = max(len(m) for m in re.findall(r'\d+', token)) if re.findall(r'\d+', token) else 0

        feature_vector = [length, digit_count, punc_count, first_punc_pos, last_punc_pos, parenthesis_count, digit_proportion,
                          punc_proportion,  starts_with_digit, ends_with_digit, consecutive_punc, consecutive_digits]

        features.append(feature_vector)
    return np.array(features)


def extract_features(tokens):
    cores = cpu_count()
    pool = Pool(cores)
    chunk_size = len(tokens) // cores
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
    results = pool.map(extract_features_segment, chunks)
    pool.close()
    pool.join()
    return np.vstack(results)


def find_optimal_clusters(data):
    """Use the elbow method to find the optimal number of clusters."""
    distortions = []
    ks = range(1, 12)
    for k in ks:
        kmean_model = KMeans(n_clusters=k)
        kmean_model.fit(data)
        distortions.append(kmean_model.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(ks, distortions, 'bx-')
    plt.xlabel('kümeler')
    plt.ylabel('Dağılım')
    plt.title('Elbow Metodu ile Anlamlı Kırılım Dağılımının Belirlenmesi')
    plt.show()


def perform_clustering(data, n_clusters):
    """Cluster the data and return labels, centroids, and word-cluster mapping."""
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    word_cluster_map = dict(zip(range(len(data)), labels))

    return labels, centroids, word_cluster_map


def plot_cluster_heatmap(labels, features, title="Cluster Heatmap"):
    """Creates a heatmap showing the distribution of features across clusters."""
    # Create a DataFrame with labels and features
    df = pd.DataFrame(features)
    df['Cluster'] = labels
    # Calculate the means of features for each cluster
    cluster_means = df.groupby('Cluster').mean()
    # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(cluster_means, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title(title)
    plt.ylabel('Cluster')
    plt.xlabel('Feature Index')
    plt.show()


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    words = read_file(sys.argv[1])
    features = extract_features(words)
    # labels, centers = perform_clustering(features, n_clusters=12)  # Adjust the number of clusters as needed
    labels, centers, word_cluster_map = perform_clustering(features, n_clusters=12)
    find_optimal_clusters(features)
    # plot_cluster_heatmap(labels, features)
    # Print word-cluster associations

    for word_index, cluster_label in word_cluster_map.items():
        print(f"{word_index} \t {words[word_index]} \t {cluster_label}")


if __name__ == "__main__":
    main()
