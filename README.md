# Token & Cost Tracker CLI

A simple Python CLI tool that uses `tiktoken` to track LLM token usage, estimate per-call cost, and log usage details to a CSV file.

## Features

- Counts input and output tokens for a given text prompt and response using `tiktoken`.
- Estimates cost based on configurable per-1K-token prices for prompt and completion.
- Logs each interaction to a CSV file with date, model, token counts, and cost.
- Optional verbose mode to print details to the console.

## Requirements

- Python 3.10+ recommended
- Dependencies listed in `requirements.txt`:
  - `tiktoken`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Basic tracking example:

```bash
python tracker.py --model gpt-3.5-turbo --prompt "Hello" --response "Hi there!" --verbose
```

This will:

- Compute input and output token counts for the prompt and response.
- Calculate the total cost using fixed per‑1K‑token prices.
- Append a row to `usage_log.csv`:

```text
Date,Model,Input Tokens,Output Tokens,Cost
2026-01-02T12:18:20,gpt-3.5-turbo,1,3,0.000005
```

Verbose mode prints a human-readable summary to stdout; omit `--verbose` if you only want CSV logging.

## Configuration

Inside `tracker.py` you can adjust pricing:

```
INPUT_PRICE_PER_1K = 0.0005   # prompt tokens
OUTPUT_PRICE_PER_1K = 0.0015  # completion tokens
```

Update these values to match your current LLM provider’s pricing.
