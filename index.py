from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

HUMANIZE_SYSTEM_PROMPT = """You are an expert writing assistant that rewrites AI-generated text to sound authentically human.

Your rewriting rules:
1. VARY sentence length dramatically — mix very short sentences with longer flowing ones. Humans write in bursts.
2. Use natural, conversational transitions instead of "Furthermore", "Moreover", "In conclusion", "It is worth noting".
3. AVOID these AI giveaway words: delve, crucial, multifaceted, nuanced, robust, leverage, utilize, paradigm, holistic, comprehensive, pivotal, myriad, testament, embark, foster, streamline, groundbreaking, cutting-edge, it's important to note, notably, certainly, absolutely.
4. Add slight informality where appropriate — contractions (it's, don't, we've), occasional colloquialisms.
5. Vary paragraph length. Some can be one sentence.
6. Make word choices slightly less predictable — choose the interesting word, not the safe one.
7. Preserve ALL original meaning, facts, and information completely.
8. Do NOT add new information or change any facts.
9. Match the original tone (academic, casual, professional) but make it sound human.
10. Output ONLY the rewritten text — no explanations, no preamble, no meta-commentary."""


class HumanizeRequest(BaseModel):
    text: str


@app.get("/")
async def root():
    return {"status": "HumanizeAI backend is running ✦"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/humanize")
async def humanize(request: HumanizeRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    if len(request.text) > 10000:
        raise HTTPException(status_code=400, detail="Text too long. Max 10,000 characters.")

    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured.")

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                CLAUDE_API_URL,
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1500,
                    "system": HUMANIZE_SYSTEM_PROMPT,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Rewrite this text to sound authentically human:\n\n{request.text}"
                        }
                    ]
                }
            )

            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="Claude API error.")

            data = response.json()
            humanized = data["content"][0]["text"]
            return {"humanized": humanized}

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Request timed out. Please try again.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
