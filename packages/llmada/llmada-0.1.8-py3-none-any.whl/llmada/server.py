""" work """
import time
from typing import List, Optional, Dict, Any, Union, Literal

from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.responses import StreamingResponse


from models.types import ChatCompletionResponse,ChatCompletionRequest
from models.factory import ModelFactory,MyModel
import os

# --- FastAPI App ---

app = FastAPI(
    title="OpenAI-Compatible LLM Service",
    description="Provides an OpenAI-compatible API for custom large language models.",
    version="1.0.0",
)

# TODO
model_factory = ModelFactory()
model_factory.register_model(MyModel())

async def generate_llm_response(prompt: str, stream: bool, model: str):
    """
    Replace this with your actual LLM call logic.
    This mock function simulates generating text.
    """
    infer = model_factory.get_handler(model)
    if not stream:
        result = await infer.generate(prompt,model=model)
    else:
        result = await infer.generate_stream(prompt,model=model)
    return result



# --- Configure CORS ---
# ! Add this section !
# Define allowed origins. Be specific in production!
# Example: origins = ["http://localhost:3000", "https://your-frontend-domain.com"]
origins = [
    "*", # Allows all origins (convenient for development, insecure for production)
    # Add the specific origin of your "别的调度" tool/frontend if known
    # e.g., "http://localhost:5173" for a typical Vite frontend dev server
    # e.g., "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies the allowed origins
    allow_credentials=True, # Allows cookies/authorization headers
    allow_methods=["*"],    # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],    # Allows all headers (Content-Type, Authorization, etc.)
)
# --- End CORS Configuration ---



# --- (Optional) Authentication Dependency ---
async def verify_api_key(authorization: Optional[str] = Header(None)):
    """
    Placeholder for API key verification.
    In a real application, you'd compare this to a stored list of valid keys.
    """
    if not authorization:
        # Allow requests without Authorization for local testing/simplicity
        # OR raise HTTPException for stricter enforcement
        # raise HTTPException(status_code=401, detail="Authorization header missing")
        print("Warning: Authorization header missing.")
        return None # Or a default principal/user if needed

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization scheme")

    token = authorization.split(" ")[1]
    # --- Replace this with your actual key validation logic ---
    # Example:
    # valid_keys = {"your-secret-key-1", "your-secret-key-2"}
    # if token not in valid_keys:
    #     raise HTTPException(status_code=401, detail="Invalid API Key")
    # print(f"Received valid API Key (last 4 chars): ...{token[-4:]}")
    # --- End Replace ---
    print(f"Received API Key (placeholder validation): ...{token[-4:]}")
    return token # Return the token or an identifier associated with it


# --- API Endpoint Implementation ---

@app.post(
    "/v1/chat/completions",
    response_model=None, # Response model needs dynamic handling (stream vs non-stream)
    summary="Chat Completions",
    description="Creates a model response for the given chat conversation.",
    tags=["Chat"],
)
async def create_chat_completion(
    request: ChatCompletionRequest,
    # token: str = Depends(verify_api_key) # Uncomment to enable authentication
):
    prompt_for_llm = "\n".join([f"{msg.role}: {msg.content}" for msg in request.messages if msg.content])
    print("-" * 20)
    print(f"Received Request for model: {request.model}")
    print(f"Streaming: {request.stream}")
    # print(f"Prompt for LLM:\n{prompt_for_llm}") # Be careful logging prompts with sensitive data
    print("-" * 20)

    try:
        response_data = await generate_llm_response(
            prompt=prompt_for_llm,
            stream=request.stream,
            model=request.model # Echo back the requested model
        )
    except Exception as e:
        print(f"Error calling LLM backend: {e}")
        raise HTTPException(status_code=500, detail=f"LLM backend error: {str(e)}")


    # --- 3. Format and Return Response ---
    if request.stream:
        if not isinstance(response_data, EventSourceResponse):
             raise HTTPException(status_code=500, detail="Streaming response was not generated correctly.")
        return response_data # Return the SSE stream directly
    else:
        print(type(response_data))
        print(isinstance(response_data, ChatCompletionResponse))
        # if not isinstance(response_data, ChatCompletionResponse):
        #      raise HTTPException(status_code=500, detail="Non-streaming response was not generated correctly.")
        return response_data # FastAPI automatically converts Pydantic model to JSON


# --- (Optional) Add other OpenAI-like endpoints if needed ---
# For example, /v1/models to list available models
class ModelCard(BaseModel):
    id: str
    object: Literal["model"] = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "your-organization" # Customize as needed

class ModelList(BaseModel):
    object: Literal["list"] = "list"
    data: List[ModelCard] = []

@app.get("/")
async def root():
    return {"message": "OpenAI-Compatible LLM Service is running."}

@app.get("/v1/models", response_model=ModelList,  tags=["Models"])
async def list_models():
    """Lists the models available through the factory."""
    available_model_ids = model_factory.get_available_models()
    available_models = [ModelCard(id=model_id) for model_id in available_model_ids]
    return ModelList(data=available_models)

# if __name__ == "__main__":
#     # !uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# --- 运行服务器 ---
if __name__ == "__main__":
    import uvicorn
    # 从环境变量读取主机和端口，方便 Docker 部署
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)