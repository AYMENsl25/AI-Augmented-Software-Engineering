"""Tool calling — order lookup.

Task: the model must decide to call the `get_order_status` tool with the order id it
finds in the user's message, then use the returned status in a short reply.

Fill in YOUR_SYSTEM_PROMPT and the tool schema TODO.
Run:  python tool_calling.py
"""
from ollama import chat

MODEL = "llama3.1:8b"

FAKE_DB = {
    "4412": "shipped, arriving Friday",
    "9001": "processing",
}


def get_order_status(order_id: str) -> str:
    return FAKE_DB.get(order_id, "not found")


# Describe the lookup tool and its argument for the model.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Look up the current shipping or processing status of a customer's order by its order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The exact order number stated by the customer, as a string of digits; do not guess or change it."},
                },
                "required": ["order_id"],
            },
        },
    }
]

# Ask for a lookup before answering an order-status question.
YOUR_SYSTEM_PROMPT = """You are an online store support assistant. When a customer asks
about an order's status, first call get_order_status using the exact order ID from
their message. Do not invent a status. After the tool returns, use its result in
a short, clear reply to the customer."""


def run() -> bool:
    message = "Hi, can you check on order 4412 for me?"
    resp = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": YOUR_SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        tools=TOOLS,
        options={"temperature": 0.0},
    )
    calls = resp.message.tool_calls or []
    if not calls:
        print("[FAIL] model did not call the tool")
        return False
    call = calls[0]
    order_id = str(call.function.arguments.get("order_id"))
    ok = order_id == "4412"
    print(f"[{'PASS' if ok else 'FAIL'}] tool called with order_id={order_id!r}")
    if ok:
        print("tool result:", get_order_status(order_id))
    return ok


if __name__ == "__main__":
    run()
