from sentence_transformers import SentenceTransformer
import faiss, pickle, sys, json

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("kb_index.faiss")
names = pickle.load(open("kb_meta.pkl", "rb"))

query = sys.argv[1]  # incoming text
q_emb = model.encode([query], convert_to_numpy=True)
scores, idxs = index.search(q_emb, k=3)

results = [{"doc": names[i], "score": float(scores[0][n])} for n, i in enumerate(idxs[0])]
print(json.dumps(results))