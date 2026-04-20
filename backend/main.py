import os
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Setup Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-3.0-flash-preview') # Flash is best for speed 

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "PadiGuard AI is Online", "track": "Agrotech & Food Security"}

@app.post("/analyze")
async def analyze_crop(file: UploadFile = File(...)):
    # Logic for image processing will go here in Phase 2
    return {"message": "Image received. Ready for Phase 2 logic."}