# 🌾 PadiGuard AI
> **Project 2030 MyAI Future Hackathon** | **Track 1: Padi & Plates (Agrotech & Food Security)**

PadiGuard AI is an intelligent, low-latency diagnostic tool designed for Malaysian farmers. By leveraging cutting-edge Agentic AI, it provides near-instant crop disease identification and localized, actionable remedy plans to safeguard crop yields and promote food security.

---

## 🤖 AI Disclosure
This project natively integrates **Google Gemini 3 Flash** for rapid computer vision and diagnostic reasoning. Model behavior is sculpted using **Google AI Studio** for precise prompt engineering and structured agentic outputs.

## 🛠 Tech Stack
- **AI Engine:** Google Gemini 3 Flash API
- **Backend:** FastAPI (Python), Uvicorn, Pydantic
- **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JS, marked.js
- **Deployment:** Google Cloud Run (Containerized via Docker)

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
   uvicorn main:app --reload
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

## 🧠 Technical Execution

### Fast, Low-Latency Diagnostics
We implemented **Gemini 3 Flash** as our core reasoning engine. Its significantly reduced latency makes it perfect for near-instant analysis of crop images—a critical requirement for farmers operating in the field where quick decisions save yields.

### Agentic AI Workflows
Our API interacts with Gemini not just as a chatbot, but as an **Autonomous Agrotech Expert**. Prompts are hyper-structured to enforce an Agentic AI workflow:
- The model must identify the disease.
- Evaluate and classify the severity level.
- Generate a strict **3-step actionable remedy plan** that complies with local **Malaysian agricultural and safety standards**.

### Pydantic Schema Enforcement
We utilize **Pydantic for Schema Enforcement** combined with Gemini's JSON extraction capabilities (`response_mime_type="application/json"`) to ensure high-fidelity data transfer between Gemini and our backend. This guarantees professional code quality, deterministic data shapes, and zero parsing errors when sending insights to the dashboard.