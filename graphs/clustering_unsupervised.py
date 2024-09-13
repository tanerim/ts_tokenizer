import click
import re
import numpy
import random

from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


@click.command()
@click.argument('filename')
@click.option('--clusters', default=3, help='Number of clusters')
@click.option('--sample', default=100, help='Number of samples to print')
def cluster_lines(filename, clusters, sample):
    lines = numpy.array(list(_get_lines(filename)))

    doc_feat = TfidfVectorizer().fit_transform(lines)
    km = KMeans(clusters).fit(doc_feat)

    k = 0
    clusters = defaultdict(list)
    for i in km.labels_:
      clusters[i].append(lines[k])
      k += 1

    s_clusters = sorted(clusters.values(), key=lambda l: -len(l))

    for cluster in s_clusters:
        print 'Cluster [%s]:' % len(cluster)
        if len(cluster) > sample:
            cluster = random.sample(cluster, sample)
        for line in cluster:
            print line
        print '--------'


def _clean_line(line):
    line = line.strip().lower()
    line = re.sub('\d+', '(N)', line)
    return line


def _get_lines(filename):
    for line in open(filename).readlines():
        yield _clean_line(line)


if __name__ == '__main__':
    cluster_lines()
