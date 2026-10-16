"""RAG — policy-grounded answers.

Task: answer a customer question using ONLY the retrieved help-center text. If the
answer isn't in the docs, the model must say it doesn't know (don't hallucinate).

Fill in YOUR_SYSTEM_PROMPT and YOUR_RETRIEVER.
Run:  python rag.py
"""
import os

from ollama import chat

MODEL = "llama3.1:8b"
DATA = os.path.join(os.path.dirname(__file__), "data", "help_center.txt")


def load_chunks() -> list[str]:
    with open(DATA, encoding="utf-8") as f:
        # one chunk per non-empty line
        return [line.strip() for line in f if line.strip()]


# Select help-center lines most relevant to the question.
def YOUR_RETRIEVER(question: str, chunks: list[str]) -> list[str]:
    stopwords = {"a", "an", "are", "can", "do", "for", "have", "how", "i", "is", "my", "the", "to", "you", "your"}
    words = {
        word.strip(".,:;!?'\" ")
        for word in question.lower().split()
    } - stopwords
    scored = []
    for chunk in chunks:
        chunk_words = {
            word.strip(".,:;!?'\" ")
            for word in chunk.lower().split()
        }
        score = sum(
            any(
                len(word) >= 4 and len(chunk_word) >= 4
                and (word.startswith(chunk_word) or chunk_word.startswith(word))
                for chunk_word in chunk_words
            )
            for word in words
        )
        if score:
            scored.append((score, chunk))
    best = max((score for score, _ in scored), default=0)
    return [chunk for score, chunk in scored if score == best]


# Require answers grounded in the retrieved context.
YOUR_SYSTEM_PROMPT = """You are an online store support assistant. Answer the
customer's question using only the supplied Context. Do not use outside
knowledge or invent facts. If the Context is empty or does not contain the
answer, say politely: I don't know based on our help center information.
Keep the answer short and state the relevant policy exactly."""

CASES = [
    ("How long do I have to return an item?", ["30 days"]),
    ("Do you ship internationally?", ["international"]),
    ("What's your CEO's home address?", ["don't know", "do not know", "not sure", "cannot"]),
]


def answer(question: str) -> str:
    context = "\n".join(YOUR_RETRIEVER(question, load_chunks()))
    resp = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": YOUR_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        options={"temperature": 0.0},
    )
    return resp.message.content.strip().lower()


def run() -> bool:
    passed = 0
    for question, needles in CASES:
        got = answer(question)
        ok = any(n.lower() in got for n in needles)
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {question!r} -> {got[:80]!r}")
    print(f"{passed}/{len(CASES)} correct")
    return passed == len(CASES)


if __name__ == "__main__":
    run()
