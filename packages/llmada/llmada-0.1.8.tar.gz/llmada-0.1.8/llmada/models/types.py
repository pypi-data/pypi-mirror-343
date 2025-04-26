import time
import uuid
from typing import List, Optional, Dict, Any, Union, Literal
from pydantic import BaseModel, Field


# --- Pydantic Models (Matching OpenAI Structures) ---

class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: Optional[str] = None
    # tool_calls: Optional[...] # Add if you support tool/function calling
    # tool_call_id: Optional[...] # Add if you support tool/function calling

class ChatCompletionRequest(BaseModel):
    model: str  # The model name you want your service to expose
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1 # How many chat completion choices to generate for each input message.
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = 2048 # Adjusted default for flexibility
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    # Add other parameters if your model supports them (e.g., seed, tool_choice)

# --- Response Models (Non-Streaming) ---

class ChatCompletionMessage(BaseModel):
    role: Literal["assistant", "tool"] # Usually assistant
    content: Optional[str] = None
    # tool_calls: Optional[...]

class Choice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = "stop"
    # logprobs: Optional[...]

class UsageInfo(BaseModel):
    prompt_tokens: int = 0 # You might need to implement token counting
    completion_tokens: int = 0
    total_tokens: int = 0

class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex}")
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str # Echo back the model requested or the one used
    choices: List[Choice]
    usage: UsageInfo = Field(default_factory=UsageInfo)
    # system_fingerprint: Optional[str] = None

# --- Response Models (Streaming) ---

class DeltaMessage(BaseModel):
    role: Optional[Literal["system", "user", "assistant", "tool"]] = None
    content: Optional[str] = None
    # tool_calls: Optional[...]

class ChunkChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = None
    # logprobs: Optional[...]

class ChatCompletionChunkResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex}")
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChunkChoice]
    # system_fingerprint: Optional[str] = None
    # usage: Optional[UsageInfo] = None # Usage is typically not included in chunks until the *very* end in some implementations or omitted
