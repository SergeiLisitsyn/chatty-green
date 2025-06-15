from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
from load_posts import load_posts
import psycopg2
import os

app = FastAPI()


# Загружаем модель
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def get_posts_from_db():
    conn = psycopg2.connect(
        dbname=os.getenv("PG_NAME", 'postgres'),
        user=os.getenv("PG_USER", 'postgres'),
        password=os.getenv("PG_PASSWORD", 'password'),
        host=os.getenv("PG_HOST", 'db'),
        port=os.getenv("PG_PORT", 5432)
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM posts_post WHERE text IS NOT NULL LIMIT 10000")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {row[0]: row[1] for row in result}


POSTS = get_posts_from_db()
post_ids = list(POSTS.keys())
post_texts = list(POSTS.values())


embeddings = model.encode(
    post_texts,
    convert_to_numpy=True,
    normalize_embeddings=True
).astype("float32")


index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)


@app.on_event("startup")
def startup_event():
    print(f"Loaded {len(POSTS)} posts into FAISS index.")


# Запрос
class RecommendRequest(BaseModel):
    text: str
    top_k: int = 3


@app.post("/recommend")
def recommend_posts(request: RecommendRequest):
    query_vector = model.encode(request.text, convert_to_numpy=True, normalize_embeddings=True).astype("float32").reshape(1, -1)

    distances, indices = index.search(query_vector, k=min(request.top_k, len(post_ids)))

    results = []
    for idx, score in zip(indices[0], distances[0]):
        post_id = post_ids[idx]
        results.append({"post_id": post_id, "score": round(float(score), 3)})

    return {"recommended": results}


@app.post("/reindex")
def reindex():
    global index, post_ids
    posts = load_posts()
    post_ids = list(posts.keys())
    texts = list(posts.values())

    embeddings = model.encode(texts, convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return {"message": f"Reindexed {len(posts)} posts."}

@app.get("/health")
def health_check():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_NAME"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "5432"),
        )
        conn.close()
        return {"status": "ok", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}