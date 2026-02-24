# loading image
import numpy as np 
from PIL import Image
import io
from fastapi import HTTPException

#io — standard Python library, io.BytesIO lets you treat raw bytes as a file object

def load_image(image_bytes:bytes)-> np.ndarray:
    try:
        image=Image.open(io.BytesIO(image_bytes)).convert("L")
    except Exception:
        raise HTTPException(status_code=400,details="Invalid image files")
    return np.array(image)

# io.BytesIO(image_bytes) — wraps the raw bytes into a file-like object because Image.open expects a file, not raw bytes
# Image.open(...) — opens it as an image
# .convert("L") — converts to grayscale. "L" stands for luminance, meaning only brightness values, no color.