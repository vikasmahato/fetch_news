from typing import Type, List, Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, load_only

from get_secrets import get_db_url
from models.models import NewsPost, Country, Source, Category
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Set up SQLAlchemy connection
engine = create_engine(get_db_url(), echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class DatabaseSession:
    def __init__(self):
        """Initialize the session when an instance is created."""
        self.session = SessionLocal()
        self.country_cache: Dict[str, Type[Country]] = {}  # In-memory cache
        self.category_cache: Dict[str, Type[Category]] = {}  # In-memory cache
        self.source_cache: Dict[str, Type[Source]] = {}  # In-memory cache

    def get_news_by_remote_id(self, remote_id: str) -> Type[NewsPost] | None:
        """Fetch a news post by its remote ID."""
        return self.session.query(NewsPost).filter(NewsPost.remote_id == remote_id).first()

    def get_source(self, source_data: dict) -> Source:
        """Fetch or create a source by its code, with caching."""
        code = source_data.get("code")
        if not code:
            return None  # If code is missing, return None

        # Check cache
        if code in self.source_cache:
            logger.info(f"Cache hit for source: {code}")
            return self.source_cache[code]

        # Query the database
        logger.info(f"Cache miss for source: {code}, querying database...")
        source = self.session.query(Source).filter_by(code=code).first()

        # If source does not exist, create a new one
        if not source:
            logger.info(f"Creating new source: {code}")
            source = Source(
                code=code,
                name=source_data.get("name"),
                url=source_data.get("url"),
                icon=source_data.get("icon"),
                deleted=0
            )
            self.session.add(source)
            self.session.commit()
            logger.info(f"New source created: {code}")

        # Store in cache
        self.source_cache[code] = source
        return source

    def get_country_by_name(self, name: str | list[str]) -> Type[Country] | None:
        """Fetch a country by its name with caching. Supports single string or list of strings."""

        # If name is a list, take the first element
        if isinstance(name, list):
            if not name:  # Handle empty list case
                return None
            name = name[0]  # Use the first element

        if name in self.country_cache:
            logger.info(f"Cache hit for country: {name}")
            return self.country_cache[name]

        logger.info(f"Cache miss for country: {name}, querying database...")
        country = self.session.query(Country).filter_by(name_en = name).first()

        if country:
            self.country_cache[name] = country  # Store in cache

        return country

    def get_category_by_code(self, code: str) -> Type[Category] | None:
        """Fetch a category by its name with caching."""
        if code in self.category_cache:
            logger.info(f"Cache hit for source: {code}")
            return self.category_cache[code]

        logger.info(f"Cache miss for source: {code}, querying database...")
        category = (self.session.query(Category)
                    .options(load_only(Category.id, Category.code, Category.description, Category.position, Category.redirect_url))
                    .filter_by(code = code.upper()).first())

        if category:
            self.category_cache[code] = category  # Store in cache

        return category


    def save(self, news_post: NewsPost):
        """Save a news post."""
        self.session.add(news_post)
        self.session.commit()
        logger.info(f"News Post Created: ID {news_post.id}")

    def save_all(self, news_posts: List[NewsPost]):
        """Save multiple news posts in a single transaction."""
        try:
            self.session.add_all(news_posts)
            self.session.commit()
            logger.info(f"Saved {len(news_posts)} news posts successfully.")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to save news posts: {e}")
            raise

    def __del__(self):
        """Ensure the session is closed when the object is destroyed."""
        if self.session:
            self.session.close()
            print("Database session closed.")


# Main execution
if __name__ == "__main__":
    db = DatabaseSession()
    news_post = db.get_news_by_remote_id("1")

    if news_post:
        print(news_post.remote_id)
    else:
        print("News post not found.")
