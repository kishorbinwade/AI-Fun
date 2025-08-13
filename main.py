# main.py - FastAPI Backend for AI Serendipity

from dotenv import load_dotenv
import os

# Load env variables first
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import hashlib
import random
from openai import OpenAI

# Init OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not set in .env file")
client = OpenAI(api_key=api_key)

app = FastAPI(
    title="AI Serendipity API",
    description="Backend API with GPT-4o integration",
    version="2.0.0"
)

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Models --------------------
class AffirmationRequest(BaseModel):
    language: Optional[str] = "english"

class AffirmationResponse(BaseModel):
    affirmation: str
    visual_element: str
    date: str
    mood_color: str

class RandomFunRequest(BaseModel):
    language: Optional[str] = "english"

class RandomFunResponse(BaseModel):
    type: str
    content: str
    emoji: str

class PersonalityRequest(BaseModel):
    input: str
    language: Optional[str] = "english"
    context: Optional[str] = None

class PersonalityResponse(BaseModel):
    insight: str
    traits: List[str]
    personality_type: str
    share_text: str
    confidence_score: float

# -------------------- Helpers --------------------
def get_date_hash():
    today = datetime.now().strftime("%Y-%m-%d")
    return hashlib.md5(today.encode()).hexdigest()[:8]

async def call_openai_api(prompt: str, max_tokens: int = 200, temperature: float = 0.8) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative, uplifting AI assistant that creates personalized, engaging content. Always be positive, inspiring, and add a touch of magic."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            presence_penalty=0.3,
            frequency_penalty=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return "Something magical went wrong, but you are still amazing! ✨"

# -------------------- API Endpoints --------------------

@app.post("/api/daily-affirmation", response_model=AffirmationResponse)
async def get_daily_affirmation(req: AffirmationRequest):
    date_hash = get_date_hash()
    today = datetime.now().strftime("%Y-%m-%d")
    day_of_week = datetime.now().strftime("%A")
    current_hour = datetime.now().hour
    time_context = "morning" if current_hour < 12 else "afternoon" if current_hour < 17 else "evening"

    prompt = f"""
    Create a deeply inspiring daily affirmation for a {time_context} on {day_of_week}.
    Language: {req.language}
    Requirements:
    - 2-3 sentences
    - Uplifting, poetic, encouraging
    - End with hope for the day ahead
    Seed: {date_hash}
    """
    text = await call_openai_api(prompt, max_tokens=150, temperature=0.7)

    visuals = ["✨", "🌟", "🌅", "💫", "🔥", "🌈", "🦋", "🌸"]
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8"]

    return AffirmationResponse(
        affirmation=text,
        visual_element=visuals[int(date_hash[:2], 16) % len(visuals)],
        date=today,
        mood_color=colors[int(date_hash[2:4], 16) % len(colors)]
    )

# @app.post("/api/random-fun", response_model=RandomFunResponse)
# async def get_random_fun(req: RandomFunRequest):
#     fun_types = [
#         {"type": "joke", "emoji": "😄", "prompt": "Create a clever, family-friendly joke with a positive twist."},
#         {"type": "compliment", "emoji": "💝", "prompt": "Give a heartfelt compliment focusing on inner qualities."},
#         {"type": "riddle", "emoji": "🧩", "prompt": "Write a fun riddle with the answer and uplifting message."},
#         {"type": "art", "emoji": "🎨", "prompt": "Describe a vivid, imaginary abstract art piece in 2-3 sentences."}
#     ]
#     choice = random.choice(fun_types)
#     content = await call_openai_api(choice["prompt"], max_tokens=200, temperature=0.9)
#     return RandomFunResponse(type=choice["type"], content=content, emoji=choice["emoji"])

