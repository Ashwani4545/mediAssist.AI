import os
import re

class DiseaseCondition:
    def __init__(
        self,
        name: str,
        category: str,
        explanation: str,
        causes: str,
        untreated_consequences: str,
        diet_recommended: list,
        diet_avoid: list,
        herbal_remedies: list,
        exercise_allowed: list,
        exercise_restrictions: list,
        telemetry_targets: dict,
        specialist: str,
        urgency: str,
        doctor_questions: list
    ):
        self.name = name
        self.category = category
        self.explanation = explanation
        self.causes = causes
        self.untreated_consequences = untreated_consequences
        self.diet_recommended = diet_recommended
        self.diet_avoid = diet_avoid
        self.herbal_remedies = herbal_remedies
        self.exercise_allowed = exercise_allowed
        self.exercise_restrictions = exercise_restrictions
        self.telemetry_targets = telemetry_targets
        self.specialist = specialist
        self.urgency = urgency
        self.doctor_questions = doctor_questions

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'category': self.category,
            'explanation': self.explanation,
            'causes': self.causes,
            'untreated_consequences': self.untreated_consequences,
            'diet': {
                'recommended': self.diet_recommended,
                'avoid': self.diet_avoid,
                'herbal_remedies': self.herbal_remedies
            },
            'exercise': {
                'allowed': self.exercise_allowed,
                'restrictions': self.exercise_restrictions
            },
            'telemetry': self.telemetry_targets,
            'routing': {
                'specialist': self.specialist,
                'urgency': self.urgency
            },
            'questions': self.doctor_questions
        }


