from fastapi import FastAPI

app = FastAPI(
    title="LLM Collab Room API",
    description="API service for the multi-LLM collaboration room.",
    version="0.1.0",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}