@app.post("/api/random-fun", response_model=RandomFunResponse)
async def get_random_fun(req: RandomFunRequest):
    lang_instruction = f"Write in {req.language} using simple, clear words."

    fun_types = [
        {
            "type": "joke",
            "emoji": "😄",
            "prompt": f"{lang_instruction} Give one short, funny, family-friendly joke that anyone can understand. Keep it under 20 words."
        },
        {
            "type": "compliment",
            "emoji": "💝",
            "prompt": f"{lang_instruction} Give one short, warm compliment about someone's character or kindness. Under 20 words."
        },
        # {
        #     "type": "riddle",
        #     "emoji": "🧩",
        #     "prompt": f"{lang_instruction} Give one short riddle with a clear answer. After the answer, add a 1-sentence uplifting note."
        # },
        {
            "type": "art",
            "emoji": "🎨",
            "prompt": f"{lang_instruction} Describe one small imaginary art scene in 1–2 short sentences that is easy to picture."
        }
    ]

    choice = random.choice(fun_types)
    content = await call_openai_api(choice["prompt"], max_tokens=80, temperature=0.8)

    return RandomFunResponse(
        type=choice["type"],
        content=content,
        emoji=choice["emoji"]
    )


@app.post("/api/riddle")
async def get_riddle(req: RandomFunRequest):
    lang_instruction = f"Write in {req.language} using simple, clear words."

    prompt = f"""{lang_instruction}
    Give one short, fun riddle for 5 to 20 age kids. 
    Output format:
    QUESTION: [riddle text]
    ANSWER: [answer text]
    Keep both under 20 words.
    """

    content = await call_openai_api(prompt, max_tokens=60, temperature=0.7)

    # Try to split into question/answer
    question, answer = content, ""
    for line in content.split("\n"):
        if line.upper().startswith("QUESTION:"):
            question = line.split(":", 1)[1].strip()
        elif line.upper().startswith("ANSWER:"):
            answer = line.split(":", 1)[1].strip()

    return {
        "question": question,
        "answer": answer
    }

@app.post("/api/ascii-challenge")
async def get_ascii_challenge(req: RandomFunRequest):
    lang_instruction = f"The answer must be in {req.language}."

    prompt = f"""{lang_instruction}

Create a simple ASCII art puzzle for kids and young adults (ages 5–22).

Rules:
- Draw using only keyboard characters (|, _, /, \\, (, ), *, etc.).
- Make it 3–6 lines tall and easy to recognize.
- The ASCII art should represent an animal, object, or simple scene.
- Keep it fun and not too detailed.
- After the ASCII art, write the correct answer in {req.language}.

Output format exactly:
ASCII:
[line1]
[line2]
[line3]
...
ANSWER: [short answer in {req.language}]

Example:
ASCII:
 |\_/|
 ( o.o )
 > ^ <
ANSWER: Cat
"""

    content = await call_openai_api(prompt, max_tokens=150, temperature=0.6)

    # Parse ASCII and answer
    ascii_art = []
    answer = ""
    capture_ascii = False
    for line in content.split("\n"):
        if line.strip().upper().startswith("ASCII:"):
            capture_ascii = True
            continue
        if line.strip().upper().startswith("ANSWER:"):
            capture_ascii = False
            answer = line.split(":", 1)[1].strip()
            continue
        if capture_ascii:
            ascii_art.append(line)

    return {
        "ascii_art": "\n".join(ascii_art),
        "answer": answer
    }




@app.post("/api/personality-insight", response_model=PersonalityResponse)
async def get_personality_insight(req: PersonalityRequest):
    if not req.input.strip():
        raise HTTPException(status_code=400, detail="Input cannot be empty")

    prompt = f"""
    Based on this: "{req.input}"
    Give:
    - 3-4 sentence personality insight
    - A creative personality type name
    - 3-4 key traits
    Language: {req.language}
    Format:
    INSIGHT: ...
    TYPE: ...
    TRAITS: ...
    """
    text = await call_openai_api(prompt, max_tokens=300, temperature=0.7)

    insight, ptype, traits = text, "The Unique Soul", ["Creative", "Thoughtful", "Inspiring"]
    for line in text.split("\n"):
        if line.startswith("INSIGHT:"): insight = line.replace("INSIGHT:", "").strip()
        elif line.startswith("TYPE:"): ptype = line.replace("TYPE:", "").strip()
        elif line.startswith("TRAITS:"):
            traits = [t.strip() for t in line.replace("TRAITS:", "").split(",") if t.strip()]

    confidence = min(0.95, 0.6 + (len(req.input.split()) * 0.05))
    return PersonalityResponse(
        insight=insight,
        traits=traits[:4],
        personality_type=ptype,
        share_text=f"I just discovered I'm {ptype}! 🌟 What's your AI personality type?",
        confidence_score=confidence
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
