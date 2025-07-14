import numpy as np

# Step 1: Define your vocabulary
vocab = ["machine", "learning", "is", "fun", "and", "powerful"]

# Step 2: Assign a vector to each word manually or randomly
embedding_dim = 5  # Each word will be represented by a 5-dimensional vector

# Random embedding
word_embeddings = {}

for word in vocab:
    word_embeddings[word] = np.random.rand(embedding_dim)

# Step 3: Print the vectors
for word, vector in word_embeddings.items():
    print(f"Word: {word.ljust(10)} → Vector: {vector}")
