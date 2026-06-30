from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.bank_transactions import router as bank_transactions_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.imports import router as imports_router
from app.api.v1.endpoints.ledger_transactions import router as ledger_transactions_router
from app.api.v1.endpoints.reconciliations import router as reconciliations_router
from app.api.v1.endpoints.uploads import router as uploads_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(bank_transactions_router, prefix="/bank-transactions", tags=["Bank Transactions"])
api_router.include_router(imports_router, prefix="/imports", tags=["Imports"])
api_router.include_router(ledger_transactions_router, prefix="/ledger-transactions", tags=["Ledger Transactions"])
api_router.include_router(reconciliations_router, prefix="/reconciliations", tags=["Reconciliations"])
api_router.include_router(uploads_router, prefix="/uploads", tags=["Uploads"])
