import schedule
import time

from fetch_news import lambda_handler

regions = ['AFRICA', 'ASIA', 'EUROPE', 'MIDDLE_EAST', 'NORTH_AMERICA', 'OCEANIA', 'SOUTH_AMERICA']

def fetch_news():
    data = {
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

    for world_region in regions:
        for value in data.values():
            lambda_handler(world_region, value)


# Schedule API calls based on cron times
schedule.every().hour.at(":10").do(fetch_news)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
