from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from database import engine
from models import schema
import uvicorn

schema.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Resume Screener API", version="1.0.0", description="API for parsing and scoring resumes against JDs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
