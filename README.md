# Writer–Critic

Two agents and a loop, in about 40 lines. One writes, the other decides whether it's good enough.

This is the smallest multi-agent system that is actually worth running: the Writer can't
grade itself, so the Critic is an independent verifier — the same reason a code reviewer
isn't the person who wrote the code.

## Run it

Everything runs on your own laptop: no account, no API key, no cost. You need git,
Python 3.9 or newer, and about 4 GB of free disk space for the model.

### 1. Install Ollama and download the model

Ollama runs open models locally. Install it from <https://ollama.com/download>
(macOS with Homebrew: `brew install ollama`), then:

```bash
ollama serve          # leave this running in a second terminal; skip if the Ollama app is open
ollama pull gemma3    # Google's open Gemma model, one-time 3.3 GB download
```

### 2. Get the code

```bash
git clone https://github.com/1luvc0d3/multi-agent-talk-01
cd multi-agent-talk-01
python3 -m venv .venv            # Windows: python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install openai python-dotenv
cp .env.example .env             # Windows cmd: copy .env.example .env
```

`.env` is already set up for Ollama and Gemma, so there is nothing to edit.

### 3. Run it

```bash
python writer_critic.py "Explain TCP congestion control to a first-year student"
```

You should see `=== draft 1 ===`, possibly a critique and more drafts, then either
`=== approved on round N ===` or `=== stopped after 3 rounds without approval ===`, and
finally `=== final ===`.

### If it fails

- `KeyError: 'API_KEY'`: there is no `.env` file next to `writer_critic.py`. Redo the last line of step 2.
- `Connection error`: Ollama isn't running. Start `ollama serve` and try again.
- `model 'gemma3' not found`: run `ollama pull gemma3`.

### Optional: use a hosted model instead

The same code works with any OpenAI-compatible endpoint, such as OpenAI, Google or Groq.
These need an account and an API key, and some charge per request. Put your key in
`API_KEY` in `.env`, and set `BASE_URL` and `MODEL` to the pair listed for your provider in
the comments at the top of that file.

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
