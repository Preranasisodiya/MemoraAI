from app.services.document_extractor import extract_text


file_path = "uploads/4/cebf4afd24fae94887f9c6843091b6ad7d877556ae488b3f1a2d24704c87ff40.pdf"

text = extract_text(
    file_path,
    "pdf"
)

print("========== EXTRACTED TEXT ==========")
print(text)
print("====================================")