import os
import io
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()

# Configure Gemini 1.5 Flash [cite: 314]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the Agent's Role (System Instruction) [cite: 313]
SYSTEM_PROMPT = """
You are the PadiGuard AI Agent, an expert in Malaysian Agrotech and Food Security. 
Your task is to analyze images of paddy crops (Padi).
First, verify if the image actually contains a crop or leaf. If the image is NOT a crop (e.g., a person, car, animal, random object), set 'is_crop_image' to false, keep the disease name as "Not a Crop", severity as "N/A", confidence score as 0, and provide an empty list for the action plan.
If it IS a crop:
1. Set 'is_crop_image' to true.
2. Identify the disease or pest.
3. Provide a 'Severity Level' (Low, Medium, High).
4. Create a 3-step 'Autonomous Action Plan' for the farmer.
5. Align suggestions with Malaysian agricultural standards and SDGs[cite: 177, 251].
Respond strictly in English[cite: 361].
"""

class PadiAnalysis(BaseModel):
    is_crop_image: bool
    disease_name: str
    severity: str
    confidence_score: float
    action_plan: list[str]
    malaysian_standard_reference: str

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=SYSTEM_PROMPT,
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": PadiAnalysis,
    }
)

from fastapi.middleware.cors import CORSMiddleware

class AnalyzeRequest(BaseModel):
    image_base64: str
    prompt: str = "Analyze this Padi leaf image and fill the JSON schema."

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to PadiGuard AI API. Go to /docs for API documentation."}

@app.post("/analyze")
async def analyze_crop(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read and prepare image
        request_object_content = await file.read()
        img = Image.open(io.BytesIO(request_object_content))
        
        # Call Gemini [cite: 312, 314]
        response = model.generate_content([
            "Analyze this crop image and fill the JSON schema.",
            img
        ])
        
        structured_data = json.loads(response.text)
        
        return {
            "track": "Padi & Plates (Agrotech)",
            "data": structured_data,
            "status": "Success"
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

@app.post("/analyze_base64")
async def analyze_base64_image(request: AnalyzeRequest):
    try:
        # Handle the base64 prefix if included (e.g. data:image/png;base64,...)
        if "," in request.image_base64:
            base64_data = request.image_base64.split(",")[1]
        else:
            base64_data = request.image_base64
            
        image_bytes = base64.b64decode(base64_data)
        img = Image.open(io.BytesIO(image_bytes))
        
        response = model.generate_content([
            request.prompt,
            img
        ])
        
        structured_data = json.loads(response.text)
        
        return {
            "track": "Padi & Plates (Agrotech)",
            "data": structured_data,
            "status": "Success"
        }
    except Exception as e:
        return {"status": "Error", "message": "JSON Parsing failed or AI error: " + str(e)}