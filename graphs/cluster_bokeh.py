import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource
import numpy as np
import plotly.express as px

# Step 1: Read words from input file
words = open(sys.argv[1]).read().splitlines()

# Step 2: Feature Extraction
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 5))
X = vectorizer.fit_transform(words)

# Step 3: Clustering
n_clusters = 20  # Number of clusters, this can be adjusted
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans.fit(X)
labels = kmeans.labels_

# Step 4: Analyze Clusters
clustered_words = pd.DataFrame({'word': words, 'cluster': labels})
print(clustered_words.head())
clustered_words.to_csv('clustered_words.csv', index=False)

# Perform TruncatedSVD to reduce dimensions to 2D for visualization
svd = TruncatedSVD(n_components=2, random_state=0)
X_svd = svd.fit_transform(X)

# Add SVD results to the DataFrame
clustered_words['x'] = X_svd[:, 0]
clustered_words['y'] = X_svd[:, 1]

# Step 5: Visualization using Bokeh
# output_file("clustered_words.html")

# Define colors for each cluster
colors = np.array([
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
])

# Add a column to the DataFrame with the colors
clustered_words['color'] = [colors[label] for label in labels]

source = ColumnDataSource(clustered_words)

# Create the plot
p = figure(title="K-Means Clustering of Complex_Punc",
           x_axis_label='Component 1',
           y_axis_label='Component 2')

# Add points to the plot with cluster colors
p.scatter('x', 'y', source=source, color='color', legend_field='cluster', size=10)

# Add hover tool
hover = HoverTool()
hover.tooltips = [("Word", "@word"), ("Cluster", "@cluster")]
p.add_tools(hover)

# show(p)


# Perform TruncatedSVD to reduce dimensions to 2D for visualization
svd = TruncatedSVD(n_components=2, random_state=0)
X_svd = svd.fit_transform(X)

# Add SVD results to the DataFrame
clustered_words['x'] = X_svd[:, 0]
clustered_words['y'] = X_svd[:, 1]

# Step 5: Visualization using Plotly
fig = px.scatter(clustered_words, x='x', y='y', color='cluster', hover_data=['word'],
                 title="K-Means Clustering of Words")

fig.show()