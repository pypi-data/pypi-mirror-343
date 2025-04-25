from importlib.metadata import PackageNotFoundError, version

# This is used to avoid circular imports
from typing import TYPE_CHECKING

from packaging.version import parse as parse_version
from wrapt import wrap_function_wrapper

if TYPE_CHECKING:
    from pillar.client import Pillar

# Pillar imports
from pillar.interceptor.hooks.openai.chat_completions import hook_chat_completions


def _register_hooks_openai(pillar_client: "Pillar") -> None:
    """
    Register hooks for OpenAI.
    """
    try:
        raw_openai_version = version("openai")
        parsed_openai_version = parse_version(raw_openai_version)
    except PackageNotFoundError:
        return

    if parsed_openai_version < parse_version("1.0.0"):
        wrap_function_wrapper(
            "openai", "ChatCompletion.create", hook_chat_completions(pillar_client)
        )
    else:
        wrap_function_wrapper(
            "openai.resources.chat.completions",
            "Completions.create",
            hook_chat_completions(pillar_client),
        )
