import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def average_embedding(embedding_array, start, end):
    if start < 0 or end > len(embedding_array) or start >= end:
        raise ValueError("Invalid start or end for slicing.")
    return embedding_array[start:end].mean(axis=0)

#---

def similarity_matrix(emb1, emb2, window_size):
    L1, D1 = emb1.shape
    L2, D2 = emb2.shape
    if D1 != D2:
        raise ValueError("Embedding dimensions must match.")
    if window_size > min(L1, L2):
        raise ValueError("Window size too large for given sequences.")

    W1 = L1 - window_size + 1
    W2 = L2 - window_size + 1

    sim_matrix = np.zeros((W1, W2))

    # Precompute all windowed averages
    windows1 = [average_embedding(emb1, i, i + window_size) for i in range(W1)]
    windows2 = [average_embedding(emb2, j, j + window_size) for j in range(W2)]

    sim_matrix = cosine_similarity(np.vstack(windows1), np.vstack(windows2))

    return sim_matrix