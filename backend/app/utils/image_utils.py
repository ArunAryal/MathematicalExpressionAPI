# loading image
import numpy as np 
from PIL import Image
import io
from fastapi import HTTPException
import logging

#io — standard Python library, io.BytesIO lets you treat raw bytes as a file object

logger=logging.getLogger(__name__)

def load_image(image_bytes:bytes)-> np.ndarray:
    try:
        image=Image.open(io.BytesIO(image_bytes)).convert("L")
    except Exception as e:
        logger.warning("Failed to open images: %s",e)
        raise HTTPException(status_code=400,detail="Invalid image file")
    return np.array(image)

# io.BytesIO(image_bytes) — wraps the raw bytes into a file-like object because Image.open expects a file, not raw bytes
# Image.open(...) — opens it as an image
# .convert("L") — converts to grayscale. "L" stands for luminance, meaning only brightness values, no color.