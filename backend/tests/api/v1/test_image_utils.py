import torch
from PIL import Image
from app.utils.image_utils import process_image

def test_process_image_output_shape():
    img = Image.new("RGB", (300, 200), color=(255, 255, 255))
    tensor = process_image(img)
    assert tensor.shape == (3, 128, 256)

def test_process_image_values_normalized():
    img = Image.new("RGB", (300, 200), color=(255, 255, 255))
    tensor = process_image(img)
    assert tensor.min().item() >= 0.0
    assert tensor.max().item() <= 1.0

def test_process_image_returns_tensor():
    img = Image.new("RGB", (300, 200), color=(0, 0, 0))
    tensor = process_image(img)
    assert isinstance(tensor, torch.Tensor)