class DiseaseKnowledgeEngine:
    def __init__(self):
        self.database = self._build_knowledge_base()

    def _build_knowledge_base(self) -> dict:
        kb = {}

        # ── 1. BRAIN CT / MRI CONDITIONS ───────────────────────────────────────
        kb['CT_ISCHEMIC_STROKE'] = DiseaseCondition(
            name="Ischemic Stroke & Cytotoxic Edema",
            category="Neurology",
            explanation="An ischemic stroke occurs when a blood clot obstructs blood supply to a specific region of brain tissue. Hypodensity on CT scans represents fluid swelling (cytotoxic edema) as oxygen-starved brain cells lose electrical membrane stability.",
            causes="Most commonly caused by arterial thrombosis, atherosclerosis, atrial fibrillation emboli, or uncontrolled hypertension causing microvascular blockage.",
            untreated_consequences="If untreated or unmanaged, cytotoxic edema can progress to mass effect, irreversible neuronal cell death, permanent neurological deficits (paralysis, loss of speech), or secondary hemorrhagic transformation.",
            diet_recommended=["Omega-3 rich walnuts and flaxseeds", "Leafy green vegetables (spinach, kale)", "Berries high in anthocyanins", "Garlic and olive oil"],
            diet_avoid=["Excessive dietary sodium (> 1,500 mg/day)", "Trans fats and deep-fried foods", "Refined sugars and ultra-processed snacks", "Alcohol"],
            herbal_remedies=[
                {"name": "Ashwagandha (Withania somnifera)", "benefit": "Neuroprotective antioxidant that reduces ischemic oxidative stress", "dosage": "300-500 mg twice daily after meals"},
                {"name": "Brahmi (Bacopa monnieri)", "benefit": "Enhances microvascular cerebral circulation and cognitive recovery", "dosage": "250-500 mg daily"},
                {"name": "Turmeric / Curcumin", "benefit": "Potent anti-inflammatory agent inhibiting post-stroke neuroinflammation", "dosage": "500 mg with black pepper extract"}
            ],
            exercise_allowed=["Supervised physical therapy gait practice", "Gentle seated range-of-motion stretching", "Light stationary cycling under supervision"],
            exercise_restrictions=["Heavy weightlifting or Valsalva strain", "High-impact cardio or running", "Strenuous neck hyperextension"],
            telemetry_targets={"Blood Pressure": "< 130/80 mmHg", "SpO2": "> 95%", "Fasting Blood Glucose": "< 100 mg/dL", "NIHSS Score": "Monitor daily"},
            specialist="Neurologist / Stroke Specialist",
            urgency="High / Immediate Evaluation",
            doctor_questions=[
                "Does this hypodensity indicate an acute or subacute ischemic change?",
                "Is a follow-up Diffusion-Weighted MRI (DWI-MRI) indicated?",
                "What antiplatelet or anticoagulant regimen is recommended?",
                "Are there signs of midline shift or mass effect?",
                "When should formal neuro-rehabilitation begin?"
            ]
        )

        kb['CT_CLEAR'] = DiseaseCondition(
            name="Clear Brain CT Scan (No Active Hypodensity)",
            category="Neurology",
            explanation="The brain CT scan demonstrates normal soft tissue attenuation without focal hypodense territorial lesions, mass effect, or midline shift.",
            causes="Normal neuroanatomy without evidence of acute tissue swelling or macroscopic ischemic infarct.",
            untreated_consequences="Maintain healthy cardiovascular & lifestyle habits to prevent future cerebrovascular events.",
            diet_recommended=["Mediterranean diet pattern", "Fresh fruits, vegetables, and legumes", "Whole grains and lean proteins"],
            diet_avoid=["Excessive salt and sodium", "High saturated fat foods"],
            herbal_remedies=[
                {"name": "Gotu Kola (Centella asiatica)", "benefit": "Promotes general cerebral vascular health and mental clarity", "dosage": "300 mg daily"}
            ],
            exercise_allowed=["30 minutes daily moderate cardio", "Bisk walking, jogging, yoga, swimming"],
            exercise_restrictions=["None — maintain standard safe fitness"],
            telemetry_targets={"Blood Pressure": "< 120/80 mmHg", "Heart Rate": "60-100 BPM"},
            specialist="General Physician / Neurologist",
            urgency="Routine",
            doctor_questions=[
                "Does this scan completely rule out early transient symptoms?",
                "Are baseline carotid Doppler studies recommended?",
                "What is my overall 10-year stroke risk assessment?"
            ]
        )

        # ── 2. CHEST X-RAY (CXR) CONDITIONS ────────────────────────────────────
        kb['CXR_PNEUMONIA'] = DiseaseCondition(
            name="Pulmonary Consolidation & Pneumonia",
            category="Pulmonology",
            explanation="Pneumonia is an infection causing inflammation in the lung air sacs (alveoli). On X-rays, fluid, pus, and cellular debris fill alveolar spaces, appearing as opaque white 'consolidation' patches instead of dark air-filled tissue.",
            causes="Caused by bacterial pathogens (Streptococcus pneumoniae), viral respiratory infections (Influenza, RSV), or aspiration of secretions into bronchial trees.",
            untreated_consequences="Delayed treatment can lead to spreading lobar consolidation, pleural effusion, empyema (pus in pleural cavity), respiratory failure, hypoxia, and systemic sepsis.",
            diet_recommended=["Warm broths and clear soups", "Vitamin C rich citrus fruits & amla", "Hydrating warm fluids and herbal teas", "Protein-dense eggs and lentils"],
            diet_avoid=["Dairy products causing excess mucus", "Ice-cold drinks and frozen foods", "Processed greasy foods"],
            herbal_remedies=[
                {"name": "Tulsi (Holy Basil / Ocimum sanctum)", "benefit": "Natural immunomodulator and anti-microbial respiratory tonic", "dosage": "5-10 fresh leaves brewed as tea twice daily"},
                {"name": "Mulethi (Licorice root / Glycyrrhiza glabra)", "benefit": "Soothes inflamed bronchial airways and loosens tenacious phlegm", "dosage": "500 mg powder with warm water"},
                {"name": "Ginger (Zingiber officinale)", "benefit": "Reduces respiratory airway inflammation and alleviates cough", "dosage": "Fresh ginger tea with honey"}
            ],
            exercise_allowed=["Diaphragmatic deep breathing exercises", "Incentive spirometry therapy", "Short indoor walking when fever-free"],
            exercise_restrictions=["Strenuous aerobic activity", "Outdoor exercise in cold or polluted air", "Heavy lifting"],
            telemetry_targets={"SpO2 Oxygen Saturation": "> 95%", "Body Temperature": "< 98.6°F (37°C)", "Respiratory Rate": "12-20 breaths/min"},
            specialist="Pulmonologist",
            urgency="Moderate to High",
            doctor_questions=[
                "Does the consolidation pattern suggest bacterial or viral etiology?",
                "Is targeted antibiotic or antiviral therapy required?",
                "What are my SpO2 target thresholds for home oxygen evaluation?",
                "When should a repeat follow-up Chest X-ray be performed?"
            ]
        )

        kb['CXR_CARDIOMEGALY'] = DiseaseCondition(
            name="Cardiomegaly (Enlarged Heart Silhouette)",
            category="Cardiology",
            explanation="Cardiomegaly indicates an enlarged heart silhouette where the Cardiothoracic Ratio (CTR) exceeds 50% (0.50) on a frontal Chest X-ray. It reflects cardiac ventricular hypertrophy or dilation.",
            causes="Primary causes include chronic systemic hypertension, coronary artery disease, heart valve incompetence/stenosis, dilated cardiomyopathy, or pericardial effusion.",
            untreated_consequences="If untreated, chronic cardiac enlargement leads to progressive heart failure, pulmonary venous congestion, shortness of breath, peripheral edema, and cardiac arrhythmias.",
            diet_recommended=["Strict sodium restricted diet (< 1,200 mg/day)", "Potassium-rich bananas, spinach, and avocados", "Fiber-rich oats and legumes"],
            diet_avoid=["High-sodium canned soups, pickles, and processed meats", "Excess fluid intake if fluid restriction ordered", "Alcohol"],
            herbal_remedies=[
                {"name": "Arjuna Bark (Terminalia arjuna)", "benefit": "Premier Ayurvedic cardiotonic that strengthens heart muscle contraction and improves cardiac output", "dosage": "500 mg extract twice daily"},
                {"name": "Garlic Extract (Allium sativum)", "benefit": "Supports blood pressure reduction and reduces arterial plaque buildup", "dosage": "1-2 raw cloves or 600 mg extract"}
            ],
            exercise_allowed=["Low-impact walking on flat terrain", "Light cardiac rehabilitation exercise"],
            exercise_restrictions=["High-intensity interval training (HIIT)", "Heavy weightlifting", "Exercise in extreme heat"],
            telemetry_targets={"Blood Pressure": "< 125/80 mmHg", "Resting BPM": "60-80 BPM", "Daily Weight": "Monitor for sudden 2+ lb gain"},
            specialist="Cardiologist",
            urgency="Moderate / Prompt Evaluation",
            doctor_questions=[
                "Should we perform an Echocardiogram (Echo) to evaluate ejection fraction?",
                "Is the enlargement due to muscular hypertrophy or fluid accumulation?",
                "What ACE inhibitor or beta-blocker therapy is indicated?"
            ]
        )

        kb['CXR_CLEAR'] = DiseaseCondition(
            name="Clear Chest X-Ray (Normal Pulmonary & Cardiac Contour)",
            category="Pulmonology",
            explanation="The Chest X-ray reveals clear, well-aerated lung parenchyma without consolidation, focal opacities, pleural effusion, or cardiomegaly.",
            causes="Normal pulmonary and thoracic vascular anatomy.",
            untreated_consequences="Maintain good respiratory hygiene and avoid tobacco smoke exposure.",
            diet_recommended=["Antioxidant-rich whole food diet", "Fresh fruits and vegetables"],
            diet_avoid=["Tobacco smoke", "Industrial environmental toxins"],
            herbal_remedies=[
                {"name": "Chyawanprash", "benefit": "Traditional Ayurvedic herbal jam for immune resilience", "dosage": "1 tablespoon daily"}
            ],
            exercise_allowed=["Regular cardiovascular exercise", "Running, swimming, cycling"],
            exercise_restrictions=["None"],
            telemetry_targets={"SpO2": "> 97%", "Resting Heart Rate": "60-100 BPM"},
            specialist="General Physician / Pulmonologist",
            urgency="Routine",
            doctor_questions=[
                "Does this X-ray confirm clear lung fields?",
                "Are any routine preventive vaccinations (pneumococcal/flu) recommended?"
            ]
        )

        # ── 3. ECG CONDITIONS ──────────────────────────────────────────────────
        kb['ECG_AFIB'] = DiseaseCondition(
            name="Atrial Fibrillation / Irregular Rhythm",
            category="Cardiology",
            explanation="Atrial Fibrillation (AFib) is a supraventricular arrhythmia characterized by chaotic, disorganized electrical signals in the heart's upper chambers (atria). On ECG, normal P-waves are absent and replaced by rapid fibrillatory waves with an irregular R-R interval.",
            causes="Caused by hypertension, coronary artery disease, valvular heart disease, hyperthyroidism, excessive alcohol consumption, or age-related atrial fibrosis.",
            untreated_consequences="Stagnant blood in the atria can form thrombi (blood clots), which can travel to the brain and cause a massive ischemic stroke. Chronic AFib also doubles the risk of heart failure.",
            diet_recommended=["Magnesium-rich dark leafy greens and pumpkin seeds", "Omega-3 rich salmon and walnuts", "High-fiber Mediterranean diet"],
            diet_avoid=["Caffeine & energy drinks", "Alcohol (major trigger for AFib episodes)", "High-sodium processed foods", "Excess refined sugar"],
            herbal_remedies=[
                {"name": "Arjuna Bark (Terminalia arjuna)", "benefit": "Promotes electrophysiological stability of atrial tissue and regulates blood pressure", "dosage": "500 mg standardized extract twice daily"},
                {"name": "Hawthorn Berry (Crataegus)", "benefit": "Supports coronary blood flow and helps balance irregular heart rhythm", "dosage": "300-400 mg daily"}
            ],
            exercise_allowed=["Light walking", "Gentle yoga and breathing exercises (Pranayama)"],
            exercise_restrictions=["Strenuous high-exertion athletics during uncontrolled episodes", "Sudden heavy lifting"],
            telemetry_targets={"Heart Rate": "60-100 BPM at rest", "Blood Pressure": "< 130/80 mmHg", "CHA2DS2-VASc Score": "Evaluate stroke risk"},
            specialist="Cardiologist / Electrophysiologist",
            urgency="High / Prompt Evaluation",
            doctor_questions=[
                "What is my CHA2DS2-VASc score for stroke risk?",
                "Is oral anticoagulation (DOAC/Warfarin) indicated?",
                "Should we pursue rate control or rhythm control (cardioversion/ablation)?"
            ]
        )

        kb['ECG_TACHYCARDIA'] = DiseaseCondition(
            name="Sinus Tachycardia (Elevated Heart Rate)",
            category="Cardiology",
            explanation="Sinus Tachycardia is defined as a resting heart rate exceeding 100 beats per minute originating from the sinoatrial (SA) node with normal P-wave morphology.",
            causes="Triggers include acute anxiety, dehydration, fever, anemia, hyperthyroidism, excessive caffeine/stimulants, or underlying cardiac stress.",
            untreated_consequences="Persistent untreated tachycardia increases myocardial oxygen demand, leading to fatigue, cardiac strain, and reduced ventricular filling efficiency.",
            diet_recommended=["Electrolyte-replenishing coconut water", "Magnesium and potassium-rich foods", "Abundant hydration (2-3 liters water/day)"],
            diet_avoid=["Caffeinated coffee, tea, and energy drinks", "Nicotine and tobacco", "Alcohol and sugar spikes"],
            herbal_remedies=[
                {"name": "Brahmi (Bacopa monnieri)", "benefit": "Calms parasympathetic nervous system overdrive and lowers stress-induced heart rate", "dosage": "300 mg daily"},
                {"name": "Chamomile & Lemon Balm Tea", "benefit": "Natural mild sedative that eases autonomic cardiac arousal", "dosage": "1 cup brewed tea in evening"}
            ],
            exercise_allowed=["Calming walks", "Relaxation exercises, meditation, and deep diaphragmatic breathing"],
            exercise_restrictions=["Intense cardio or sprinting while heart rate remains elevated"],
            telemetry_targets={"Resting Heart Rate": "60-90 BPM target", "Blood Pressure": "< 120/80 mmHg"},
            specialist="Cardiologist / General Physician",
            urgency="Moderate",
            doctor_questions=[
                "Is this tachycardia sinus rhythm or a supraventricular arrhythmia?",
                "Should we order thyroid function tests (TSH) and blood counts?",
                "Would a short-acting beta-blocker be helpful?"
            ]
        )

        kb['ECG_NORMAL'] = DiseaseCondition(
            name="Normal Sinus Rhythm",
            category="Cardiology",
            explanation="The ECG demonstrates a normal sinus rhythm with regular P-waves preceding every QRS complex at a rate between 60 and 100 BPM.",
            causes="Normal cardiac electrophysiology and healthy sinoatrial node pacing.",
            untreated_consequences="Maintain healthy cardiovascular lifestyle.",
            diet_recommended=["Balanced heart-healthy Mediterranean diet"],
            diet_avoid=["Excessive caffeine, sodium, and trans fats"],
            herbal_remedies=[
                {"name": "Arjuna Bark", "benefit": "General cardiotonic maintenance", "dosage": "250 mg daily"}
            ],
            exercise_allowed=["Regular cardiovascular & resistance training"],
            exercise_restrictions=["None"],
            telemetry_targets={"Heart Rate": "60-100 BPM", "Blood Pressure": "< 120/80 mmHg"},
            specialist="Cardiologist / Physician",
            urgency="Routine",
            doctor_questions=[
                "Does this ECG confirm healthy sinus rhythm?",
                "How often should routine screening ECGs be repeated?"
            ]
        )

        # ── 4. BLOOD TEST CONDITIONS ───────────────────────────────────────────
        kb['BLOOD_DIABETES'] = DiseaseCondition(
            name="Hyperglycemia & Type-2 Diabetes Mellitus",
            category="Endocrinology",
            explanation="Characterized by elevated blood glucose levels (fasting glucose > 126 mg/dL or HbA1c > 6.5%). Indicates insulin resistance where cells fail to absorb circulating glucose efficiently.",
            causes="Pancreatic beta-cell dysfunction combined with peripheral tissue insulin resistance, sedentary lifestyle, obesity, and genetic predisposition.",
            untreated_consequences="Chronic uncontrolled hyperglycemia inflicts widespread microvascular damage leading to diabetic retinopathy (blindness), diabetic nephropathy (kidney failure), peripheral neuropathy, and accelerated coronary artery disease.",
            diet_recommended=["Complex low-GI carbohydrates (quinoa, steel-cut oats, legumes)", "Non-starchy vegetables (broccoli, cucumbers, bell peppers)", "Healthy fats (flaxseed, chia, almonds)"],
            diet_avoid=["White sugar, sodas, and fruit juices", "White bread, white rice, and refined flour", "Trans fats and high-fat processed snacks"],
            herbal_remedies=[
                {"name": "Gurmar (Gymnema sylvestre)", "benefit": "Known as the 'sugar destroyer', helps suppress sweet taste receptors and improves pancreatic insulin secretion", "dosage": "500 mg extract before meals"},
                {"name": "Methi / Fenugreek Seeds (Trigonella foenum-graecum)", "benefit": "Rich in soluble fiber that slows carbohydrate absorption and lowers postprandial glucose", "dosage": "1 teaspoon soaked seeds daily morning"},
                {"name": "Cinnamon (Cinnamomum verum)", "benefit": "Enhances cellular insulin sensitivity and glucose uptake", "dosage": "1/2 teaspoon powder with warm water"}
            ],
            exercise_allowed=["Brisk walking 45 minutes daily (greatly increases muscle insulin sensitivity)", "Resistance training with light weights", "Yoga"],
            exercise_restrictions=["High-impact jumping if diabetic peripheral neuropathy is present"],
            telemetry_targets={"HbA1c": "< 6.5%", "Fasting Glucose": "80-130 mg/dL", "Postprandial Glucose": "< 180 mg/dL"},
            specialist="Endocrinologist / Diabetologist",
            urgency="Moderate / Routine Management",
            doctor_questions=[
                "What is my baseline HbA1c and average blood glucose?",
                "Should we initiate Metformin or combination therapy?",
                "What is the target frequency for capillary glucose self-monitoring?"
            ]
        )

        kb['BLOOD_ANEMIA'] = DiseaseCondition(
            name="Anemia (Low Hemoglobin / RBC Count)",
            category="Hematology",
            explanation="Anemia is characterized by a deficit in red blood cells or hemoglobin concentration (Hb < 12 g/dL in women, < 13 g/dL in men), reducing oxygen-carrying capacity of the blood.",
            causes="Iron deficiency, nutritional B12/folate deficiency, chronic blood loss, chronic kidney disease, or bone marrow suppression.",
            untreated_consequences="Causes chronic tissue hypoxia, fatigue, dizziness, pallor, and compensatory tachycardia which can lead to high-output heart failure over time.",
            diet_recommended=["Iron-rich green leafy vegetables (spinach, beet greens)", "Pomegranate, raisins, and dates", "Vitamin C rich food alongside iron to boost absorption"],
            diet_avoid=["Tea and coffee taken immediately with meals (tannins inhibit iron absorption)", "Calcium supplements taken simultaneously with iron"],
            herbal_remedies=[
                {"name": "Amla (Emblica officinalis / Indian Gooseberry)", "benefit": "Extremely rich in Vitamin C, dramatically enhances dietary iron bio-absorption", "dosage": "1-2 fresh fruits or 10 ml juice daily"},
                {"name": "Punarnava (Boerhavia diffusa)", "benefit": "Traditional Ayurvedic hematinic herb that stimulates red blood cell production", "dosage": "300-500 mg daily"}
            ],
            exercise_allowed=["Light gentle walking", "Restorative yoga and stretching"],
            exercise_restrictions=["High-intensity strenuous exertion while hemoglobin is low"],
            telemetry_targets={"Hemoglobin (Hb)": "13.5-17.5 g/dL (men), 12.0-15.5 g/dL (women)", "Ferritin": "> 30 ng/mL"},
            specialist="Hematologist / General Physician",
            urgency="Moderate",
            doctor_questions=[
                "Is the anemia microcytic (iron deficiency) or macrocytic (B12/folate)?",
                "What oral iron supplementation or IV iron protocol is recommended?",
                "Should we screen for occult gastrointestinal blood loss?"
            ]
        )

        kb['BLOOD_NORMAL'] = DiseaseCondition(
            name="Normal Blood Metabolic & Hematology Panel",
            category="General Medicine",
            explanation="All blood panel metrics including CBC, renal function, liver enzymes, and blood glucose fall within standard physiological reference ranges.",
            causes="Normal hematological and organ metabolic function.",
            untreated_consequences="Maintain healthy nutrition and annual routine blood screening.",
            diet_recommended=["Balanced nutritional diet rich in fresh whole foods"],
            diet_avoid=["Ultra-processed foods and excess alcohol"],
            herbal_remedies=[
                {"name": "Triphala", "benefit": "Gentle daily digestive and metabolic tonic", "dosage": "1/2 teaspoon with warm water at bedtime"}
            ],
            exercise_allowed=["Regular physical exercise program"],
            exercise_restrictions=["None"],
            telemetry_targets={"Fasting Glucose": "< 100 mg/dL", "Hemoglobin": "Normal range", "Creatinine": "< 1.2 mg/dL"},
            specialist="General Physician",
            urgency="Routine",
            doctor_questions=[
                "Are all blood parameters within normal limits?",
                "When should routine annual health checkup blood tests be scheduled?"
            ]
        )

        # ── 5. DERMATOLOGY CONDITIONS ──────────────────────────────────────────
        kb['DERMATO_LESION'] = DiseaseCondition(
            name="Asymmetric Pigmented Skin Lesion",
            category="Dermatology",
            explanation="Dermatological analysis detected a skin lesion exhibiting structural asymmetry, border irregularity, or variegated pigmentation patterns requiring clinical dermoscopy evaluation.",
            causes="Can arise from atypical dysplastic nevi, actinic keratosis, seborrheic keratosis, or cutaneous melanoma transformation driven by UV radiation exposure.",
            untreated_consequences="If a dysplastic or malignant skin lesion is left unmonitored, invasive melanoma can metastasize into regional lymph nodes and distant organ systems.",
            diet_recommended=["Antioxidant-rich berries, tomatoes (lycopene), and green tea", "Foods high in Vitamin E & C", "Plenty of water"],
            diet_avoid=["Excessive sun exposure without SPF 50+ protection", "Tanning beds"],
            herbal_remedies=[
                {"name": "Neem (Azadirachta indica)", "benefit": "Potent anti-inflammatory and dermal purification herb", "dosage": "Topical neem oil application / 250 mg extract"},
                {"name": "Aloe Vera", "benefit": "Soothes skin tissue and reduces dermal inflammatory oxidative stress", "dosage": "Pure topical gel applied twice daily"}
            ],
            exercise_allowed=["Indoor exercise and gym workouts", "Outdoor activity early morning or evening with SPF 50+ sunscreen"],
            exercise_restrictions=["Direct peak-sun outdoor exercise (10 AM - 4 PM) without protective clothing"],
            telemetry_targets={"ABCDE Rule Check": "Monitor for changes in Size, Shape, or Color"},
            specialist="Dermatologist",
            urgency="Prompt Dermoscopy Review",
            doctor_questions=[
                "Is a formal handheld dermoscopy evaluation required for this lesion?",
                "Does this lesion meet criteria for a punch or excisional biopsy?",
                "How often should total-body skin examinations be scheduled?"
            ]
        )

        kb['DERMATO_CLEAR'] = DiseaseCondition(
            name="Clear Skin Scan (No Suspicious Lesions)",
            category="Dermatology",
            explanation="The dermatological scan reveals uniform skin tissue without suspicious asymmetric pigmentation, irregular borders, or structural lesion boundaries.",
            causes="Healthy cutaneous tissue.",
            untreated_consequences="Continue broad-spectrum UV protection.",
            diet_recommended=["Skin-hydrating whole foods, nuts, and seeds"],
            diet_avoid=["Excessive UV sun exposure without protection"],
            herbal_remedies=[
                {"name": "Aloe Vera", "benefit": "Natural skin hydration and maintenance", "dosage": "Topical application as desired"}
            ],
            exercise_allowed=["Regular exercise with sun protection"],
            exercise_restrictions=["None"],
            telemetry_targets={"Sunscreen Protection": "SPF 30+ daily"},
            specialist="Dermatologist",
            urgency="Routine",
            doctor_questions=[
                "Are there any baseline skin moles to monitor over time?",
                "What daily sun protection regimen is recommended for my skin type?"
            ]
        )

        # ── 6. RETINAL CONDITIONS ──────────────────────────────────────────────
        kb['RETINAL_GLAUCOMA'] = DiseaseCondition(
            name="Elevated Cup-to-Disc Ratio (Glaucoma Risk Indicator)",
            category="Ophthalmology",
            explanation="Fundus scan analysis revealed an elevated Optic Cup-to-Disc Ratio (CDR > 0.65). This structural cupping indicates thinning of the neuroretinal rim and retinal nerve fiber layer.",
            causes="Primary cause is elevated intraocular pressure (IOP) damaging optic nerve fibers, impaired microvascular ocular perfusion, or genetic ocular susceptibility.",
            untreated_consequences="Progressive optic nerve atrophy leads to irreversible loss of peripheral visual fields (tunnel vision) and eventual complete blindness.",
            diet_recommended=["Dark leafy greens rich in lutein and zeaxanthin (kale, spinach)", "Omega-3 rich fish and chia seeds", "Flavonoid-rich dark chocolate & green tea"],
            diet_avoid=["Heavy caffeine consumption (can transiently raise IOP)", "Drinking large volumes of water in a single rapid chug"],
            herbal_remedies=[
                {"name": "Bilberry Extract (Vaccinium myrtillus)", "benefit": "Rich in anthocyanins that strengthen retinal capillary microvascular structures", "dosage": "120-240 mg standardized extract daily"},
                {"name": "Ginkgo Biloba", "benefit": "Enhances ocular microvascular blood flow to the optic nerve head", "dosage": "120 mg daily"}
            ],
            exercise_allowed=["Moderate walking and light aerobic exercise (helps lower intraocular pressure)"],
            exercise_restrictions=["Inverted yoga postures (headstands) which significantly increase IOP", "Heavy weightlifting strain"],
            telemetry_targets={"Intraocular Pressure (IOP)": "< 21 mmHg", "Cup-to-Disc Ratio (CDR)": "< 0.50 target"},
            specialist="Ophthalmologist / Glaucoma Specialist",
            urgency="Prompt Evaluation",
            doctor_questions=[
                "What is my tonometry Intraocular Pressure (IOP) reading?",
                "Should we perform an Optical Coherence Tomography (OCT) scan of the optic nerve?",
                "Are IOP-lowering eye drops (prostaglandin analogs / beta-blockers) indicated?"
            ]
        )

        kb['RETINAL_CLEAR'] = DiseaseCondition(
            name="Normal Retinal Fundus Scan",
            category="Ophthalmology",
            explanation="Retinal fundus image demonstrates normal optic disc anatomy with a healthy Cup-to-Disc Ratio (CDR < 0.50), intact vascular architecture, and clear macula.",
            causes="Healthy ocular posterior segment neuroanatomy.",
            untreated_consequences="Maintain routine comprehensive dilated eye examinations.",
            diet_recommended=["Lutein and Vitamin A rich foods (carrots, sweet potatoes, spinach)"],
            diet_avoid=["Prolonged unshielded blue light / UV glare"],
            herbal_remedies=[
                {"name": "Triphala Eye Wash (Sterile)", "benefit": "Traditional ocular soothing herb", "dosage": "As recommended by eye specialist"}
            ],
            exercise_allowed=["Regular physical activity"],
            exercise_restrictions=["None"],
            telemetry_targets={"Visual Acuity": "20/20 target", "IOP": "10-21 mmHg"},
            specialist="Ophthalmologist / Optometrist",
            urgency="Routine",
            doctor_questions=[
                "Does this fundus scan confirm normal optic disc and macula?",
                "When should the next routine eye exam take place?"
            ]
        )

        # ── 7. BONE X-RAY CONDITIONS ───────────────────────────────────────────
        kb['BONE_FRACTURE'] = DiseaseCondition(
            name="Cortical Discontinuity & Fracture Risk",
            category="Orthopedics",
            explanation="Radiographic evaluation detected cortical boundary disruption, linear radiolucent discontinuity lines, or structural bone misalignment consistent with a fracture.",
            causes="Traumatic impact, fall, mechanical stress overload, or pathological bone weakening from osteopenia/osteoporosis.",
            untreated_consequences="Improperly managed bone fractures risk non-union, mal-union misalignment, chronic osteomyelitis infection, joint instability, and secondary post-traumatic arthritis.",
            diet_recommended=["Calcium-rich dairy, ragi (finger millet), and sesame seeds", "Vitamin D3 rich fortified foods and egg yolks", "Protein-dense foods for collagen bone matrix repair"],
            diet_avoid=["Carbonated cola drinks (phosphoric acid leaches bone calcium)", "Excessive sodium", "Alcohol and smoking"],
            herbal_remedies=[
                {"name": "Hadjoori / Hadjod (Cissus quadrangularis)", "benefit": "Famous Ayurvedic 'bone setter' herb that accelerates fracture healing and osteoblast mineralization", "dosage": "500 mg standardized extract twice daily"},
                {"name": "Shilajit", "benefit": "Rich in fulvic acid and trace minerals that support bone calcium deposition", "dosage": "250-500 mg purified resin/powder with warm milk"}
            ],
            exercise_allowed=["Immobilization of affected fracture limb", "Gentle non-weight bearing range of motion for adjacent uninjured joints"],
            exercise_restrictions=["Strictly NO weight-bearing or impact on the injured bone until cleared by orthopedic surgeon"],
            telemetry_targets={"Serum Calcium": "8.5-10.2 mg/dL", "Vitamin D (25-OH)": "30-50 ng/mL"},
            specialist="Orthopedic Surgeon",
            urgency="High / Urgent Evaluation",
            doctor_questions=[
                "Is this a complete or incomplete / stress fracture?",
                "Is conservative cast/splint immobilization adequate, or is surgical fixation (ORIF) needed?",
                "What is the expected timeline for radiographic callus formation?"
            ]
        )

        kb['BONE_CLEAR'] = DiseaseCondition(
            name="Normal Bone Cortical Alignment & Radiodensity",
            category="Orthopedics",
            explanation="The skeletal Radiograph reveals continuous cortical margins, intact trabecular architecture, and normal joint space alignment without acute fracture lines.",
            causes="Normal skeletal bone structure.",
            untreated_consequences="Maintain bone-density supportive exercise and nutrition.",
            diet_recommended=["Calcium and Vitamin D rich diet"],
            diet_avoid=["Excessive soft drinks and tobacco"],
            herbal_remedies=[
                {"name": "Hadjod", "benefit": "Daily bone mineral density support", "dosage": "250 mg daily"}
            ],
            exercise_allowed=["Weight-bearing exercise (walking, jogging, resistance training) to maintain bone density"],
            exercise_restrictions=["None"],
            telemetry_targets={"Bone Mineral Density": "T-score > -1.0"},
            specialist="Orthopedic Specialist / Physician",
            urgency="Routine",
            doctor_questions=[
                "Are my bone structure and joint spaces clear?",
                "Is a DEXA bone density scan recommended based on my age?"
            ]
        )

        return kb

    def identify_condition(self, modality: str, findings_text: str) -> DiseaseCondition:
        """
        Match modality + findings_text to the best DiseaseCondition in the local KB.
        """
        text_lower = (findings_text or "").lower()
        m = (modality or "").upper()

        if m == 'CT':
            if any(w in text_lower for w in ['hypodense', 'stroke', 'edema', 'ischemic', 'infarct', 'anomaly detected']):
                return self.database['CT_ISCHEMIC_STROKE']
            return self.database['CT_CLEAR']

        elif m == 'CXR':
            if any(w in text_lower for w in ['pneumonia', 'consolidation', 'opacity', 'infiltrate', 'lung']):
                return self.database['CXR_PNEUMONIA']
            elif any(w in text_lower for w in ['cardiomegaly', 'enlarged', 'heart shadow', 'ctr']):
                return self.database['CXR_CARDIOMEGALY']
            return self.database['CXR_CLEAR']

        elif m == 'ECG':
            if any(w in text_lower for w in ['fibrillation', 'afib', 'irregular', 'arrhythmia']):
                return self.database['ECG_AFIB']
            elif any(w in text_lower for w in ['tachycardia', 'fast', 'elevated rate', 'bpm']):
                return self.database['ECG_TACHYCARDIA']
            return self.database['ECG_NORMAL']

        elif m == 'BLOOD_TEST':
            if any(w in text_lower for w in ['glucose', 'diabetes', 'sugar', 'hba1c', 'hyperglycemia']):
                return self.database['BLOOD_DIABETES']
            elif any(w in text_lower for w in ['anemia', 'hemoglobin', 'rbc', 'low hb', 'iron']):
                return self.database['BLOOD_ANEMIA']
            return self.database['BLOOD_NORMAL']

        elif m == 'DERMATO':
            if any(w in text_lower for w in ['asymmetry', 'lesion', 'irregular', 'pigmentation', 'melanoma']):
                return self.database['DERMATO_LESION']
            return self.database['DERMATO_CLEAR']

        elif m == 'RETINAL':
            if any(w in text_lower for w in ['cup', 'disc', 'cdr', 'cupping', 'glaucoma', 'tortuosity']):
                return self.database['RETINAL_GLAUCOMA']
            return self.database['RETINAL_CLEAR']

        elif m == 'BONE_XRAY':
            if any(w in text_lower for w in ['fracture', 'cortical', 'discontinuity', 'disruption', 'break']):
                return self.database['BONE_FRACTURE']
            return self.database['BONE_CLEAR']

        # Default fallback to Brain CT Ischemic Stroke if unknown text with detected anomalies
        return self.database['CT_ISCHEMIC_STROKE'] if 'anomaly' in text_lower else self.database['CT_CLEAR']


_engine = None

def get_disease_knowledge_engine() -> DiseaseKnowledgeEngine:
    global _engine
    if _engine is None:
        _engine = DiseaseKnowledgeEngine()
    return _engine
