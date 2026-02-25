from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import predict
import logging
from contextlib import asynccontextmanager
from app.services.model_service import ModelService
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger=logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Loading model...")
    ModelService.load(settings.MODEL_PATH)
    logger.info("Model loaded successfully.")
    yield
    logger.info("Shutting down.")

# everything before yield runs on startup, everything after runs on shutdown. 

app=FastAPI(title=settings.APP_NAME,debug=settings.DEBUG,lifespan=lifespan)
# title shows up in automated fastapi docs
#  if DEBUG=true in your .env, FastAPI runs in debug mode with more detailed error messages

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_methods=['POST','GET'],
    allow_headers=["*"]
)

app.include_router(predict.router,prefix=f"{settings.API_V1_STR}/predict",tags=["predict"])
# predict.router is a collection of routes defined in a separate file, and include_router plugs them into the main app. The prefix automatically adds /api/v1/predict in front of all those routes, so you don't have to repeat it in every route definition. tags just groups them together in the auto-generated docs for better organization.


@app.get('/health')
def health():
    return {'status':'ok'}