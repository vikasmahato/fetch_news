import datetime
import json
import re
import requests
import logging
import langcodes

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_language_code(language_name: str) -> str:
    try:
        language = langcodes.find(language_name)
        return language.language.split('-')[0]  # Extract 2-letter code
    except ValueError:
        return "unknown"

def count_sentences(text):
    """
    Count the number of sentences in a given text.

    Args:
        text (str): The input text.

    Returns:
        int: The number of sentences.
    """
    if text is None:
        return 0
    # Use a regular expression to split the text into sentences
    sentences = re.split(r'[.!?]', text)

    # Remove any empty strings or whitespace-only elements
    sentences = [s.strip() for s in sentences if s.strip()]

    return len(sentences)


def is_image_downloadable(image_url):
    """
    Checks if the image at the given URL is downloadable.

    Args:
        image_url (str): The URL of the image.

    Returns:
        bool: True if the image is downloadable, False otherwise.
    """
    try:
        # Make a HEAD request to check the headers
        response = requests.head(image_url, timeout=5)

        # Check if the response status is OK (200) and Content-Type is an image
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if content_type.startswith('image/'):
                return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking URL {image_url}: {e}")

    return False

def split_into_paragraphs(text):
    # Remove extra spaces and normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Split into sentences by periods, question marks, or exclamation marks
    sentences = re.split(r'(?<=[.!?])\s', text)

    paragraphs = []
    paragraph = []

    # Group sentences into logical paragraphs (heuristically, 2-3 sentences per paragraph)
    for sentence in sentences:
        if len(paragraph) < 3:  # Limit paragraph length to 3 sentences
            paragraph.append(sentence)
        else:
            paragraphs.append(" ".join(paragraph))
            paragraph = [sentence]

    # Append the last paragraph if it exists
    if paragraph:
        paragraphs.append(" ".join(paragraph))

    return paragraphs

def process_text_to_editorjs(text):
    paragraphs = split_into_paragraphs(text)

    blocks = [
        {
            "type": "paragraph",
            "data": {
                "text": paragraph
            }
        }
        for paragraph in paragraphs
    ]
    editorjs_json = {
        "time": int(datetime.datetime.now().timestamp() * 1000),
        "blocks": blocks,
        "version": "2.26.5"
    }

    return json.dumps(editorjs_json)
