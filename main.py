from fastapi import FastAPI
from src.dslbank import get_dsl

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Plugin for Domain Specific Language that can be used in LLM's to generate programs."}

@app.get("/dsl")
async def read_dsl(name: str):
    """Return the DSL by name."""
    return get_dsl(name)
