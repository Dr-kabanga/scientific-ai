$Env:GITHUB_TOKEN = "github_pat_11BRN3D4Q07Wb0yV3RwCv4_2tRmioOcVy3xjojjhs
CHcCnE7umQoMUll6fRVGzsfx06QS3L3EUCuLx22rP"

# Publish Test Results to Azure Pipelines
- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit' # Specify the format of your test results.
    testResultsFiles: '**/TEST-*.xml' # Adjust the pattern to match your test result files.
    searchFolder: '$(System.DefaultWorkingDirectory)' # Optional: Specify the folder to search for test results.
    mergeTestResults: true # Merge test results from multiple files.
    failTaskOnFailedTests: true # Fail the task if there are test failures.
    testRunTitle: 'My Test Run' # Optional: Provide a title for the test run.
    publishRunAttachments: true # Upload test result files as attachments.

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Step 1: Load Genetic Data
def load_genetic_data(file_path):
    """
    Load genetic data from a CSV file.
    The file should contain columns like 'SampleID', 'Marker1', 'Marker2', ..., 'MarkerN'.
    """
    genetic_data = pd.read_csv(file_path)
    print(f"Loaded genetic data with {genetic_data.shape[0]} samples and {genetic_data.shape[1] - 1} markers.")
    return genetic_data

# Step 2: Load Linguistic Data
def load_linguistic_data(file_path):
    """
    Load linguistic data from a CSV file.
    The file should contain columns like 'Language', 'Feature1', 'Feature2', ..., 'FeatureN'.
    """
    linguistic_data = pd.read_csv(file_path)
    print(f"Loaded linguistic data with {linguistic_data.shape[0]} languages and {linguistic_data.shape[1] - 1} features.")
    return linguistic_data

# Step 3: Perform PCA on Genetic Data
def perform_pca(data, n_components=2):
    """
    Perform Principal Component Analysis (PCA) on the data.
    """
    pca = PCA(n_components=n_components)
    reduced_data = pca.fit_transform(data)
    print(f"Reduced data to {n_components} principal components.")
    return reduced_data

# Step 4: Cluster Genetic Data
def cluster_data(data, n_clusters=3):
    """
    Perform K-Means clustering on the data.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(data)
    print(f"Clustered data into {n_clusters} clusters.")
    return labels

# Step 5: Calculate Linguistic Similarity
def calculate_linguistic_similarity(data):
    """
    Calculate pairwise cosine similarity for linguistic features.
    """
    similarity_matrix = cosine_similarity(data)
    print("Calculated linguistic similarity matrix.")
    return similarity_matrix

# Step 6: Visualize Results
def visualize_results(genetic_data, genetic_labels, linguistic_similarity):
    """
    Visualize genetic clusters and linguistic similarity.
    """
    plt.figure(figsize=(12, 6))

    # Genetic Clusters
    plt.subplot(1, 2, 1)
    plt.scatter(genetic_data[:, 0], genetic_data[:, 1], c=genetic_labels, cmap='viridis', s=50)
    plt.title("Genetic Clusters")
    plt.xlabel("PC1")
    plt.ylabel("PC2")

    # Linguistic Similarity Heatmap
    plt.subplot(1, 2, 2)
    plt.imshow(linguistic_similarity, cmap='hot', interpolation='nearest')
    plt.title("Linguistic Similarity")
    plt.colorbar(label="Cosine Similarity")

    plt.tight_layout()
    plt.show()

# Main Function
if __name__ == "__main__":
    # File paths for genetic and linguistic data
    genetic_file = "genetic_data.csv"
    linguistic_file = "linguistic_data.csv"

    # Load data
    genetic_data = load_genetic_data(genetic_file)
    linguistic_data = load_linguistic_data(linguistic_file)

    # Perform PCA on genetic data
    genetic_features = genetic_data.iloc[:, 1:].values  # Exclude SampleID
    reduced_genetic_data = perform_pca(genetic_features)

    # Cluster genetic data
    genetic_labels = cluster_data(reduced_genetic_data)

    # Calculate linguistic similarity
    linguistic_features = linguistic_data.iloc[:, 1:].values  # Exclude Language
    linguistic_similarity = calculate_linguistic_similarity(linguistic_features)

    # Visualize results
    visualize_results(reduced_genetic_data, genetic_labels, linguistic_similarity)

# Example genetic data
example_genetic_data = """
individual_id,marker_1,marker_2,marker_3,marker_4,marker_5
1,0.1,0.3,0.5,0.7,0.9
2,0.2,0.4,0.6,0.8,0.1
3,0.3,0.5,0.7,0.9,0.2
4,
"""