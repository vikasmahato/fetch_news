import json

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams

from db_utils import DatabaseSession
from get_secrets import get_vector_db_api_key

db = DatabaseSession()


API_KEY = get_vector_db_api_key()

qdrant = QdrantClient(
    url="https://00ea6bb4-0b7d-41fd-b6f5-d933674cecde.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key=API_KEY
)


COLLECTION_NAME = "news_posts"

# Create the collection if it doesn't exist
if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim vector

BATCH_SIZE = 1000
start = 0


while True:
    print(f"Fetching rows starting at index: {start}")
    rows = db.findAll(start=start, limit=BATCH_SIZE)

    if not rows:
        print("No more rows to process.")
        break

    points = []
    for row in rows:
        text = row.title or ""
        vector = model.encode(text)

        content_json = row.content or ""
        paragraph_texts = []

        try:
            content_data = json.loads(content_json)
            if isinstance(content_data, dict) and "blocks" in content_data:
                for block in content_data["blocks"]:
                    if block.get("type") == "paragraph":
                        paragraph_texts.append(block["data"].get("text", ""))
        except Exception as e:
            print(f"Failed to parse content JSON for row {row.id}: {e}")

        content_text = " ".join(paragraph_texts)
        if len(content_text) > 300:
            content_text = content_text[:300].rstrip() + "..."

        try:
            images = json.loads(row.images_json or '{}')
            image_url = images.get("sm")
        except (json.JSONDecodeError, TypeError):
            image_url = None

        # Fallback to row.images[0].original_image_url if "sm" not available
        if not image_url:
            try:
                image_url = row.images[0].original_image_url
            except (IndexError, AttributeError, TypeError):
                image_url = ""

        payload = {
            "id": row.id,
            "title": row.title,
            "content": content_text,
            "image_url": image_url,
            "video_url": "",
            "language": row.language,
            "published_at": row.published_at.isoformat() if row.published_at else None,
        }

        point_id = int(row.id)
        points.append(PointStruct(id=point_id, vector=vector.tolist(), payload=payload))

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Uploaded {len(points)} news posts to Qdrant from index {start}")

    # Move to next batch
    start += BATCH_SIZE

# --- Semantic Search ---
# def search_news(query: str, limit: int = 5):
#     query_vector = model.encode(query).tolist()
#     search_result = qdrant.search(
#         collection_name=COLLECTION_NAME,
#         query_vector=query_vector,
#         limit=limit
#     )
#     return [hit.payload for hit in search_result]
#
# # Example Search
# results = search_news("latest tech innovations")
# for r in results:
#     print(f"- {r['title']}")
