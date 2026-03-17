import pytest
from fastapi.testclient import TestClient 
import io
from PIL import Image
from app.main import app


# initialize TestClient to make HTTP request to app without actually starting a server.
client=TestClient(app)

def make_png_bytes()->bytes:

    #create real PNG image programatically for testing. A 64*64 grayscale('L') iamge filled with white
    image=Image.new('L',(64,64),color=255)

    #crete an in memory buffer like an empty file living in RAM
    buffer=io.BytesIO()

    #save created image into that buffer in PNG format.
    image.save(buffer,format="PNG")

    # return the buffer's contents as raw bytes.
    return buffer.getvalue()

#ensure the server is up
def test_health():
    response=client.get('/health')
    assert response.status_code==200
    assert response.json()=={'status':'ok'}

# test case: when model returns an expression, Sympy doesnot solve it
def test_predict_expression(mocker):

    #replace the real ModelService.predict method with a fake one that always returns x^2+2x+1
    mocker.patch("app.api.v1.endpoints.predict.ModelService.predict",return_value="x^2 + 2x + 1")

    #send a post request uploading a valid png
    response=client.post(
        'api/v1/predict/',
        # simulate a multipart file upload. test.png is filename, make_png_bytes() is the content and image/png is content type
        files={"file": ("test.png",make_png_bytes(),'image/png')}
        )
    assert response.status_code==200
    data=response.json()
    assert data["latex"]=="x^2 + 2x + 1"
    assert not data['is_equation']
    assert data['result'] is None

#test case: when model returns the equation, sumpy solves it
def test_predict_equation(mocker):
    #fake model to return x+2=5
    mocker.patch("app.api.v1.endpoints.predict.ModelService.predict", return_value="x + 2 = 5")

    response=client.post(
        'api/v1/predict/',
        files={"file":("test.png",make_png_bytes(),"image/png")}
    )

    assert response.status_code==200
    data=response.json()
    assert data["is_equation"]
    assert data['result'] is not None

# test case: bytes aren't a real image, load_image raises 400
def test_predict_invalid_file():

    #upload a random bytes claiming to be a png
    response=client.post(
        'api/v1/predict',
        files={'file':('test.txt',b'Hello World!','image/png')}
    )
    assert response.status_code==400

# test case:  non-PNG rejected at content type check
def test_predict_wrong_content_type():
    response=client.post(
        'api/v1/predict/',
        files={"file": ("test.pdf",make_png_bytes(),'application/pdf')}
    )
    assert response.status_code==400

def test_predict_jpeg_accepted(mocker):
    mocker.patch("app.api.v1.endpoints.predict.ModelService.predict", return_value="x^2 + 1")
    response = client.post(
        "api/v1/predict/",
        files={"file": ("test.jpg", make_png_bytes(), "image/jpeg")}
    )
    assert response.status_code == 200