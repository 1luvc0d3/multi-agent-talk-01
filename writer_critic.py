"""Two agents, one loop: a Writer drafts, a Critic approves or sends it back.

Run:  python writer_critic.py "Explain TCP congestion control to a first-year student"
"""
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI  # works with any OpenAI-compatible endpoint

load_dotenv()  # reads API_KEY, BASE_URL and MODEL from .env

MODEL = os.environ.get("MODEL", "gpt-4o-mini")
MAX_ROUNDS = 3  # the stop condition. Without this, a loop never ends.

client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ.get("BASE_URL", "https://api.openai.com/v1"),
)

WRITER = """You are the Writer.
Write a clear answer in under 150 words.
If you are given critique, revise the draft to address every point.
Output the answer only, with no preamble."""

CRITIC = """You are the Critic. You never write the answer yourself.
Check the draft against this checklist:
  1. Is it correct?
  2. Would a first-year student follow it?
  3. Is it under 150 words?
  4. Does it avoid undefined jargon?
If every item passes, reply with exactly: APPROVED
Otherwise list the failures as short numbered fixes."""


def ask(role: str, message: str) -> str:
    """One turn of one agent. This is the whole 'agent' primitive."""
    reply = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": message},
        ],
    )
    return reply.choices[0].message.content.strip()


def main() -> None:
    question = " ".join(sys.argv[1:]) or "Explain what a rate limiter does."

    draft = ask(WRITER, question)
    for round_number in range(1, MAX_ROUNDS + 1):
        print(f"\n=== draft {round_number} ===\n{draft}")

        critique = ask(CRITIC, f"Question: {question}\n\nDraft:\n{draft}")
        if critique.startswith("APPROVED"):
            print(f"\n=== approved on round {round_number} ===")
            break

        print(f"\n--- critique {round_number} ---\n{critique}")
        draft = ask(WRITER, f"Question: {question}\n\nYour draft:\n{draft}\n\nCritique:\n{critique}")
    else:
        print(f"\n=== stopped after {MAX_ROUNDS} rounds without approval ===")

    print(f"\n=== final ===\n{draft}")


if __name__ == "__main__":
    main()
