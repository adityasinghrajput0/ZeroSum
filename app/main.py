from fastapi import FastAPI
from app.api import auth, accounts, topup, transfers

app=FastAPI(title="ZeroSum")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")
app.include_router(topup.router, prefix="/api/v1")
app.include_router(transfers.router,prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status":"ok"}