from fastapi import FastAPI
from app.api import auth, accounts

app=FastAPI(title="ZeroSum")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status":"ok"}