# Writer–Critic

Two agents and a loop, in about 40 lines. One writes, the other decides whether it's good enough.

This is the smallest multi-agent system that is actually worth running: the Writer can't
grade itself, so the Critic is an independent verifier — the same reason a code reviewer
isn't the person who wrote the code.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install openai python-dotenv
cp .env.example .env         # then put your key in .env
python writer_critic.py "Explain TCP congestion control to a first-year student"
```

Works with any OpenAI-compatible endpoint — OpenAI, Gemma, Groq, or Ollama on your own
laptop. `.env.example` has the settings for each.

## The part that matters

```python
MAX_ROUNDS = 3  # the stop condition
```

Delete that limit and the loop runs until the Critic happens to be satisfied, which may be
never. Every agent needs four things: a model, tools, a loop, and a stop condition. Most
people forget the fourth, and that's how you end up with a bill.

## Try these

1. **Make the Critic stricter.** Add a checklist item it will usually fail. Watch the round
   count rise and the cost with it.
2. **Make the Critic the Writer.** Give both the same prompt and ask it to grade its own
   draft. It approves almost everything. That's why the checker is never the doer.
3. **Log every handoff.** Print what goes between them each round. The quality of the whole
   system is the quality of those messages, not the cleverness of either agent.
4. **Add a third agent.** A Researcher that gathers facts before the Writer starts. Note
   where it blocks the others — that's the queue, and you're the one unblocking it.

## What a handoff should carry

Goal, inputs, constraints, definition of done, and what to do if blocked. The Critic prompt
here is that list in miniature. Leave out "if blocked" and an agent that gets stuck invents
something plausible instead of stopping.
