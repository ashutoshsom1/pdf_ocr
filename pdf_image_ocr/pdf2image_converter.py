
from pathlib import Path
from typing import List
import os
from pdf2image import convert_from_path
from pdf_image_ocr.config import cfg
from pdf_image_ocr.log_init import logger
import cv2
import numpy as np

from PIL import PpmImagePlugin

def convert_image(pdf_file: Path) -> List:
    poppler_path = r"C:\Users\ashutosh.somvanshi\poppler\poppler-24.08.0\Library\bin"  # Get from environment
    try:
        images_from_path = convert_from_path(
            pdf_file, 
            output_folder=cfg.image_location,
            poppler_path=poppler_path if os.name == 'nt' else None  # Only use on Windows
        )
        return images_from_path
    except Exception as e:
        logger.error(f"PDF conversion failed: {str(e)}")
        logger.error(f"Poppler path: {poppler_path}")
        logger.error(f"PDF file: {pdf_file}")
        raise


def save_image(im: PpmImagePlugin.PpmImageFile, target_path: Path):
    rgb_im = im.convert('RGB')
    rgb_im.save(target_path)


def convert_to_cv2_image(im: PpmImagePlugin.PpmImageFile) -> np.ndarray:
    pil_image = im.convert('RGB') 
    # Convert RGB to BGR 
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    

if __name__ == "__main__":
    for pdf in cfg.doc_location.glob("*.pdf"):
        logger.info("File: %s", pdf)
        images_from_path = convert_image(pdf)
        logger.info("Images: %s", type(images_from_path))
        logger.info("Images: %s", type(images_from_path[0]))
        for i, im in enumerate(images_from_path):
            save_image(im, cfg.image_location/f"{pdf.stem}_{i}.jpg")
            logger.info(type(convert_to_cv2_image(im)))
