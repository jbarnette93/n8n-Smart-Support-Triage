import os, json, requests
from tqdm import tqdm

# ---- CONFIG ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_URL = "https://kb-support-gczm0qb.svc.aped-4627-b74a.pinecone.io/vectors/upsert" 
DOCS_DIR = "support_docs"

MODEL = "text-embedding-3-small"

# ---- CHECK CONFIG ----
if not OPENAI_API_KEY or not PINECONE_API_KEY:
    raise SystemExit("❌ Missing OPENAI_API_KEY or PINECONE_API_KEY environment variable.")

# ---- HEADERS ----
openai_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

pinecone_headers = {
    "Content-Type": "application/json",
    "Api-Key": PINECONE_API_KEY
}

# ---- MAIN LOOP ----
for fname in tqdm(os.listdir(DOCS_DIR), desc="Uploading docs"):
    if not fname.endswith((".txt", ".md")):
        continue
    path = os.path.join(DOCS_DIR, fname)
    text = open(path).read().strip()
    if not text:
        continue

    # 1️⃣ Get embedding
    embed_payload = {"model": MODEL, "input": text}
    r = requests.post("https://api.openai.com/v1/embeddings", headers=openai_headers, json=embed_payload)
    if r.status_code != 200:
        print(f"❌ Embedding failed for {fname}: {r.text}")
        continue
    embedding = r.json()["data"][0]["embedding"]

    # 2️⃣ Upload to Pinecone
    upsert_payload = {
        "vectors": [{
            "id": fname,
            "values": embedding,
            "metadata": {"filename": fname, "length": len(text)}
        }]
    }
    r2 = requests.post(PINECONE_INDEX_URL, headers=pinecone_headers, json=upsert_payload)
    if r2.status_code != 200:
        print(f"❌ Pinecone upload failed for {fname}: {r2.text}")
    else:
        print(f"✅ Uploaded {fname}")

print("🎉 Done! All files processed.")