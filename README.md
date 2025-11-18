# team-SRS
# 💊 AI Medical Prescription Verification System

A comprehensive Streamlit-based application for verifying prescriptions, checking drug interactions, recommending age-appropriate dosages, and suggesting alternative medications.

## 🎯 Features

### 1. **Single Drug Check** 💉
- Search for any medication in our database (50+ drugs)
- View detailed drug information
- Get age-appropriate dosage recommendations
- Check known interactions
- See alternative medications

### 2. **Multi-Drug Interaction Checker** ⚡
- Add up to multiple medications
- Check for drug-drug interactions
- View severity levels (Contraindicated/Major/Moderate/Minor)
- Get age-specific dosage recommendations
- Patient profile management (age, weight, height, conditions, allergies)

### 3. **Prescription Text Parser** 📝
- Paste prescription text
- Automatic drug extraction using NLP
- Extracts: drug name, dosage, frequency, route, duration
- Full interaction analysis of extracted medications
- Download results

### 4. **Prescription Image Upload** 📸
- Upload prescription photos (JPG, PNG, JPEG, BMP)
- OCR text extraction from images
- Editable extracted text
- Automatic medication parsing
- Full analysis with image reference

### 5. **Patient Profile Management** 👤
- Save patient demographics
- Store medical history
- Track drug allergies
- BMI calculation
- Persistent profile storage

## 📊 Database Contents

- **50+ Medications**: Common drugs with detailed information
- **30+ Interactions**: Drug-drug interactions with mechanisms
- **Dosage Formulas**: 6 different calculation methods
  - Clark's Rule (weight-based)
  - Young's Rule (age-based)
  - Fried's Rule (infants)
  - BSA Mosteller (height & weight)
  - Dilling's Rule
  - Webster Rule

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd prescription-verifier
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run prescription_verifier.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`

## 📖 Usage Guide

### Single Drug Check
1. Select a medication from dropdown
2. Enter patient age (and optionally weight, height)
3. View:
   - Drug information card
   - Age-appropriate dosages
   - Known interactions
   - Alternative medications

### Multi-Drug Checker
1. Enter patient profile (age, weight, height, conditions, allergies)
2. Select multiple medications (up to 5+)
3. View:
   - Interaction matrix with severity levels
   - Management recommendations
   - Dosage for each drug
   - Alternative medication suggestions

### Prescription Parser
1. Paste prescription text or use sample
2. Click "Parse Prescription"
3. System extracts: drug name, dose, frequency, route
4. Add patient age/weight
5. Click "Analyze Interactions" to see full analysis

### Upload Prescription Image
1. Upload clear prescription photo
2. Review extracted text (edit if needed)
3. Click "Confirm and Analyze"
4. View medications extracted from image
5. Add patient info and run full analysis

### Patient Profile
1. Fill in demographic information
2. Add medical conditions and allergies
3. Save profile (stored in session)
4. Use saved profile across sessions

## 🎨 UI Features

**Color-Coded Severity Levels:**
- 🔴 **Contraindicated** (Red): Should NOT use together
- 🟠 **Major** (Orange): Serious interaction risk
- 🟡 **Moderate** (Yellow): Moderate caution needed
- 🟢 **Minor** (Green): Safe to use together

**Professional Medical Theme:**
- Clean, organized interface
- Clear data tables
- Expandable sections
- Real-time validation
- Responsive design

## 📋 Medications in Database

**Common drugs include:**
Warfarin, Metformin, Aspirin, Lisinopril, Ibuprofen, Amoxicillin, Atorvastatin, Omeprazole, Levothyroxine, Sertraline, Amlodipine, Furosemide, Metoprolol, Simvastatin, Albuterol, Prednisone, Clopidogrel, Fluoxetine, Diclofenac, Ranitidine

*More can be easily added to the DRUG_DATABASE dictionary*

## 💾 Data Management

All data is stored locally:
- Patient profiles in session state
- No cloud synchronization
- Privacy-compliant (HIPAA-friendly)
- All computations done client-side

## 🧮 Dosage Formula Examples

### Clark's Rule (Weight-based)
```
Dose = (Weight in kg / 70) × Adult Dose
Example: (20 kg / 70) × 500 mg = 142.86 mg
```

### Young's Rule (Age-based)
```
Dose = (Age / (Age + 12)) × Adult Dose
Example: (5 / 17) × 100 mg = 29.4 mg
```

### BSA Mosteller (Most Accurate)
```
BSA = √(Height_cm × Weight_kg / 3600)
Dose = (Patient BSA / Adult BSA of 1.73) × Adult Dose
```

## ⚠️ Important Disclaimer

**THIS SYSTEM IS FOR EDUCATIONAL PURPOSES ONLY**

- Not intended for clinical decision-making
- Not a substitute for professional medical advice
- Consult healthcare professionals before medication changes
- Do not rely solely on this system for treatment decisions
- Always verify information with licensed pharmacists/doctors
- Use case: Learning, research, demonstration purposes

## 🔧 Customization

### Add New Medications
Edit `DRUG_DATABASE` in the code:
```python
"New Drug Name": {
    "brand_names": ["Brand1", "Brand2"],
    "class": "Drug Class",
    "uses": ["Use 1", "Use 2"],
    "adult_dose": "X mg dosage",
    "side_effects": ["Effect 1", "Effect 2"],
    "contraindications": ["Contraindication 1"],
}
```

### Add New Interactions
Edit `INTERACTIONS_DATABASE`:
```python
{
    "drug1": "Drug Name 1",
    "drug2": "Drug Name 2",
    "severity": "Major",
    "mechanism": "How they interact...",
    "management": "What to do...",
}
```

## 🐛 Troubleshooting

**App won't start?**
- Check Python version (need 3.8+)
- Verify all dependencies installed: `pip install -r requirements.txt`

**Image upload not working?**
- Ensure file is JPG/PNG/JPEG/BMP format
- Check file size (max 5MB)
- Try a different prescription photo

**Dosage calculation shows "Not specified"?**
- Ensure all required fields filled
- Age must be 0-120 years
- Weight must be positive number

**Drugs not being extracted?**
- Ensure drug names spelled correctly
- Drug name must be in database
- Add more drugs to database if needed

## 📞 Support

For issues or questions:
1. Check the About section in the app
2. Review this README
3. Verify all dependencies installed
4. Check Streamlit documentation: https://docs.streamlit.io/

## 🎓 Learn More

**Prescription Verification:**
- Drug databases: DrugBank, RxNorm
- Interaction mechanisms
- Dosage calculations

**Medical Technology:**
- NLP for medical text
- OCR for prescription images
- Healthcare data management

## 📄 License

Educational project - Smart Intern Hackathon 2025

## 🙏 Acknowledgments

Built with:
- Streamlit - Web app framework
- Pandas - Data manipulation
- Pillow - Image processing
- EasyOCR - Optical character recognition

---

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Status:** Active Development
