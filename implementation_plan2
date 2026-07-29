# MediAssist.AI — Full Platform Transformation Plan

Transform **NeuroDetect AI** (brain CT only) into **MediAssist.AI** — a universal AI medical intelligence platform that scans *every type of medical report*, identifies diseases, explains them in plain language, and provides actionable recovery guidance.

---

## Scope of Changes

### 🔴 What gets replaced / rebranded
- All "NeuroDetect AI" branding → **MediAssist.AI**
- All "NeuroDetect", "ND-" patient IDs → **MA-** patient IDs
- Brain CT–only UI messaging → universal multi-report language
- Existing basic guidance engine → full 8-module guidance system

---

## Phase 1 — Branding & Identity

### [MODIFY] All HTML Templates
Replace every instance of "NeuroDetect AI", "NeuroDetect", "ND-" with "MediAssist.AI" or "MA-" across:
- [index.html](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/templates/segmentation/index.html) — Landing page hero text, title, meta description, taglines
- [app.html](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/templates/segmentation/app.html) — Scanner page header, chatbot name, upload zone description
- [dashboard.html](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/templates/segmentation/dashboard.html) — All heading references
- [base.html](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/templates/segmentation/base.html) — Navbar brand, page title
- All other templates (about, login, register, registry, settings, profile, terms, contact)

### [MODIFY] [models.py](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/models.py)
- Patient ID prefix: `ND-{year}-{num}` → `MA-{year}-{num}`

---

## Phase 2 — Extended Report Type Support (Ingestion Engine)

### [MODIFY] [ingestion.py](file:///e:/going%20on%20works/MediAssist.AI/webapp/core_ml/ingestion.py)
Expand the `route_file()` modality router to support:

| Input Format | Detected Modality | Analyzer |
|---|---|---|
| `.dcm` DICOM (CT/MR tags) | `CT` / `MRI` | Brain & body CT/MRI |
| `.dcm` DICOM (CR/DX tags) | `CXR` | Chest X-ray |
| `.dcm` DICOM (ECG tags) | `ECG` | Heart rhythm |
| `.pdf` lab report | `BLOOD_TEST` | OCR + rule engine |
| `.jpg/.png` ECG keywords | `ECG` | ECG analyzer |
| `.jpg/.png` chest keywords | `CXR` | Chest X-ray |
| `.jpg/.png` skin keywords | `DERMATO` | Skin lesion analyzer |
| `.jpg/.png` eye/retina keywords | `RETINAL` | Retinal scan |
| `.jpg/.png` bone/xray | `BONE_XRAY` | Bone/fracture analyzer |
| `.jpg/.png` default | `CT` | General scan |

### [NEW] `core_ml/skin_analyzer.py`
Physics-based dermatology analyzer for uploaded skin images. Detects pigmentation anomalies, lesion boundaries, color asymmetry.

### [NEW] `core_ml/retinal_analyzer.py`
Retinal fundus image analyzer. Detects disc-to-cup ratio abnormalities, hemorrhages, vessel tortuosity.

### [NEW] `core_ml/bone_xray_analyzer.py`
Bone X-ray fracture and density analyzer. Estimates fracture probability, joint space narrowing.

---

## Phase 3 — Disease Knowledge Engine (Custom Local AI — Zero External APIs)

> [!IMPORTANT]
> All chatbot and guidance responses are generated **100% locally** inside Django. No Anthropic, OpenAI, or any other cloud API is used. This is a pure Python rule-based + semantic RAG engine.

### [NEW] `core_ml/disease_knowledge.py`
Central knowledge base for all supported medical conditions across modalities:

**Brain / Neurology (CT, MRI)**
- Ischemic Stroke, TIA, Subarachnoid Hemorrhage, Brain Tumor (Glioma, Meningioma), Hydrocephalus, Cerebral Edema

**Cardiology (ECG, CXR)**
- Atrial Fibrillation, Myocardial Infarction, Cardiomegaly, LVH, Tachycardia, Bradycardia, Heart Block

**Pulmonology (CXR)**
- Pneumonia (Bacterial, Viral), TB, COPD, Pleural Effusion, Pulmonary Edema, Pneumothorax

**Hematology / Lab (Blood Test)**
- Anemia, Thrombocytopenia, Hyperglycemia / Diabetes, Dyslipidemia, Kidney Disease (elevated creatinine/urea), Liver Disease (elevated ALT/AST), Thyroid disorders

**Dermatology (DERMATO)**
- Melanoma risk, Eczema, Psoriasis, Ringworm, Acne vulgaris

**Ophthalmology (RETINAL)**
- Diabetic Retinopathy, Glaucoma, Age-related Macular Degeneration

**Orthopedics (BONE_XRAY)**
- Fracture, Osteoporosis, Arthritis, Joint Space Narrowing

For **each** condition the engine stores:
1. **What it is** — Plain-language disease explanation
2. **How it occurred** — Causes, risk factors, pathophysiology in simple terms
3. **What happens if untreated** — Stage-by-stage consequences of no treatment
4. **Herbal & Dietary Recommendations** — Foods to eat, foods to avoid, herbal remedies (e.g. Ashwagandha, Brahmi, Turmeric, Neem, Moringa) with evidence citations
5. **Recovery & Exercise Plan** — Condition-specific safe exercise list, progression stages
6. **Clinical Telemetry** — Key parameters to monitor (BP, BPM, SpO2, HbA1c, etc.)
7. **Doctor Guide** — 5–8 precise questions to ask the specialist + specialist routing
8. **Risk Profiler** — Calculates 10-year risk scores (CV risk, stroke risk, diabetes risk, organ-specific)

