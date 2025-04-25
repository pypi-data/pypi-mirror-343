import uuid
from collections.abc import Callable
from contextvars import ContextVar

# Pillar
from pillar.callbacks import (
    IsFlaggedCallable,
    OnFlaggedCallbackType,
    default_is_flagged,
    id_on_flagged,
)
from pillar.types import API_REQUEST, API_RESPONSE

# === Context Variables - For session ===
pillar_session_id: ContextVar[str | None] = ContextVar(
    "pillar_session_id", default=str(uuid.uuid4())
)
pillar_user_id: ContextVar[str | None] = ContextVar("pillar_user_id", default=None)

pillar_is_flagged_fn: ContextVar[IsFlaggedCallable] = ContextVar(
    "pillar_is_flagged_fn", default=default_is_flagged
)
pillar_on_flagged_fn: ContextVar[OnFlaggedCallbackType] = ContextVar(
    "pillar_on_flagged_fn", default=id_on_flagged
)


# === Update Context from Response Callback ===
def update_context_from_response(request: API_REQUEST, response: API_RESPONSE) -> None:
    """Default update context from response."""
    pillar_session_id.set(response.session_id)


# === Get Context Variables Names ===


def get_fn_name(fn: Callable) -> str:
    """Get the name of a function."""
    if hasattr(fn, "__name__"):
        return str(fn.__name__)
    return str(fn)


def get_on_flagged_fn_name() -> str:
    """Get the name of the on flagged function."""
    fn = pillar_on_flagged_fn.get()
    return get_fn_name(fn)


def get_is_flagged_fn_name() -> str:
    """Get the name of the flagged detector function."""
    fn = pillar_is_flagged_fn.get()
    return get_fn_name(fn)
