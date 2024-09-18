
from fastapi import FastAPI

from .routers import casetext


app = FastAPI()
app.include_router(casetext.router)


@app.get("/")
async def root():
    return {"message": "Hello Challenge!"}
