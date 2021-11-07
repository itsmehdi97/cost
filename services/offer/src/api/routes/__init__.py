from fastapi import APIRouter

from api.routes.offers import router as offers_router



router = APIRouter()



router.include_router(offers_router, prefix='', tags=['offers'])