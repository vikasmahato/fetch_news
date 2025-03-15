import schedule
import time

from fetch_news import lambda_handler


def fetch_news(category, nisee_category, sub_categories):
    payload = {
        "category": category,
        "nisee_category": nisee_category,
        "sub_categories": sub_categories
    }
    lambda_handler(payload)

# Schedule API calls based on cron times
schedule.every().hour.at(":10").do(fetch_news, "business", "economy", ["market", "economy", "united states", "china", "business"])
schedule.every().hour.at(":15").do(fetch_news, "technology", "technology", ["internet", "gadgets", "software", "mobile", "desktop", "artificial intelligence"])
schedule.every().hour.at(":20").do(fetch_news, "sports", "sports", ["cricket", "hockey", "tennis", "football", "badminton", "basketball", "f1 racing"])
schedule.every().hour.at(":25").do(fetch_news, "health", "health", ["nutrition", "mental health", "fitness", "science", "health"])
schedule.every().hour.at(":30").do(fetch_news, "politics", "politics", ["united states", "india", "china", "russia", "europe", "asia", "africa"])
schedule.every().hour.at(":35").do(fetch_news, "tourism", "travel", ["africa", "europe", "china", "india", "united states"])
schedule.every().hour.at(":40").do(fetch_news, "real_estate", "real_estate", ["real_estate"])
schedule.every().hour.at(":45").do(fetch_news, "lifestyle", "lifestyle", ["entertainment", "food", "lifestyle", "environment", "tourism"])

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(30)
