# 🌾 PadiGuard AI
> **Project 2030 MyAI Future Hackathon** | **Track 1: Padi & Plates (Agrotech & Food Security)**

PadiGuard AI is an intelligent, low-latency diagnostic tool designed for Malaysian farmers. By leveraging cutting-edge Agentic AI, it provides near-instant crop disease identification and localized, actionable remedy plans to safeguard crop yields and promote food security.

---

## 🤖 AI Disclosure
This project natively integrates **Google Gemini 3 Flash** for rapid computer vision and diagnostic reasoning. Model behavior is sculpted using **Google AI Studio** for precise prompt engineering and structured agentic outputs.

## 🛠 Tech Stack
- **AI Engine:** Google Gemini 3 Flash API
- **Backend:** FastAPI (Python), Uvicorn, Pydantic, OpenCV, NumPy
- **Frontend:** HTML5, Tailwind CSS, Vanilla JS, marked.js
- **Deployment:** Container Ready (Docker)

---

## 🚀 How to Run Locally

### 1️⃣ Backend Setup
1. Open a terminal and navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the `backend` directory and add your API key:
   ```env
   GEMINI_API_KEY="your_google_gemini_api_key_here"
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0
   ```
   > **Note:** The backend will run on **http://localhost:8000**. Built-in API documentation is available at **http://localhost:8000/docs**.

### 2️⃣ Frontend Setup
1. Open a **new, separate terminal window** and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Start the local HTTP server:
   ```bash
   python -m http.server 3000
   ```
3. Open your browser and navigate to **http://localhost:3000** to use the PadiGuard AI Dashboard.

---

## 🧠 Technical Execution & Key Features

### ✨ Computer Vision Preprocessing (OpenCV)
To minimize API latency and maximize diagnostic accuracy, raw images undergo extreme optimization before hitting the cloud:
1. **Smart Resizing:** Large mobile photos are instantly scaled down to a maximum side of 1024px while retaining aspect ratio, massively reducing payload transit time and token costs.
2. **Denoising:** `fastNlMeansDenoisingColored` removes graininess common in low-light field imagery.
3. **CLAHE Contrast Mapping:** Exposes subtle lesion boundaries and leaf discoloration algorithms might otherwise miss.
4. **Sharpening:** A 3x3 convolution kernel extracts harsh edges of pest damages and necrotic spots.

### 🌐 Instant Multi-Language Support (i18n)
PadiGuard boasts full interface internationalization for **English, Bahasa Malaysia, and Mandarin Chinese**. Upon selecting a language, the UI changes instantly, and the dynamic backend prompt inherits the language context—commanding the Gemini agent to autonomously generate its complex diagnostic response entirely in the farmer's native language. 

### 🛡️ Rigid Agentic Workflows & Schema Enforcement
Our API interacts with Gemini not as a chatbot, but as an **Autonomous Agrotech Expert**. 
- Using **Pydantic**, the Gemini 3 Flash model is strictly constrained (`response_mime_type="application/json"`) to map its output to our exact `PadiAnalysis` schema schema—effectively eliminating arbitrary hallucinations.
- Diagnoses natively include strict **3-step autonomous action plans** aligned with **Malaysian agricultural safety standards and SDGs**.

### 🛑 Intelligent Error Handling & Guardrails
- **Non-Crop & Wide Shot Rejection:** The model is armed with critical rules to detect non-plant imagery or sweeping wide shots of entire fields. It politely rejects these images and instructs the farmer to take a close-up photo of the single affected leaf.
- **Guided Farmer Inputs:** Instead of vague text boxes, farmers input context through specific, localized dropdown menus (Symptom, Duration), guiding the model towards an accurate conclusion.
- **Frontend AbortControllers:** The UI enforces a strict 30-second client-side timeout. If field internet is too slow, it gracefully aborts and prompts the user to retake the photo rather than hanging indefinitely.