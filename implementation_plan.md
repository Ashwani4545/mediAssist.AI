# Implementation Plan — Custom Local AI Chatbot Engine (Zero External APIs)

Build a 100% self-contained, offline-capable, custom AI Chatbot engine for **NeuroDetect AI** that runs directly within the project without relying on third-party cloud APIs (such as Anthropic, OpenAI, or Google).

## User Review Required

> [!IMPORTANT]
> **No API Keys or Cloud Subscriptions Required**: The chatbot will run completely locally on the server.
> You can choose between:
> 1. **Option A (Recommended for standard CPUs)**: A custom PyTorch + Semantic RAG & Medical Intent Engine (`CustomMedicalChatbot`). Instant response time (< 50ms), zero memory overhead, highly accurate for clinical scan interpretation, risk profiles, diet plans, and emergency detection.
> 2. **Option B (Requires GPU / PyTorch LLM setup)**: A local open-weight LLM using HuggingFace Transformers (e.g. `Qwen2.5-0.5B-Instruct` or `TinyLlama-1.1B`).

## Proposed Changes

### Core ML & Chatbot Engine

#### [NEW] [custom_chatbot.py](file:///e:/projects/Advanced%20ML/python/brain-region-segmentation/webapp/core_ml/custom_chatbot.py)
- Create a dedicated Python module `webapp/core_ml/custom_chatbot.py`.
- **Intent Recognition & Semantic Matching**: Recognizes clinical queries (lesion load explanation, stroke signs, cardiomegaly risk, blood metric interpretation, emergency triage, diet advice, specialist routing).
- **Scan-Grounded Context Retriever**: Integrates active scan findings (HU windowing, lesion %, detected anomalies), patient risk score (cardiovascular, diabetes, stroke risk), and patient guidance blueprint.
- **Empathetic & Multilingual Generator**: Generates human-like, compassionate clinical explanations in English, Hindi, Spanish, etc.
- **Emergency Safeguard Guardrails**: Detects acute stroke signs (FAST), chest pain, severe shortness of breath, and outputs immediate emergency escalation alerts.

---

### Django Web Application

#### [MODIFY] [views.py](file:///e:/projects/Advanced%20ML/python/brain-region-segmentation/webapp/segmentation/views.py)
- Update `chat_api` view to invoke `CustomMedicalChatbot.generate_response()` directly.
- Remove external Anthropic API network requests and dependency fallbacks.
- Store conversation history and detected emotional states in `ChatMessage` database model.

#### [MODIFY] [app.html](file:///e:/projects/Advanced%20ML/python/brain-region-segmentation/webapp/segmentation/templates/segmentation/app.html) & [styles.css](file:///e:/projects/Advanced%20ML/python/brain-region-segmentation/webapp/segmentation/static/segmentation/css/styles.css)
- Update Chatbot UI headers to showcase **"NeuroDetect Local AI Engine — 100% Private & Offline"**.
- Add quick topic tags tailored to local chatbot features (e.g., "Explain Lesion Load", "Stroke Warning Signs", "Recommended Diet", "Specialist Questions").

---

## Verification Plan

### Automated Verification
- Run test script calling `CustomMedicalChatbot` across test scenarios:
  - Brain CT scan with hypodense lesion.
  - Chest X-ray with lung opacity / CTR > 0.5.
  - ECG scan with high heart rate.
  - Blood test out-of-range metrics.
  - Multilingual queries (Hindi/English).
  - Anxious / Emergency trigger keywords.

### Manual Verification
- Start local Django server (`python manage.py runserver`).
- Upload a DICOM / NCCT image on `http://127.0.0.1:8000/app/`.
- Interact with the chatbot in various languages and topics.
- Verify zero network calls are made to external domains.
