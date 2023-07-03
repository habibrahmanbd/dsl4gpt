from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from typing import Any, Dict
import json
import uvicorn
from src.dslbank import get_dsl

app = FastAPI()

router = APIRouter(include_in_schema=False)

class DSLWrapper(BaseModel):
    domain: str
    format: str
    dsl: str

@app.get("/dsl", response_model=DSLWrapper)
async def read_dsl(name: str):
    """Return the DSL by name from the DSLBank."""
    return DSLWrapper(domain=name, format="tex", dsl=get_dsl(name))

@router.get("/.well-known/ai-plugin.json")
async def ai_plugin():
    """Return the contents of the manifest.json file."""
    try:
        with open('./manifest.json', 'r') as file:
            data = json.load(file)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

app.include_router(router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="dsl4llm",
        version="0.0.1",
        description="Plugin for Domain Specific Languages for Large Language Models to generate code based on the DSL.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

