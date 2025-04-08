import os
from pathlib import Path
from dotenv import load_dotenv
from pdf_image_ocr.log_init import logger

# Load environment variables
load_dotenv()

class Config():
    # Set default values if environment variables are not found
    doc_location = Path(os.getenv("DOC_LOCATION", "/tmp"))
    image_location = Path(os.getenv("TEMP_IMG_PATH", "/tmp/pdf_to_image_server"))
    
    # Create directories if they don't exist
    if not image_location.exists():
        image_location.mkdir(parents=True, exist_ok=True)
    if not doc_location.exists():
        doc_location.mkdir(parents=True, exist_ok=True)

cfg = Config()
