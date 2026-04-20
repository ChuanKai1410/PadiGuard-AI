# PadiGuard AI - Project 2030 MyAI Future Hackathon
**Track:** Track 1: Padi & Plates (Agrotech & Food Security)

## AI Disclosure
[cite_start]This project utilizes **Google Gemini 3 Flash** for crop disease identification and **Google AI Studio** for prompt engineering[cite: 90, 314].

## Tech Stack
- **AI:** Gemini API
- [cite_start]**Backend:** FastAPI (Python) [cite: 113, 114]
- [cite_start]**Deployment:** Google Cloud Run [cite: 87, 110]

## How to Run Locally
1. Install dependencies: `cd backend` and `pip install -r requirements.txt`
2. Add your `GEMINI_API_KEY` to a `.env` file in the `backend` directory.
3. Start the Backend API: `uvicorn main:app --reload`. The backend will run on **http://localhost:8000** (Documentation available at **http://localhost:8000/docs**).
4. Start the Frontend UI: Open a new terminal in the `frontend` directory and run `python -m http.server 3000`. The frontend will be accessible at **http://localhost:3000**.

## Technical Execution
- **Low-Latency Diagnostics:** We implemented **Gemini 3 Flash** as the core model. Its lightweight and fast inference makes it perfect for near-instant analysis of crop images, essential for farmers out in the field.
- **Agentic AI Workflows:** Prompts are structured to enforce an Agentic AI workflow—the model doesn't just describe what it sees, but is engineered to act as an autonomous Agrotech expert. It explicitly formats its output to give structured disease identification, severity levels, and an actionable 3-step remedy plan compliant with local Malaysian safety standards.