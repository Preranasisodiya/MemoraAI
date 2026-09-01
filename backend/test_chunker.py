from app.services.document_extractor import extract_text
from app.services.text_chunker import chunk_text


file_path = "uploads/4/cebf4afd24fae94887f9c6843091b6ad7d877556ae488b3f1a2d24704c87ff40.pdf"

# Extract text from the PDF
text = extract_text(
    file_path,
    "pdf"
)

# Create chunks
chunks = chunk_text(
    text,
    chunk_size=1000,
    overlap=200
)

print("====================================")
print("TOTAL CHARACTERS:", len(text))
print("TOTAL CHUNKS:", len(chunks))
print("====================================")

for index, chunk in enumerate(chunks, start=1):

    print(f"\n========== CHUNK {index} ==========")
    print(chunk)