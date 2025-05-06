"""
MySQL → Chroma 업로드 스크립트
docker compose exec ai python -m app.ingest
"""
from __future__ import annotations
import os
from itertools import chain
import pymysql, chromadb, tqdm                    # ← CHANGED
from langchain_openai import OpenAIEmbeddings

# ───── env ────────────────────────────────────────────────────────────────
DSN = dict(
    host        = os.getenv("MYSQL_HOST", "host.docker.internal"),
    port        = int(os.getenv("MYSQL_PORT", 3307)),     
    user        = os.getenv("MYSQL_USER", "root"),
    password    = os.getenv("MYSQL_PASS", ""),
    db          = os.getenv("MYSQL_DB", "mylio"),
    charset     = "utf8mb4",
    cursorclass = pymysql.cursors.DictCursor,
)

CHROMA_HOST       = os.getenv("CHROMA_HOST", "http://chroma:8000")  # ← CHANGED (8000 고정)
COLLECTION_NAME   = os.getenv("COLLECTION_NAME", "menu_embeddings")

emb   = OpenAIEmbeddings(model="text-embedding-3-small")
client = chromadb.HttpClient(host=CHROMA_HOST)
coll   = client.get_or_create_collection(COLLECTION_NAME)          # ← NEW helper

# ───── 1. 메뉴 READ ────────────────────────────────────────────────────────
def fetch_menus() -> list[dict]:
    sql = """
        SELECT  m.id, m.name_kr, m.name_en, m.description,
                GROUP_CONCAT(t.tag_kr SEPARATOR ' ') AS tags,
                m.store_id
          FROM  menu m
          LEFT JOIN menu_tag_map t ON t.menu_id = m.id
         WHERE  m.status = 'SELLING'
      GROUP BY  m.id
    """
    with pymysql.connect(**DSN) as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()

# ───── 2. 업서트 ───────────────────────────────────────────────────────────
def upload():
    rows = fetch_menus()
    if not rows:
        print("⚠️  메뉴가 없습니다.")
        return

    ids, vecs, docs, metas = [], [], [], []
    for r in tqdm.tqdm(rows, desc="Embedding"):
        corpus = " ".join(filter(None, (
            r["name_kr"], r["name_en"], r["description"], r["tags"]
        )))
        ids.append(str(r["id"]))
        vecs.append(emb.embed_query(corpus))
        docs.append(r["name_kr"])
        metas.append({
            "menu_id":  r["id"],
            "name":     r["name_kr"],
            "store_id": r["store_id"],
        })

    # 방법 1: 컬렉션을 삭제하고 새로 생성
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"✅ 컬렉션 '{COLLECTION_NAME}' 삭제 완료")
    except Exception as e:
        print(f"⚠️ 컬렉션 삭제 실패: {e}")
    
    # 새 컬렉션 생성
    coll = client.create_collection(COLLECTION_NAME)
    print(f"✅ 새 컬렉션 '{COLLECTION_NAME}' 생성 완료")

    # 새 데이터 일괄 추가
    coll.add(ids=ids, embeddings=vecs, documents=docs, metadatas=metas)
    print(f"✅ {len(ids)} 건 업로드 완료")

if __name__ == "__main__":
    upload()