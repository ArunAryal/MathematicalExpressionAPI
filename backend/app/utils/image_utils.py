# loading image
import numpy as np 
from PIL import Image
import io
from fastapi import HTTPException
import logging
import torch

#io — standard Python library, io.BytesIO lets you treat raw bytes as a file object

logger=logging.getLogger(__name__)

IMG_H = 128
IMG_W = 256

def load_image(image_bytes:bytes)-> Image.Image:
    try:
        return Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        logger.warning("Failed to open images: %s",e)
        raise HTTPException(status_code=400,detail="Invalid image file")

# io.BytesIO(image_bytes) — wraps the raw bytes into a file-like object because Image.open expects a file, not raw bytes
# Image.open(...) — opens it as an image
# .convert("L") — converts to grayscale. "L" stands for luminance, meaning only brightness values, no color.

def process_image(pil_img: Image.Image) -> torch.Tensor:
    img = pil_img.convert("L")
    img.thumbnail((IMG_W, IMG_H), Image.BILINEAR)
    
    padded = Image.new("L", (IMG_W, IMG_H), color=255)
    offset_x = (IMG_W - img.width) // 2
    offset_y = (IMG_H - img.height) // 2
    padded.paste(img, (offset_x, offset_y))
    
    arr = np.array(padded, dtype=np.float32) / 255.0
    arr = np.stack([arr, arr, arr], axis=0)
    return torch.tensor(arr, dtype=torch.float32)