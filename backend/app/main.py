from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import SessionLocal, wait_for_database
from app.services.bootstrap import seed_initial_superuser


@asynccontextmanager
async def lifespan(_: FastAPI):
    wait_for_database()
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    db = SessionLocal()
    try:
        seed_initial_superuser(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All versioned API routers, including bank and ledger transaction queries,
# are registered through the central v1 router.
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} online"}
