from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.confirmation import router as confirmation_router
from app.api.v1.tag import router as tag_router
from app.api.v1.user import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(confirmation_router, prefix="/v1/confirmation", tags=["confirmation"])
app.include_router(tag_router, prefix="/v1/tags", tags=["tags"])
app.include_router(user_router, prefix="/v1/users", tags=["users"])