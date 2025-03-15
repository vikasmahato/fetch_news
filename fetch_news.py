import datetime
import json
import sys

import uuid
import logging

from newsdataapi import NewsDataApiClient

from db_utils import DatabaseSession
from get_secrets import get_news_data_api_key
from models.models import NewsPost, NewsPostVideo, NewsPostImage
from s3_utils import process_image
from utils.utils import count_sentences, is_image_downloadable, process_text_to_editorjs, get_language_code

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)  # Output logs to stdout
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)


def lambda_handler(event):
    try:
        db = DatabaseSession()
        API_KEY = get_news_data_api_key()
        if not API_KEY:
            raise ValueError("API Key not found in Secrets Manager")

        category = db.get_category_by_code(event.get("nisee_category", "unknown"))
        news_data_category = event.get("category").upper()
        sub_categories = event.get("sub_categories", [])

        client = NewsDataApiClient(apikey=get_news_data_api_key())

        for sub_category in sub_categories:
            saved_count = 0
            processed_news = []
            response = client.latest_api(q=sub_category,
                                         country=["us", "in"],
                                         category=news_data_category, language=["en", "hi"],
                                         removeduplicate=True)
            articles = response.get("results", [])
            logger.info(f"News API response: {response.get('status', 'error')}")

            if not articles:
                logger.info("No new articles found.")
                return {"message": "No articles found."}

            for article in articles:
                try:
                    sentence_count = count_sentences(article.get("content"))
                    image_url = article.get('image_url')
                    video_url = article.get('video_url')

                    if image_url and not is_image_downloadable(image_url):
                        logger.info(f"Skipping article due to non-downloadable image: {article.get('title')}")
                        continue

                    if sentence_count < 10:
                        logger.info(f"Skipping article due to low sentence count: {article.get('title')}")
                        continue

                    if not (image_url or video_url):
                        logger.info(f"Skipping article due to missing media: {article.get('title')}")
                        continue


                    creator = article.get("creator")
                    if creator is not None and len(creator) > 0:
                        creator = creator[0]

                    exsiting_news = db.get_news_by_remote_id(article.get("article_id"))

                    if exsiting_news:
                        logger.info(f"Exsiting news article: {article.get('title')}")
                        continue

                    images_json = None
                    image_uuid = uuid.uuid4()
                    if image_url:
                        images_json = json.dumps(process_image(image_url, image_uuid))

                    country = db.get_country_by_name(article.get('country'))
                    source = db.get_source(
                        {
                            "code": article.get("source_id"),
                            "name": article.get("source_name"),
                            "url": article.get("source_url"),
                            "icon": article.get("source_icon"),
                        }
                    )

                    news_post = NewsPost(
                        remote_id=article.get("article_id"),
                        title=article.get("title"),
                        language=get_language_code(article.get("language")),
                        description=article.get("description"),
                        content=process_text_to_editorjs(article.get("content")),
                        published_at=article.get("publishedAt", datetime.datetime.now()),
                        creator=creator,
                        country=country,
                        world_region=country.region if country else None,
                        link=article.get("link"),
                        category_=category,
                        sub_category=sub_category.upper().replace(" ", "_"),
                        likes=0,
                        formatting="MARKDOWN",
                        type="ORGANISATION_POST",
                        source=source,
                        images=[NewsPostImage(id=image_uuid.bytes, images = image_url, original_image_url = image_url, s3_image_base_url= "https://nisee-development.s3.ap-south-1.amazonaws.com/images/")] if image_url else [],
                        videos=[NewsPostVideo(videos = video_url)] if video_url else [],
                        deleted=0,
                        images_json=images_json
                    )
                    processed_news.append(news_post)

                    if len(processed_news) >= 10:
                        db.save_all(processed_news)
                        saved_count = saved_count + len(processed_news)
                        processed_news = []

                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue

            db.save_all(processed_news)
            saved_count = saved_count + len(processed_news)
            db.save_metrics(news_data_category, sub_category, saved_count)

        return {"message": "News processing completed."}

    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":

    data  = {
        'tourism': {
            "category": "tourism",
            "nisee_category": "travel",
            "sub_categories": ["africa", "europe", "china", "india", "united states"]
        },
        'real_estate': {
            "category": "real_estate",
            "nisee_category": "real_estate",
            "sub_categories": ["real_estate"]
        },
        'business': {
            "category": "business",
            "nisee_category": "economy",
            "sub_categories": ["market", "economy", "united states", "china", "business"]
        },
        'technology': {
            "category": "technology",
            "nisee_category": "technology",
            "sub_categories": ["internet", "gadgets", "software", "mobile", "desktop", "artificial intelligence"]
        },
        'sports': {
            "category": "sports",
            "nisee_category": "sports",
            "sub_categories": ["cricket", "hockey", "tennis", "football", "badminton", "basketball", "f1 racing"]
        },
        'health': {
            "category": "health",
            "nisee_category": "health",
            "sub_categories": ["nutrition", "mental health", "fitness", "science", "health"]
        },
        'politics': {
            "category": "politics",
            "nisee_category": "politics",
            "sub_categories": ["united states", "india", "china", "russia", "europe", "asia", "africa"]
        },

        'lifestyle': {
            "category": "lifestyle",
            "nisee_category": "lifestyle",
            "sub_categories": ["entertainment", "food", "lifestyle", "environment", "tourism"]
        }
    }

    for key, value in data.items():
        lambda_handler(value)