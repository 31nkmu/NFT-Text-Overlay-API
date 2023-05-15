from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .auth.router import auth_router
from .certificates.router import certificates_router
from .web3_transactions.router import router as transactions_router


app = FastAPI(title="Elemint")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(certificates_router)
app.include_router(transactions_router)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", log_level="info")