---

## Phase 4 — Enhanced Guidance Generator

### [MODIFY] [guidance.py](file:///e:/going%20on%20works/MediAssist.AI/webapp/core_ml/guidance.py)
Remove all Anthropic API calls. Replace with the local `DiseaseKnowledgeEngine`:

```python
def generate_guidance(self, modality, findings_text):
    disease = self.knowledge.identify_condition(modality, findings_text)
    return {
        'disease_name': disease.name,
        'what_it_is': disease.explanation,
        'how_it_occurred': disease.causes,
        'if_untreated': disease.consequences,
        'diet': disease.diet,           # + herbal
        'exercise': disease.exercise,
        'telemetry': disease.telemetry,
        'questions': disease.doctor_questions,
        'routing': disease.specialist_routing,
        'risk': disease.risk_indicators
    }
```

---

## Phase 5 — Custom Local Chatbot Engine

### [MODIFY] [views.py](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/views.py) — `chat_api`
Remove Anthropic `client.messages.create(...)` call. Replace entirely with:

```python
from core_ml.mediassist_chatbot import MediAssistChatbot
bot = MediAssistChatbot()
assistant_response = bot.respond(user_msg_text, scan, history_objs, language)
```

### [NEW] `core_ml/mediassist_chatbot.py`
Fully offline, intent-routing medical chatbot with:
- **Intent detection** across 20+ medical query types (disease explanation, diet, herbal, exercise, telemetry, emergency, risk, doctor questions, etc.)
- **Scan-grounded response generation** using active scan findings, risk profile, guidance data
- **Emotion detection** (fear, panic, confusion → empathetic tone shift)
- **Emergency escalation protocol** (FAST stroke, cardiac arrest, BP crisis)
- **Multilingual output** (English, Hindi, regional dialects)

---

## Phase 6 — UI Overhaul (app.html)

### [MODIFY] [app.html](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/templates/segmentation/app.html)
Expand the results section from brain CT–specific to universal multi-report panels:

| Panel | Current | New |
|---|---|---|
| **Upload** | "Upload Brain NCCT" | "Upload Any Medical Report" (DICOM, X-Ray, ECG, Lab PDF, Skin, Retinal) |
| **Findings** | Lesion load % | Modality-adaptive: condition name + severity + confidence |
| **Disease Info** | — | **New card**: What It Is + How It Occurred + Untreated Consequences |
| **Diet** | Basic food list | Full diet plan + **Herbal Remedies** section |
| **Telemetry** | — | **New card**: Clinical parameters to monitor (BP, BPM, SpO2, etc.) |
| **Recovery** | Basic exercise | Staged recovery timeline with exercise plan |
| **Doctor Guide** | Question list | Questions + specialist name + urgency level |
| **Risk Profiler** | CV/Stroke/Diabetes % | All risk scores + visual risk meter |
| **Doctor Room** | Telehealth chat | Full Doctor Room with consultation notes |
| **Chatbot** | "MedAssist" | **MediAssist Bot** — fully local, offline |

### [MODIFY] [index.html](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/templates/segmentation/index.html)
Complete hero rewrite:
- Tagline: **"Scan Any Report. Understand Every Disease. Recover with Confidence."**
- Feature showcase: All 8 modules (Disease Info, Herbal Diet, Telemetry, Recovery, Doctor Guide, Risk Profiler, Doctor Room, AI Chat)
- Supported report types: CT, MRI, X-Ray, ECG, Lab PDF, Skin, Retinal, Bone X-Ray

---

## Phase 7 — Database Migration

### [MODIFY] [models.py](file:///e:/going%20on%20works/MediAssist.AI/webapp/segmentation/models.py)
Add fields to `PatientScan`:
```python
disease_name = models.CharField(max_length=200, blank=True)
disease_explanation = models.TextField(blank=True)
disease_causes = models.TextField(blank=True)
untreated_consequences = models.TextField(blank=True)
herbal_recommendations = models.JSONField(default=list)
telemetry_targets = models.JSONField(default=dict)
```

Add new migration and run `python manage.py makemigrations && migrate`.

---

## Phase 8 — README & Project Identity Update

### [MODIFY] [README.md](file:///e:/going%20on%20works/MediAssist.AI/README.md)
Complete rewrite to reflect MediAssist.AI branding, all supported modalities, and 8 module descriptions.

---

## Verification Plan

### Automated
- Upload Brain CT DICOM → verify disease name, herbal diet, risk scores
- Upload Chest X-ray JPG → verify CXR modality detected, pulmonology guidance
- Upload ECG image → verify ECG routing, BPM telemetry
- Upload Blood Test PDF → verify lab OCR parsing, hematology guidance
- Chat with bot in English and Hindi → verify offline responses, emotion detection

### Manual
- Run `python manage.py runserver`
- Visit `http://127.0.0.1:8000/` → confirm MediAssist.AI branding
- Visit `http://127.0.0.1:8000/app/` → upload all 4 report types, test all 8 panels
