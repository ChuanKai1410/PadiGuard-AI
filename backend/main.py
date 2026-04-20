import os
import io
import base64
from fastapi import FastAPI
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import cv2
import numpy as np

load_dotenv()

# Configure Gemini 1.5 Flash [cite: 314]
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class PadiAnalysis(BaseModel):
    is_crop_image: bool
    disease_name: str
    severity: str
    confidence_score: float
    action_plan: list[str]
    malaysian_standard_reference: str

# Define the Agent's Role (System Instruction) [cite: 313]
SYSTEM_PROMPT = """
You are the PadiGuard AI Agent, an expert in Malaysian Agrotech and Food Security. 
Your task is to analyze images of paddy crops (Padi).
1. Identify the disease or pest.
2. Provide a 'Severity Level' (Low, Medium, High).
3. Create a 3-step 'Autonomous Action Plan' for the farmer.
4. Align suggestions with Malaysian agricultural standards and SDGs[cite: 177, 251].
Respond entirely and strictly in the language requested by the user prompt.

CRITICAL RULE: If the uploaded image does NOT contain a plant, leaf, or crop, set `is_crop_image` to false, set `disease_name` to "Non-Crop Image", set `severity` to "N/A", provide a polite rejection message in the first item of `action_plan` asking for a valid crop image, and set `confidence_score` to 1.0. If the image shows an entire field or a whole plant instead of a specific leaf, immediately return a JSON response asking the user to provide a close-up photo of the affected area for a precise diagnosis.
"""

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
    prompt: str = "Act as a Malaysian Agrotech expert. Identify the disease in this Padi leaf and provide a 3-step action plan using local Malaysian safety standards."

def enhance_image(image_bytes):
    # Convert bytes to OpenCV format
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 0. Smart Resizing (maintain aspect ratio)
    height, width = img.shape[:2]
    max_side = 1024
    if max(height, width) > max_side:
        scaling_factor = max_side / float(max(height, width))
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    # 1. Denoising (Removes graininess)
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    # 2. CLAHE (Better contrast for disease symptoms)
    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # 3. Sharpening Kernel
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced_img, -1, kernel)

    # Convert back to PIL for Gemini
    success, encoded_img = cv2.imencode('.jpg', sharpened)
    return Image.open(io.BytesIO(encoded_img.tobytes()))

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


@app.post("/analyze_base64")
async def analyze_base64_image(request: AnalyzeRequest):
    try:
        # Handle the base64 prefix if included (e.g. data:image/png;base64,...)
        if "," in request.image_base64:
            base64_data = request.image_base64.split(",")[1]
        else:
            base64_data = request.image_base64
            
        image_bytes = base64.b64decode(base64_data)
        
        # Enhance the blurry image first
        ready_image = enhance_image(image_bytes)
        
        response = model.generate_content([
            request.prompt + " Format your output strictly adhering to the JSON schema.",
            ready_image
        ])
        
        structured_data = json.loads(response.text)
        
        return {
            "status": "Success",
            "data": structured_data
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}