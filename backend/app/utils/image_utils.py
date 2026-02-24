# loading image
import numpy as np 
from PIL import Image
import io
from fastapi import HTTPException

def load_image(image_bytes:bytes)-> np.ndarray:
    try:
        image=Image.open(io.BytesIO(image_bytes)).convert("L")
    except Exception:
        raise HTTPException(status_code=400,details="Invalid image files")
    return np.array(image)