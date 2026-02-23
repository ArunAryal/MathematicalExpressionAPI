from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import predict

app=FastAPI(title=settings.APP_NAME,debug=settings.DEBUG)
# title shows up in automated fastapi docs
#  if DEBUG=true in your .env, FastAPI runs in debug mode with more detailed error messages

app.include_router(predict.router,prefix=f"{settings.API_V1_STR}/predict",tags=["predict"])
# predict.router is a collection of routes defined in a separate file, and include_router plugs them into the main app. The prefix automatically adds /api/v1/predict in front of all those routes, so you don't have to repeat it in every route definition. tags just groups them together in the auto-generated docs for better organization.


@app.get('/health')
def health():
    return {'status':'ok'}