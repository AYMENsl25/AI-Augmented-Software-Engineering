# Week 3 — Prompting Techniques

## 1. K-shot ticket classification

**Final system prompt:**

```text
Classify each customer message for an online store.
Reply with exactly one lowercase label: billing, shipping, returns, technical, or other.
Do not add an explanation, punctuation, or any other text.

Examples:
Message: My payment failed, but the money left my account.
Label: billing
Message: The tracking page says my parcel is delayed.
Label: shipping
Message: Can I exchange a jacket that does not fit?
Label: returns
Message: I cannot sign in because the website shows an error.
Label: technical
Message: What time does your store open?
Label: other

Now classify the next customer message.
```

**Observed sample:** `My card was charged twice for order 4412.` → `billing`

**Check result:** 4/4 correct with `llama3.1:8b`.

**What I learned:** Labeled examples show the model both how to map a message to a category and how short the answer must be. The explicit output rule helped make the response match the exact-label check.

## 2. Step-by-step refund decision

**Final system prompt:**

```text
Apply the refund policy below to the order description.
Check each eligibility requirement in order: purchased within 30 days,
unused/original condition, and not a final-sale item. For each requirement,
write PASS, FAIL, or UNKNOWN with a brief explanation based on the given facts.
Mark a requirement UNKNOWN if the order does not say; never assume it passed.
A refund is allowed only when every requirement is confirmed. If any requirement
fails or is unknown, the decision is NO. End with exactly one final line,
either DECISION: YES or DECISION: NO. Copy that line exactly, with no period,
other punctuation, or text after it.
```

**Observed sample input:** `Bought 5 days ago but it was a final-sale item.`

**Observed sample output:**

```text
Here are the results of the refund policy eligibility requirements:

1. Purchased within 30 days: PASS (bought 5 days ago, which is within 30 days)
2. Unused/original condition: UNKNOWN (order does not mention condition)
3. Not a final-sale item: FAIL (it was a final-sale item)

DECISION: NO
```

**Check result:** 3/3 correct with `llama3.1:8b`.

**What I learned:** A checklist helps the model apply every policy condition, while `UNKNOWN` prevents it from inventing a missing fact. I also inspected the raw response: the built-in check initially passed an answer ending `DECISION: NO.`, so passing the check alone did not prove the final line had the required exact format.

## 3. Order-status tool calling

**Final system prompt:**

```text
You are an online store support assistant. When a customer asks
about an order's status, first call get_order_status using the exact order ID from
their message. Do not invent a status. After the tool returns, use its result in
a short, clear reply to the customer.
```

**Tool description:** “Look up the current shipping or processing status of a customer's order by its order ID.” The `order_id` parameter asks for the exact number as a string, without guessing or changing it.

**Observed sample:** Customer: `Hi, can you check on order 4412 for me?` → model called `get_order_status(order_id="4412")` → tool returned `shipped, arriving Friday`.

**Check result:** PASS with `llama3.1:8b`.

**What I learned:** A tool schema gives the model a named action and a typed argument, so it can request a lookup rather than inventing an order status. This starter checks the call and argument, but it does not send the tool result back into a second model call; therefore it does not test the final customer reply.

## 4. Help-center retrieval

**Final system prompt:**

```text
You are an online store support assistant. Answer the
customer's question using only the supplied Context. Do not use outside
knowledge or invent facts. If the Context is empty or does not contain the
answer, say politely: I don't know based on our help center information.
Keep the answer short and state the relevant policy exactly.
```

**Retriever:** Compare meaningful words in the question with each help-center line, allowing longer word forms such as `internationally`/`international` and `shipping`/`ship`. Return only the highest-scoring lines; return no lines when there is no match.

**Observed sample:** `Do you ship internationally?` → retrieved `Shipping: We offer international shipping to most countries; delivery takes 7-21 business days.` → model answered `yes, we offer international shipping to most countries.`

**Check result:** 3/3 correct with `llama3.1:8b`. The unrelated CEO address question retrieved no lines, and the model answered `i don't know based on our help center information.`

**What I learned:** The model can stay grounded only if retrieval supplies the right evidence. My first retriever chose a billing line containing `ships` and missed `internationally`/`international`; the model then refused, which was appropriate for the wrong context but did not answer the customer's real question.

## Across all four techniques

The model handled structured tasks well when the prompt gave it a clear output shape, examples, policy checks, or a tool schema. It still needed scaffolding around the model: exact-format instructions, a tool that supplies real order data, and a retriever that selects relevant source text. The experiments also showed why checking the raw answer matters: a passing test can miss a formatting error or an unsupported intermediate claim.
