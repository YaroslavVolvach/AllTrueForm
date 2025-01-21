from fastapi import FastAPI 
from app.api.v1.support_request import router as support_request_router
from app.api.v1.tag import router as tag_router
from app.api.v1.user import router as user_router

app = FastAPI()

app.include_router(support_request_router, prefix="/v1/support-request", tags=["support-request"])
app.include_router(tag_router, prefix="/v1/tags", tags=["tags"])
app.include_router(user_router, prefix="/v1/users", tags=["users"])