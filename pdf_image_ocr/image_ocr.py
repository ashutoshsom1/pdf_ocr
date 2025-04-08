from pathlib import Path
from typing import List
import easyocr
from pdf_image_ocr.pdf2image_converter import convert_image, convert_to_cv2_image
from pdf_image_ocr.log_init import logger

# Initialize EasyOCR reader (do this once)
reader = easyocr.Reader(['en'])  # Initialize for English

def convert_img_to_text(pdf_file: Path) -> str:
    try:
        image_list = convert_image(pdf_file)
        str_result = ""
        
        for image in image_list:
            # Convert PIL image to cv2 format
            cv2_image = convert_to_cv2_image(image)
            
            # Perform OCR
            results = reader.readtext(cv2_image)
            
            # Extract text from results
            page_text = " ".join([text[1] for text in results])
            str_result += page_text + "\n\n"
        
        return str_result
    except Exception as e:
        logger.error(f"Error in OCR processing: {str(e)}")
        raise

if __name__ == "__main__":
    from pdf_image_ocr.config import cfg
    
    for doc in cfg.doc_location.glob("*"):
        logger.info(doc)
        converted_text = convert_img_to_text(doc)
        logger.info(converted_text)
        logger.info("")
        break
