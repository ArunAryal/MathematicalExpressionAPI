# loads model, runs inference

import numpy as np
from tensorflow import keras

class ModelService:
    _model=None #private

    @classmethod
    def load(cls,model_path:str):
        cls._model=keras.models.load_model(model_path)

    @classmethod
    def predict(cls,array:np.ndarray) -> str:
        if cls._model is None:
            raise RuntimeError("Model is not loaded")
        output=cls._model.predict(array)
        return output