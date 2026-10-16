# AI Travel Advisor API

An AI-powered travel planning backend built with Python, FastAPI, and the OpenAI API.

The API generates personalized travel itineraries, uses web search when relevant, applies basic request safety checks, reports token usage, and checks the arithmetic consistency of estimated budgets.

## Live deployment

- **API base URL:** https://ai-travel-advisor-seven.vercel.app
- **Health check:** https://ai-travel-advisor-seven.vercel.app/health
- **Interactive API documentation:** https://ai-travel-advisor-seven.vercel.app/docs
- **Chat endpoint:** `POST /chat`

## Technologies

- Python
- FastAPI
- OpenAI Responses API
- OpenAI Moderation API
- Pydantic
- Uvicorn
- Vercel

## Features

- Personalized day-by-day travel itineraries.
- Web search for relevant travel information.
- Conversation continuity using `previous_response_id`.
- Basic request safety checks and moderation.
- Input and output token usage reporting.
- Arithmetic validation of estimated budget totals.
- HTTP API endpoints for health checks and chat requests.

## Run locally on Windows

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure the OpenAI API key

Create a local file named `chiave 1510.env` in the project root:

```dotenv
OPENAI_API_KEY=your_openai_api_key
```

Replace the example value with your own key. Never commit this file to Git.

### 4. Start the API

```powershell
python -m uvicorn api:app --reload
```

The local API is available at `http://127.0.0.1:8000`.

Open `http://127.0.0.1:8000/docs` to explore and test the endpoints.

## API endpoints

### Health check

`GET /health`

Example response:

```json
{
  "status": "ok"
}
```

### Chat

`POST /chat`

Example request to start a conversation:

```json
{
  "message": "Plan a 2-day trip to Bologna focused on food and museums."
}
```

To continue the same conversation, send the `response_id` from the previous response as `previous_response_id`:

```json
{
  "message": "Can you reduce the budget?",
  "previous_response_id": "YOUR_PREVIOUS_RESPONSE_ID"
}
```

The response includes the generated answer, the latest response ID, token usage, a safety status, and a budget validation result.

Budget validation checks arithmetic consistency. It does not guarantee that estimated prices are accurate or currently available.

## Environment variables

For local development, the application reads `OPENAI_API_KEY` from `chiave 1510.env` or `.env`.

For Vercel, configure `OPENAI_API_KEY` in the project's Environment Variables settings. Do not upload the local environment file to GitHub.

## Security and limitations

This is an educational project and a work in progress.

The current chat endpoint does not implement user authentication or request rate limiting. Do not use it as an unrestricted public service without additional protections.

The current budget validation checks the arithmetic consistency of detected budget items. It does not independently verify real-world prices.

The existing `saved_trips.json` file is used for local project data and is not automatically a persistent, multi-user database for the deployed API.

## Repository

https://github.com/ivanmatteuzzi/ai-travel-advisor