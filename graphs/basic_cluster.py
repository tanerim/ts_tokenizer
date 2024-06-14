import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import plotly.express as px
from sklearn.decomposition import PCA

# Sample data
data = open(sys.argv[1]).read().splitlines()

# Convert the text data into TF-IDF features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data)

# Perform K-Means clustering
n_clusters = 10  # You can choose the number of clusters based on your data
kmeans = KMeans(n_clusters=n_clusters, random_state=2)
kmeans.fit(X)
labels = kmeans.labels_

# Reduce dimensions for visualization using PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X.toarray())

# Create a DataFrame for visualization
df = pd.DataFrame({
    'x': principal_components[:, 0],
    'y': principal_components[:, 1],
    'label': labels,
    'word': data
})

# Plot interactive visualization using Plotly
fig = px.scatter(df, x='x', y='y', color='label', text='word', title='Clusters of Misspelled Words')
fig.update_traces(marker=dict(size=12), textposition='top center')
fig.show()
