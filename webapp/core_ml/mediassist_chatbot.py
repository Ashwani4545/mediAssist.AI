import os
import re
from core_ml.disease_knowledge import get_disease_knowledge_engine

class MediAssistChatbot:
    def __init__(self):
        self.disease_engine = get_disease_knowledge_engine()

    def respond(self, user_message: str, scan, history=None, language: str = "English") -> dict:
        """
        Generate a scan-grounded, empathetic, and medically accurate response 100% offline.
        
        Args:
            user_message: str — query text from patient
            scan: PatientScan model instance
            history: list of ChatMessage instances (optional)
            language: str — requested language (English, Hindi, etc.)
            
        Returns:
            dict containing:
                'message': str (response text)
                'emotion_detected': str or None ('anxious', 'fearful', 'panicked')
        """
        q = (user_message or "").lower().strip()
        modality = getattr(scan, 'modality', 'CT')
        findings_text = getattr(scan, 'notes', '') or ''
        confidence = getattr(scan, 'confidence', 0.0)
        detected = getattr(scan, 'detected', False)
        
        # 1. Emotion & Sentiment Analysis
        emotion_detected = None
        anxious_keywords = ['scared', 'afraid', 'worried', 'panic', 'dying', 'cancer', 'stroke right now', 'emergency', 'fear', 'terrified']
        if any(kw in q for kw in anxious_keywords):
            emotion_detected = 'anxious'
            
        # Retrieve Disease Knowledge profile for active scan
        condition = self.disease_engine.identify_condition(modality, findings_text)
        cond_data = condition.to_dict()

        # Retrieve Risk Profile & Guidance if attached
        cv_risk = "N/A"
        stroke_risk = "N/A"
        diabetes_risk = "N/A"
        try:
            if hasattr(scan, 'risk_profile') and scan.risk_profile:
                cv_risk = f"{scan.risk_profile.cv_risk_score}% ({scan.risk_profile.cv_risk_grade})"
                stroke_risk = f"{scan.risk_profile.stroke_risk_score}% ({scan.risk_profile.stroke_risk_grade})"
                diabetes_risk = f"{scan.risk_profile.diabetes_risk_score}% ({scan.risk_profile.diabetes_risk_grade})"
        except Exception:
            pass

        # 2. Emergency Safeguard Check
        if any(w in q for w in ['emergency', 'dying', 'chest pain', 'severe shortness of breath', 'facial drooping', 'slurred speech', 'arm weakness']):
            resp = self._format_emergency_response(modality, cond_data['name'])
            return {'message': self._apply_language(resp, language), 'emotion_detected': 'panicked'}

        # 3. Intent Classification & Response Formulation
        resp_paragraphs = []
        
        # Add empathetic prefix if anxiety detected
        if emotion_detected == 'anxious':
            resp_paragraphs.append("I can hear how concerning this feels, but please take a deep breath. I am here to help you understand your report step by step in simple terms.")

        # Intent 1: What is this disease / Explain scan
        if any(w in q for w in ['explain', 'what is', 'disease', 'condition', 'scan', 'findings', 'result', 'meaning', 'lesion', 'load', 'anomaly']):
            resp_paragraphs.append(f"Based on your **{modality}** analysis, your scan relates to **{cond_data['name']}**.")
            resp_paragraphs.append(f"**What it means:** {cond_data['explanation']}")
            if detected:
                resp_paragraphs.append(f"The automated model flagged a telemetry score of **{confidence:.1f}%** for this report.")

        # Intent 2: How did this happen / Root causes
        elif any(w in q for w in ['how', 'cause', 'happen', 'occurred', 'why', 'reason', 'develop']):
            resp_paragraphs.append(f"**How {cond_data['name']} occurs:**")
            resp_paragraphs.append(cond_data['causes'])

        # Intent 3: What if medicare is delayed / Untreated consequences
        elif any(w in q for w in ['untreated', 'delay', 'neglect', 'happen if', 'consequence', 'worse', 'danger', 'risk']):
            resp_paragraphs.append(f"**What happens if treatment or medical care is delayed for {cond_data['name']}:**")
            resp_paragraphs.append(cond_data['if_untreated'])
            resp_paragraphs.append("This is why timely consultation with a healthcare provider is essential.")

        # Intent 4: Herbal diet & remedies
        elif any(w in q for w in ['herb', 'herbal', 'ayurveda', 'natural', 'remedy', 'supplement', 'ashwagandha', 'arjuna', 'brahmi', 'turmeric']):
            resp_paragraphs.append(f"**Evidence-Backed Herbal & Natural Recommendations for {cond_data['name']}:**")
            for h in cond_data['diet']['herbal_remedies']:
                resp_paragraphs.append(f"• **{h['name']}**: {h['benefit']} (Dosage: *{h['dosage']}*)")
            resp_paragraphs.append("*Note: Always inform your doctor before adding herbal supplements alongside prescribed medications.*")

        # Intent 5: Dietary advice (Foods to eat & avoid)
        elif any(w in q for w in ['diet', 'food', 'eat', 'avoid', 'nutrition', 'meal', 'drink']):
            resp_paragraphs.append(f"**Dietary Plan for {cond_data['name']}:**")
            resp_paragraphs.append("**Recommended Foods to Eat:** " + ", ".join(cond_data['diet']['recommended']))
            resp_paragraphs.append("**Foods to Strictly Avoid:** " + ", ".join(cond_data['diet']['avoid']))

        # Intent 6: Exercise & Physical Recovery
        elif any(w in q for w in ['exercise', 'workout', 'activity', 'walk', 'gym', 'sport', 'physical', 'recovery']):
            resp_paragraphs.append(f"**Recovery & Physical Activity Guidelines:**")
            resp_paragraphs.append("**Allowed / Recommended Activities:** " + ", ".join(cond_data['exercise']['allowed']))
            resp_paragraphs.append("**Activities & Strain to Avoid:** " + ", ".join(cond_data['exercise']['restrictions']))

        # Intent 7: Clinical Telemetry & Target metrics
        elif any(w in q for w in ['telemetry', 'target', 'metric', 'blood pressure', 'bp', 'spo2', 'oxygen', 'heart rate', 'bpm', 'glucose']):
            resp_paragraphs.append(f"**Key Clinical Telemetry Target Parameters:**")
            for k, v in cond_data['telemetry'].items():
                resp_paragraphs.append(f"• **{k}**: Target {v}")
            if cv_risk != "N/A":
                resp_paragraphs.append(f"**Your 10-Year Calculated Risk Scores:** Cardiovascular: {cv_risk} | Stroke: {stroke_risk} | Diabetes: {diabetes_risk}")

        # Intent 8: Doctor guide / Questions to ask specialist
        elif any(w in q for w in ['doctor', 'specialist', 'ask', 'question', 'consult', 'referral', 'appointment']):
            resp_paragraphs.append(f"**Specialist Referral:** You should consult a **{cond_data['routing']['specialist']}** (Urgency Level: *{cond_data['routing']['urgency']}*).")
            resp_paragraphs.append("**Key Questions to Ask Your Specialist:**")
            for i, question in enumerate(cond_data['questions'], 1):
                resp_paragraphs.append(f"{i}. {question}")

        # Fallback General Conversational Response
        else:
            resp_paragraphs.append(f"Regarding your **{modality}** report for **{cond_data['name']}**:")
            resp_paragraphs.append(f"• **Condition Summary:** {cond_data['explanation']}")
            resp_paragraphs.append(f"• **Recommended Diet:** " + ", ".join(cond_data['diet']['recommended'][:2]))
            resp_paragraphs.append(f"• **Herbal Support:** {cond_data['diet']['herbal_remedies'][0]['name']} ({cond_data['diet']['herbal_remedies'][0]['benefit']})")
            resp_paragraphs.append(f"• **Specialist:** {cond_data['routing']['specialist']}")
            resp_paragraphs.append("Feel free to ask me specifically about dietary advice, herbal remedies, exercise guidelines, or questions to ask your doctor!")

        # Always add medical safety disclaimer footer
        resp_paragraphs.append("\n*Disclaimer: MediAssist.AI is an academic research platform. Always review report findings with a qualified medical specialist for clinical diagnosis.*")

        full_response = "\n\n".join(resp_paragraphs)
        translated_response = self._apply_language(full_response, language)
        
        return {
            'message': translated_response,
            'emotion_detected': emotion_detected
        }

    def _format_emergency_response(self, modality: str, condition_name: str) -> str:
        return (
            "🚨 **IMMEDIATE EMERGENCY ALERT** 🚨\n\n"
            "If you or the patient are experiencing **acute emergency symptoms** — such as severe chest pain, radiative arm numbness, "
            "sudden facial drooping, weakness on one side of the body, or severe difficulty breathing — **please call emergency services (112, 102/108 in India, or 911) IMMEDIATELY**.\n\n"
            f"Your scan relates to **{condition_name}**. Acute onset symptoms cannot be safely evaluated by an AI tool and require immediate emergency room (ER) care.\n\n"
            "Do not wait. Seek immediate medical attention."
        )

    def _apply_language(self, text: str, language: str) -> str:
        """Simple localized greeting/footer wrapper for requested languages."""
        lang = (language or "English").lower()
        if 'hindi' in lang:
            prefix = "🙏 **MediAssist.AI (हिंदी सहायता)**:\n\n"
            return prefix + text
        elif 'spanish' in lang:
            prefix = "🇪🇸 **MediAssist.AI (Asistente Médico)**:\n\n"
            return prefix + text
        return text


_chatbot = None

def get_mediassist_chatbot() -> MediAssistChatbot:
    global _chatbot
    if _chatbot is None:
        _chatbot = MediAssistChatbot()
    return _chatbot
