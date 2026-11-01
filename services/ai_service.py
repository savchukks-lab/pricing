"""Optional adapter to the existing UI-independent Responses service.

Import lazily so the skeleton starts without an API key or the optional SDK.
No case data is sent automatically.
"""


def draft_summary(prompt, context, *, client=None):
    from shared.openai_service import generate_text
    return generate_text(prompt, context, client=client)
