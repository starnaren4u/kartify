# Kartify

Kartify is a conversational order support agent. It classifies customer requests, looks up order details from a local SQLite database, drafts a response, and runs evaluation and safety checks before returning the answer. The current chat interface runs in the terminal.

## Requirements

- Python 3.12 or newer
- An OpenAI API key, or credentials for a compatible OpenAI API endpoint
- The order database at `src/kartify/data/kartify.db`

## Run locally (Windows PowerShell)

From the project root, create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly in the commands below instead.

Install the project and its dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

Create your local environment file and add your API credentials:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace `your-openai-api-key` with your key. Set `OPENAI_BASE_URL` to your API endpoint; for OpenAI's API, use `https://api.openai.com/v1`. Keep `.env` private and do not commit it.

Start the chat agent:

```powershell
python main.py
```

The agent prompts for a customer ID and then accepts order-related questions in the terminal. Set `DEBUG_LOGGERS_ENABLED=false` in `.env` to turn off graph state logging; use `true` to enable it.

## Run tests

```powershell
python -m unittest discover -s tests
```
