
import litellm

_original_completion = litellm.completion


def _completion_without_cache_breakpoint(*args, **kwargs):
    messages = kwargs.get("messages")

    if messages:
        cleaned_messages = []

        for message in messages:
            if isinstance(message, dict):
                message = {
                    key: value
                    for key, value in message.items()
                    if key != "cache_breakpoint"
                }
            cleaned_messages.append(message)

        kwargs["messages"] = cleaned_messages

    return _original_completion(*args, **kwargs)


def apply_groq_compatibility():
    litellm.completion = _completion_without_cache_breakpoint
