import sys
import re
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from bokeh.plotting import figure, show, output_file
from bokeh.io import push_notebook, output_notebook
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Category20
from ts_tokenizer.data import LocalData
from ts_tokenizer.token_handler import TokenPreProcess
from ts_tokenizer.token_check import TokenCheck

valids = open(sys.argv[2]).read().splitlines()

def extract_features(tokens):
    features = []
    for token in tokens:
        validation = 1 if token in valids else 0
        # Feature 1: Length of the token
        length = len(token)
        # Feature 2: Count of digits
        digit_count = len(re.findall(r'\d', token))
        # Feature 3: Count of punctuation
        punc_count = len(re.findall(r'[^\w\s]', token))
        # Feature 4: Presence of HTML entities
        html_entity = 1 if re.search(r'&[a-z]+;', token) else 0
        # Feature 5: Presence of non-ASCII characters
        non_ascii = 1 if re.search(r'[^\x00-\x7F]', token) else 0
        # Feature 6: Position of the first punctuation mark
        first_punc_pos = next((i for i, char in enumerate(token) if re.match(r'[^\w\s]', char)), -1)
        # Feature 7: Position of the last punctuation mark
        last_punc_pos = next((i for i, char in enumerate(reversed(token)) if re.match(r'[^\w\s]', char)), -1)
        last_punc_pos = len(token) - 1 - last_punc_pos if last_punc_pos != -1 else -1
        # Feature 8: Parenthesis count
        parenthesis_count = len(re.findall(r'[()]', token))
        # Feature 9: Proportion of digits
        digit_proportion = digit_count / length if length > 0 else 0
        # Feature 10: Proportion of punctuation
        punc_proportion = punc_count / length if length > 0 else 0
        # Feature 11: Proportion of uppercase characters
        upper_count = len(re.findall(r'[A-Z]', token))
        upper_proportion = upper_count / length if length > 0 else 0
        # Feature 12: Count of vowels
        vowel_count = len(re.findall(r'[aeiouAEIOU]', token))
        # Feature 13: Count of consonants
        consonant_count = len(re.findall(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]', token))
        # Feature 14: Starts with digit
        starts_with_digit = 1 if token and token[0].isdigit() else 0
        # Feature 15: Ends with digit
        ends_with_digit = 1 if token and token[-1].isdigit() else 0
        # Feature 16: Contains uppercase characters
        contains_upper = 1 if re.search(r'[A-Z]', token) else 0
        # Feature 17: Consecutive punctuation
        consecutive_punc = max(len(m) for m in re.findall(r'[^\w\s]+', token)) if re.findall(r'[^\w\s]+', token) else 0
        # Feature 18: Consecutive digits
        consecutive_digits = max(len(m) for m in re.findall(r'\d+', token)) if re.findall(r'\d+', token) else 0
        # Feature 19: Consecutive letters
        consecutive_letters = max(len(m) for m in re.findall(r'[a-zA-Z]+', token)) if re.findall(r'[a-zA-Z]+', token) else 0

        features.append([validation,
            length, digit_count, punc_count, html_entity, non_ascii, first_punc_pos, last_punc_pos,
            parenthesis_count, digit_proportion, punc_proportion, upper_proportion, vowel_count,
            consonant_count, starts_with_digit, ends_with_digit, contains_upper, consecutive_punc,
            consecutive_digits, consecutive_letters
        ])

    return np.array(features)


def tokenize_and_classify(tokens):
    features = extract_features(tokens)

    # Standardize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=18, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)

    return clusters, features_scaled


if __name__ == "__main__":
    sample_words = []
    f = open(sys.argv[1], 'r', encoding='utf-8').read().split("\n")
    for word in f:
        sample_words.append(word)
    clusters, features_scaled = tokenize_and_classify(sample_words)

    num_clusters = 18
    cluster_counts = {i: 0 for i in range(num_clusters)}
    cluster_samples = {i: [] for i in range(num_clusters)}

    for word, cluster in zip(sample_words, clusters):
        cluster_counts[cluster] += 1
        if len(cluster_samples[cluster]) < 3:
            cluster_samples[cluster].append(word)

    # Bokeh visualization
    source = ColumnDataSource(data=dict(
        x=features_scaled[:, 0],
        y=features_scaled[:, 1],
        color=[Category20[20][i % 20] for i in clusters],
        label=[str(cluster) for cluster in clusters],
        word=sample_words
    ))

    TOOLTIPS = [
        ("Word", "@word"),
        ("Cluster", "@label")
    ]

    p = figure(title="Clusters of Tokens", tools="pan,wheel_zoom,reset,hover", tooltips=TOOLTIPS)
    p.scatter('x', 'y', color='color', legend_field='label', source=source, size=8)

    p.legend.title = "Cluster"
    p.xaxis.axis_label = "Feature 1 (Standardized)"
    p.yaxis.axis_label = "Feature 2 (Standardized)"

    show(p)
