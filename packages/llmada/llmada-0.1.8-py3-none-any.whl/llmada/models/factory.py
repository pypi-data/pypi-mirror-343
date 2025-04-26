# llm_interface.py (or within main.py initially)
import abc
import time
import uuid
import asyncio
from typing import AsyncGenerator, List, Dict, Any, Optional, Union, Literal

from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from .types import ChatMessage,ChatCompletionRequest,ChatCompletionMessage,Choice,UsageInfo
from .types import ChatCompletionResponse,DeltaMessage,ChunkChoice, ChatCompletionChunkResponse


class ModelFactory:
    def __init__(self):
        self._handlers: Dict[str, LLMInterface] = {}

    def register_model(self, handler_instance: LLMInterface):
        model_name = handler_instance.get_model_name()
        if model_name in self._handlers:
            print(f"Warning: Overwriting handler for model '{model_name}'")
        print(f"Registering handler for model: {model_name}")
        self._handlers[model_name] = handler_instance

    def get_handler(self, model_name: str) -> Optional[LLMInterface]:
        return self._handlers.get(model_name)

    def get_available_models(self) -> List[str]:
        return list(self._handlers.keys())


class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None
    # ... other fields if necessary

class LLMInterface(abc.ABC):
    """Abstract Base Class for Language Model Handlers."""

    @abc.abstractmethod
    def get_model_name(self) -> str:
        """Returns the unique name of the model this handler supports."""
        pass

    @abc.abstractmethod
    async def generate(
        self,
        prompt: str,
        model: str,
        # Add other relevant parameters from ChatCompletionRequest
        **kwargs: Any # For future flexibility
    ) -> Dict[str, Any]:
        """
        Generates a non-streaming response.
        Should return a dictionary containing at least:
        - 'content': The generated text content (str)
        - 'finish_reason': The reason generation stopped (str)
        - Optional: 'prompt_tokens', 'completion_tokens' (int)
        """
        pass

    @abc.abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        model: str,
        # Add other relevant parameters from ChatCompletionRequest
        **kwargs: Any
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generates a streaming response.
        Should yield dictionaries containing:
        - 'delta_content': The content chunk for this step (str)
        - 'finish_reason': The reason generation stopped (str, usually None until the last chunk)
        - Optional first chunk: 'role': The role ('assistant')
        """
        pass



# TODO 
class MyModel(LLMInterface):
    MODEL_NAME = "mock-beta-test4"

    def get_model_name(self) -> str:
        return self.MODEL_NAME


    async def generate(
        self,
        prompt: str,
        model: str,
    ) -> Dict[str, Any]:
        choice = Choice(
            index=0,
            message=ChatCompletionMessage(role="assistant", content=" This is a simulated  response  from the model"),
            finish_reason="stop"
        )
        response_id = f"chatcmpl-{uuid.uuid4().hex}"
        created_time = int(time.time())
        words = [1,3,4,5]
        # Simulate token counts (highly inaccurate)
        usage = UsageInfo(prompt_tokens=len(prompt.split()), completion_tokens=len(words), total_tokens=len(prompt.split()) + len(words))
        return ChatCompletionResponse(
            id=response_id,
            model=model,
            choices=[choice],
            usage=usage,
            created=created_time
        )
    
    async def generate_stream(
        self,
        prompt: str,
        model: str,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        response_id = f"chatcmpl-{uuid.uuid4().hex}"
        created_time = int(time.time())
        words = ["This", "is", "a", "simulated", "response", "from", "the", model, "model.", "It", "demonstrates", "streaming."]

        
        async def stream_generator():
            # First chunk: Send role
            first_chunk_choice = ChunkChoice(index=0, delta=DeltaMessage(role="assistant"), finish_reason=None)
            yield ChatCompletionChunkResponse(
                id=response_id, model=model, choices=[first_chunk_choice], created=created_time
            ).model_dump_json() # Use model_dump_json() for Pydantic v2

            # Subsequent chunks: Send content word by word
            for i, word in enumerate(words):
                chunk_choice = ChunkChoice(index=0, delta=DeltaMessage(content=f" {word}"), finish_reason=None)
                yield ChatCompletionChunkResponse(
                    id=response_id, model=model, choices=[chunk_choice], created=created_time
                ).model_dump_json()
                await asyncio.sleep(0.05) # Simulate token generation time

            # Final chunk: Send finish reason
            final_chunk_choice = ChunkChoice(index=0, delta=DeltaMessage(), finish_reason="stop")
            yield ChatCompletionChunkResponse(
                id=response_id, model=model, choices=[final_chunk_choice], created=created_time
            ).model_dump_json()

            # End of stream marker (specific to SSE)
            yield "[DONE]"

        # Need to wrap the generator for EventSourceResponse
        async def event_publisher():
            try:
                async for chunk in stream_generator():
                    yield {"data": chunk}
                    await asyncio.sleep(0.01) # Short delay between sending chunks is good practice
            except asyncio.CancelledError as e:
                print("Streaming connection closed by client.")
                raise e

        return EventSourceResponse(event_publisher())
        
