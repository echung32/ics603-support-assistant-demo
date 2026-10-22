"""FastAPI routes and the placeholder support page."""

from decimal import Decimal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.agent import ChatRequest, ChatResponse, Refund

app = FastAPI(title="Support assistant skeleton")

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Support assistant</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 0; color: #243349;
           background: #f4f6f8; }
    main { max-width: 1050px; margin: auto; padding: 24px; }
    .grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px; }
    .panel { padding: 20px; border: 1px solid #cbd3dd; border-radius: 8px;
             background: white; }
    h2 { margin-top: 32px; }
    h3 { margin-top: 0; }
    textarea { box-sizing: border-box; width: 100%; min-height: 130px;
               padding: 10px; font: inherit; }
    button { margin-top: 12px; padding: 10px 18px; font: inherit; }
    .content { white-space: pre-wrap; overflow-wrap: anywhere; }
    @media (max-width: 650px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main>
    <h1>Support assistant</h1>
    <p>Skeleton demo: every submission returns the same example.
       No refund is processed or sent for review.</p>

    <h2>Customer support</h2>
    <div class="grid">
      <section class="panel">
        <h3>Your question</h3>
        <form id="question-form" action="/chat" method="post">
          <label for="question">How can we help?</label>
          <textarea id="question" name="question" required></textarea>
          <button id="send" type="submit">Send</button>
        </form>
        <p id="error" role="alert"></p>
      </section>
      <section class="panel" aria-live="polite">
        <h3>Answer</h3>
        <p id="answer" class="content">Submit a question to see the placeholder answer.</p>
      </section>
      <section class="panel" aria-live="polite">
        <h3>Refund outcome</h3>
        <p id="refund" class="content">No example displayed yet.</p>
      </section>
      <section class="panel">
        <h3>Earlier in this conversation</h3>
        <p>Conversation history placeholder. Messages are not saved.</p>
      </section>
    </div>

    <h2>Staff review — placeholders</h2>
    <div class="grid">
      <section class="panel">
        <h3>Waiting for review</h3>
        <p>Review queue placeholder.</p>
      </section>
      <section class="panel">
        <h3>Customer's message</h3>
        <p>Customer message placeholder.</p>
      </section>
      <section class="panel">
        <h3>Proposal from the model</h3>
        <p>Order ID, amount, and reason placeholder.</p>
      </section>
      <section class="panel">
        <h3>Order record</h3>
        <p>Order ID, order total, and date placed placeholder.</p>
      </section>
      <section class="panel">
        <h3>Policy check</h3>
        <p>Policy outcome and reason placeholder. No rules are evaluated.</p>
      </section>
      <section class="panel">
        <h3>Decision</h3>
        <button type="button" disabled>Approve</button>
        <button type="button" disabled>Reject (undecided)</button>
      </section>
    </div>
  </main>
  <script>
    const form = document.getElementById('question-form');
    const send = document.getElementById('send');
    const error = document.getElementById('error');
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      send.disabled = true;
      error.textContent = '';
      try {
        const response = await fetch(form.action, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: document.getElementById('question').value })
        });
        if (!response.ok) throw new Error('Request failed');
        const data = await response.json();
        document.getElementById('answer').textContent = data.answer;
        document.getElementById('refund').textContent = data.refund
          ? `Example status: ${data.refund.status}\\nOrder: ${data.refund.order_id}`
            + `\\nAmount: $${data.refund.amount}\\nReason: ${data.refund.reason}`
          : 'No refund proposed.';
      } catch {
        error.textContent = 'Could not load the placeholder response. Please try again.';
      } finally {
        send.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Show the support and staff review placeholders."""
    return PAGE


@app.post("/chat", response_model=ChatResponse)
def chat(_request: ChatRequest) -> ChatResponse:
    """Return a fixed example without interpreting the question."""
    return ChatResponse(
        answer="Placeholder answer: your question was received. This is a static demo.",
        refund=Refund(
            order_id="A-1001",
            amount=Decimal("60.00"),
            reason="Placeholder only: wrong color. No actual review has been created.",
            status="pending_review",
        ),
    )
