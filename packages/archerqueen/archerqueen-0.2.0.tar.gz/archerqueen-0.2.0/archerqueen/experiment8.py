import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Generate a synthetic dataset
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=42)
X = StandardScaler().fit_transform(X)

# Visualize the original dataset
plt.scatter(X[:, 0], X[:, 1], s=50, c='gray', label='Data Points')
plt.title('Original Dataset')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()

# Apply K-Means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans_labels = kmeans.fit_predict(X)

# Visualize K-Means clustering
plt.scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='viridis', s=50)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='red', label='Centroids')
plt.title('K-Means Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()

# Apply DBSCAN clustering
dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(X)

# Visualize DBSCAN clustering
plt.scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap='plasma', s=50)
plt.title('DBSCAN Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

# Silhouette Scores
kmeans_silhouette = silhouette_score(X, kmeans_labels)
dbscan_silhouette = silhouette_score(X, dbscan_labels)

print(f"Silhouette Score for K-Means: {kmeans_silhouette:.2f}")
print(f"Silhouette Score for DBSCAN: {dbscan_silhouette:.2f} (if applicable)")
