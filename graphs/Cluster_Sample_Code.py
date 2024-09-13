import os
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import numpy as np
from sklearn.cluster import MeanShift # as ms
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import tree
import pandas as pd
style.use('ggplot')



f = open(sys.argv[1])
my_data = f.readlines()

g = open(sys.argv[2])
tr_stop = g.read().split()


#print tr_stop

vectorizer = TfidfVectorizer(stop_words=tr_stop)
X = vectorizer.fit_transform(my_data)

#number of clusters
true_k = 4
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=3000, n_init=1)
model.fit(X)


cluster_number = true_k

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
#print terms

for i in range(true_k):
    print ("Cluster %d:" % i,)
#set number of items in each cluster
    for ind in order_centroids[i, :20]:
        print (u"%s" % terms[ind],)
    print ()

### Prints a basic graph###
xs = order_centroids[:,25]
ys = order_centroids[:,0]
plt.scatter(xs, ys, c='black', s=10)
plt.show()


pl.figure('K-means with 3 clusters')
pl.scatter(pca_2d[:, 0], pca_2d[:, 1], c=kmeans.labels_, cmap='rainbow')
pl.show()

