from fastapi import FastAPI, Depends
from .routes import router as iam_router
from fastapi.middleware.cors import CORSMiddleware
from .auth import require_api_key

app = FastAPI(title="AWS IAM Management Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply API key dependency to all `/api` routes. The dependency is a no-op
# if `API_KEY` env var is not set which keeps tests/dev flows simple.
app.include_router(iam_router, prefix="/api", dependencies=[Depends(require_api_key)])


@app.get("/health")
def health():
    return {"status": "ok"}
