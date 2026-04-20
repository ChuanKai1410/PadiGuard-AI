# PadiGuard AI - Project 2030 MyAI Future Hackathon
**Track:** Track 1: Padi & Plates (Agrotech & Food Security)

## AI Disclosure
[cite_start]This project utilizes **Google Gemini 1.5 Flash** for crop disease identification and **Google AI Studio** for prompt engineering[cite: 90, 314].

## Tech Stack
- **AI:** Gemini API
- [cite_start]**Backend:** FastAPI (Python) [cite: 113, 114]
- [cite_start]**Deployment:** Google Cloud Run [cite: 87, 110]

## How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Add your `GEMINI_API_KEY` to a `.env` file.
3. Run: `uvicorn main:app --reload`