import pytest
import torch
from unittest.mock import MagicMock, patch
from app.services.model_service import ModelService

def test_model_load_bad_path():
    with pytest.raises(Exception):
        ModelService.load("nonexistent/path/model.pt")

def test_predict_returns_string(mocker):
    mock_model = MagicMock()
    
    # mock encode to return a dummy tensor
    mock_model.encode.return_value = torch.zeros(1, 128, 256)
    
    # mock decode to immediately return EOS token
    from app.core.vocab import EOS_ID
    logits = torch.zeros(1, 1, 256)
    logits[0, 0, EOS_ID] = 100.0  # force argmax to pick EOS
    mock_model.decode.return_value = logits

    ModelService._model = mock_model

    from PIL import Image
    img = Image.new("RGB", (300, 200), color=(255, 255, 255))
    result = ModelService.predict(img)
    
    assert isinstance(result, str)

def test_predict_raises_if_model_not_loaded():
    ModelService._model = None
    from PIL import Image
    img = Image.new("RGB", (300, 200))
    with pytest.raises(RuntimeError, match="Model is not loaded."):
        ModelService.predict(img)