# pydantic models for request/response

from pydantic import BaseModel

class PredictResponse(BaseModel):
    latex:str
    is_equation:bool
    result:str | None = None
    # result is none when its just an expression,populated when sympy solves as equation