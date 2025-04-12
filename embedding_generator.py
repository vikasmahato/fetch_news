from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams
from get_secrets import get_vector_db_api_key


class NewsPostVectorDB:
    def __init__(self, collection_name="news_posts"):
        self.API_KEY = get_vector_db_api_key()
        self.qdrant = QdrantClient(
            url="https://00ea6bb4-0b7d-41fd-b6f5-d933674cecde.europe-west3-0.gcp.cloud.qdrant.io:6333",
            api_key=self.API_KEY
        )
        self.collection_name = collection_name

        # Ensure the collection exists
        if self.collection_name not in [c.name for c in self.qdrant.get_collections().collections]:
            self.qdrant.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

        # Load embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim vector

    def save_embeddings(self, news_posts):
        """
        Takes a list of news posts (or a single post) and saves its embedding to the vector DB.
        """
        if isinstance(news_posts, list):
            batch_size = 1000
            start = 0
            while start < len(news_posts):
                end = min(start + batch_size, len(news_posts))
                batch = news_posts[start:end]
                self._upsert_embeddings(batch)
                start += batch_size
        else:
            self._upsert_embeddings([news_posts])

    def _upsert_embeddings(self, news_posts):
        points = []
        for post in news_posts:
            text = post.title or ""
            vector = self.model.encode(text)

            payload = {
                "id": post.id,
                "title": post.title,
                "published_at": post.published_at.isoformat() if post.published_at else None,
            }

            point_id = int(post.id)
            points.append(PointStruct(id=point_id, vector=vector.tolist(), payload=payload))

        self.qdrant.upsert(collection_name=self.collection_name, points=points)
        print(f"Uploaded {len(points)} news posts to Qdrant")

    def search_news(self, query: str, limit: int = 5):
        """
        Searches for similar news posts in the vector DB based on a search term.
        """
        query_vector = self.model.encode(query).tolist()
        search_result = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return [hit.payload for hit in search_result]
