from fastapi import FastAPI
from fastsecforge.config import settings
from fastsecforge.database import Base, get_db
from fastsecforge.routers.auth import router as auth_router
from fastsecforge.routers.users import router as users_router
app = FastAPI(title=settings.PROJECT_NAME)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Initialize database tables for SQL
    if settings.DATABASE_TYPE == "sql":
        Base.metadata.create_all(bind=get_db().__next__().bind)

@app.get("/")
def root():
    return {"message": "FastSecForge API", "status": "active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)