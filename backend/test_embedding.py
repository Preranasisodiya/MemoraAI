from app.services.embedding_service import generate_embedding

text = """
Machine learning is a subset of artificial intelligence
that allows systems to learn from data.
"""

embedding = generate_embedding(text)

print("Embedding generated successfully")
print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])