from fastapi import APIRouter,UploadFile,File,HTTPException
from app.schemas.predict import PredictResponse
from app.services.model_service import ModelService
from app.services.math_service import MathService
from app.utils.image_utils import load_image

# APIRouter — the mini app to define routes
# File — used to mark a parameter as a file input

# UploadFile —special FastAPI class that wraps an uploaded file and gives you useful information and methods to work with it. When a file is uploaded, it doesn't just give you raw bytes — it gives you an object with multiple things attached:
# file.filename — the original name of the file, like "math.png"
# file.content_type — what kind of file it is
# file.read() — method to actually read the bytes
# file.size — size of the file

# file.content_type is the MIME type of the uploaded file. MIME type is just a standard way of describing what kind of data a file contains. For example:

# image/png — PNG image
# image/jpeg — JPEG image
# application/pdf — PDF file
# text/plain — plain text file


router=APIRouter()
# Creates the router object that main.py plugs in via include_router.



# Registers a POST endpoint at /. Since main.py added the prefix /api/v1/predict, the full URL becomes /api/v1/predict/. response_model=PredictResponse tells FastAPI to always shape the response according to that pydantic model.
@router.post('/',response_model=PredictResponse)
async def predict(file:UploadFile=File(...)):
    if file.content_type not in ('image/png','image/jpeg'):
        raise HTTPException(status_code=400,detail="only PNG images are accepted.")
    
    image_bytes=await file.read()
    image_array=load_image(image_bytes)

    latex=ModelService.predict(image_array)
    is_equation,result= MathService.process(latex)

    return PredictResponse(latex=latex, is_equation=is_equation, result=result)


#The function is async because reading files is an I/O operation — async lets the server handle other requests while waiting