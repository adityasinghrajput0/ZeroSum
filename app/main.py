from fastapi import FastAPI
from app.api import auth

app=FastAPI(title="ZeroSum")
app.include_router(auth.router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status":"ok"}