import boto3
from io import BytesIO
from PIL import Image, ImageFilter
import requests

S3_BUCKET = "nisee-development"
S3_REGION = "ap-south-1"

s3_client = boto3.client("s3")

# Image sizes
IMAGE_SIZES = {
    "lg": (1024, 1024),
    "md": (512, 512),
    "sm": (256, 256),
    "blur": (128, 128)  # Very small blurred
}


def save_to_s3(image, file_name):
    s3_key = f"images/{file_name}"

    buffer = BytesIO()
    image.save(buffer, "WEBP", quality=85)
    buffer.seek(0)

    s3_client.upload_fileobj(buffer, S3_BUCKET, s3_key, ExtraArgs={"ContentType": "image/webp"})
    # logger.info(f"Uploaded: {s3_key}")
    return s3_key


def process_image(image_url, image_uuid):
    # Download the image
    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception("Failed to download image")

    # Open the image and convert to RGB
    image = Image.open(BytesIO(response.content)).convert("RGB")

    # Save the original image in WebP format inside "images/" folder
    original_filename = f"{image_uuid}.webp"
    save_to_s3(image, original_filename)

    image_base_path = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/"

    processed_images = {}
    for size_name, dimensions in IMAGE_SIZES.items():
        img_resized = image.copy()
        img_resized.thumbnail(dimensions)
        if size_name == "blur":
            img_resized = img_resized.filter(ImageFilter.GaussianBlur(5))
        resized_filename = f"{image_uuid}-{size_name}.webp"
        s3_key = save_to_s3(img_resized, resized_filename)
        processed_images[size_name] = f"{image_base_path}/{s3_key}"

    return processed_images