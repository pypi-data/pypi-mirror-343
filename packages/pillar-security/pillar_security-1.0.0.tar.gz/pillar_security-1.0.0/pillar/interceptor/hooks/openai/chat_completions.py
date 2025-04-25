import traceback
from collections.abc import Callable, Generator, Iterable
from typing import TYPE_CHECKING, Any

from openai.types.chat import ChatCompletionChunk

from pillar.errors import PillarBlockError
from pillar.types import PillarMessage, Role

# This is used to avoid circular imports
if TYPE_CHECKING:
    from pillar.client import Pillar

PROVIDER = "openai"


def collect_messages_from_stream(stream: Iterable[ChatCompletionChunk]) -> list[PillarMessage]:
    results: list[PillarMessage] = []
    current_message: dict[str, Any] | None = None
    tool_calls_by_index: dict[int, dict[str, Any]] = {}

    for chunk in stream:
        choice = chunk.choices[0]
        delta = choice.delta

        if current_message is None:
            current_message = {
                "role": delta.role or Role.ASSISTANT.value,
                "content": "",
                "tool_calls": [],
            }

        if delta.content:
            current_message["content"] += delta.content

        if delta.tool_calls:
            for tool_call in delta.tool_calls:
                idx = tool_call.index
                existing = tool_calls_by_index.get(
                    idx, {"id": "", "type": "", "function": {"name": "", "arguments": ""}}
                )
                if tool_call.id:
                    existing["id"] = tool_call.id
                if tool_call.type:
                    existing["type"] = tool_call.type
                if tool_call.function:
                    if tool_call.function.name:
                        existing["function"]["name"] = tool_call.function.name
                    if tool_call.function.arguments:
                        existing["function"]["arguments"] += tool_call.function.arguments
                tool_calls_by_index[idx] = existing

        if choice.finish_reason:
            if tool_calls_by_index:
                current_message["tool_calls"] = [
                    tool_calls_by_index[i] for i in sorted(tool_calls_by_index)
                ]
            message = PillarMessage(
                role=Role.ASSISTANT.value,
                content=current_message["content"],
                tool_calls=current_message["tool_calls"],
            )
            results.append(message)
            current_message = None
            tool_calls_by_index = {}

    return results


def analyze_and_forward_stream(
    pillar: "Pillar", stream: Iterable[ChatCompletionChunk], model: str
) -> Generator[ChatCompletionChunk, None, None]:
    chunks = []

    try:
        for chunk in stream:
            chunks.append(chunk)
            yield chunk
    except Exception:
        pillar.logger.error("Exception during stream passthrough")
        pillar.logger.error(traceback.format_exc())

    try:
        messages = collect_messages_from_stream(chunks)
        if messages:
            pillar.analyze_sync(
                messages=messages,
                tools=None,
                model=model,
                provider=PROVIDER,
            )
    except Exception:
        pillar.logger.error("Exception during pillar.analyze_sync")
        pillar.logger.error(traceback.format_exc())


def hook_chat_completions(pillar: "Pillar") -> Callable:
    def hook(wrapped: Callable, instance: Any, args: tuple, kwargs: dict) -> Any:
        try:
            function_name = "openai.chat.completions.create"
            if len(args) > 0:
                pillar.logger.error(
                    f"Expected {function_name} to be called with keyword arguments only"
                )
                return wrapped(*args, **kwargs)

            if "messages" not in kwargs:
                pillar.logger.error(
                    f"Expected {function_name} to be called with keyword argument messages"
                )
                return wrapped(*args, **kwargs)

            if "model" not in kwargs:
                pillar.logger.error(
                    f"Expected {function_name} to be called with keyword argument model"
                )
                return wrapped(*args, **kwargs)

            messages = kwargs["messages"]
            model = kwargs["model"]
            tools = kwargs.get("tools", [])

            pillar.logger.debug(f"messages: {messages}")
            pillar.logger.debug(f"tools: {tools}")
            pillar.logger.debug(f"model: {model}")
            # scan input
            messages_to_llm = pillar.analyze_sync(
                messages=messages,
                tools=tools,
                model=model,
                provider=PROVIDER,
            )

            # override the messages to llm with the messages to llm from the pillar response
            # get the wrapped function result - the actual response from the LLM
            result = wrapped(*args, **{**kwargs, "messages": messages_to_llm})

            # if the response is a stream, we need to handle it differently
            if kwargs.get("stream", False):
                return analyze_and_forward_stream(pillar, result, model)

            # scan output
            if hasattr(result, "choices") and result.choices:
                all_messages = [choice.message.to_dict() for choice in result.choices]
                _ = pillar.analyze_sync(
                    tools=tools,
                    messages=all_messages,
                    model=model,
                    provider=PROVIDER,
                )

            return result

        # Handle blocking errors
        except PillarBlockError as blocking_error:
            raise blocking_error
        # Handle other errors (API errors, etc.)
        except Exception:
            pillar.logger.error("Exception in openai.chat.completions.create hook")
            pillar.logger.error(traceback.format_exc())
            return wrapped(*args, **kwargs)

    return hook
