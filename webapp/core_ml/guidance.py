import os
import json
from django.conf import settings
from core_ml.disease_knowledge import get_disease_knowledge_engine

class GuidanceGenerator:
    def __init__(self):
        self.disease_engine = get_disease_knowledge_engine()

    def generate_guidance(self, modality: str, findings_text: str) -> dict:
        """
        Formulate a comprehensive, personalized guidance package 100% offline.
        Uses DiseaseKnowledgeEngine for instant medical reasoning across all 7 modalities.
        """
        condition = self.disease_engine.identify_condition(modality, findings_text)
        data = condition.to_dict()

        # Format output into structured JSON matching all UI panels
        return {
            'disease_name': data['name'],
            'category': data['category'],
            'what_it_is': data['explanation'],
            'how_it_occurred': data['causes'],
            'if_untreated': data['untreated_consequences'],
            'diet': {
                'recommended': data['diet']['recommended'],
                'avoid': data['diet']['avoid'],
                'herbal_remedies': data['diet']['herbal_remedies'],
                'reasoning': f"Dietary modifications for {data['name']} designed to lower inflammation, manage organ stress, and promote cellular repair."
            },
            'exercise': {
                'allowed': data['exercise']['allowed'],
                'restrictions': data['exercise']['restrictions'],
                'guidelines': f"Staged physical activity for {data['name']}. Always consult your specialist before progressing exercise intensity."
            },
            'lifestyle': {
                'tips': [
                    "Maintain strict sleep hygiene (7-8 hours restful sleep nightly)",
                    "Track daily telemetry metrics (BP, SpO2, heart rate) every morning",
                    "Avoid alcohol, tobacco smoke, and severe stress triggers"
                ],
                'red_flags': [
                    "Sudden acute chest pain, radiative arm numbness, or severe shortness of breath",
                    "Sudden facial drooping, arm weakness, or slurred speech (FAST stroke protocol)",
                    "High fever (> 101°F) or persistent oxygen saturation drop below 92%"
                ],
                'notes': f"Comprehensive recovery and self-monitoring guidelines for {data['name']}."
            },
            'telemetry': data['telemetry'],
            'routing': data['routing'],
            'questions': data['questions']
        }

_generator = None

def get_guidance_generator() -> GuidanceGenerator:
    global _generator
    if _generator is None:
        _generator = GuidanceGenerator()
    return _generator
