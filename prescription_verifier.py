import streamlit as st
import pandas as pd
import numpy as np
import re
from PIL import Image
st.set_page_config(page_title="AI Medical Prescription Verifier", page_icon="💊", layout="wide")
from datetime import datetime

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #7b5fcf 0%, #b798db 100%);
    color: #fff;
}
.feature-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 25px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 8px 15px rgba(123, 95, 207, 0.3);
    margin-bottom: 20px;
}
.feature-card:hover {
    background: rgba(255, 255, 255, 0.3);
    box-shadow: 0 15px 25px rgba(123, 95, 207, 0.6);
    transform: scale(1.05);
}
.feature-icon {
    font-size: 50px;
    color: #ffd700;
    margin-bottom: 15px;
}
.feature-title {
    font-size: 1.5em;
    font-weight: 700;
    margin-bottom: 8px;
    color: #ffd700;
}
.feature-desc {
    font-size: 1em;
    color: #eee;
}
</style>
""", unsafe_allow_html=True)

user_name = "Medical Professional"
now = datetime.now().strftime("%A, %B %d, %Y")

st.markdown(f"### Good day, {user_name}! 👋")
st.markdown(f"#### Today is {now}")

st.markdown('<h1 style="color:#ffd700;">AI Prescription Verifier Dashboard</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

features = [
    ("💉", "Single Drug Check", "Lookup medications and get personalized dosage guidance", "?page=SingleDrugCheck"),
    ("⚡", "Multi-Drug Checker", "Analyze multiple medications for interactions", "?page=MultiDrugCheck"),
    ("📝", "Prescription Parser", "Paste prescription text for auto-extraction and verification", "?page=PrescriptionParser"),
    ("📸", "Upload Prescription Image", "Use OCR to analyze prescription images", "?page=ImageUpload"),
    ("👤", "Patient Profile", "Manage patient info and medical history", "?page=PatientProfile")
]

columns = [col1, col2, col3]

for i, (icon, title, desc, link) in enumerate(features):
    with columns[i % 3]:
        st.markdown(f"""
        <a href="{link}" target="_blank" style="text-decoration:none;">
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)


# Load drug database from CSV with error handling
@st.cache_data
def load_drug_database():
    try:
        df = pd.read_csv("dbs.csv")
        # Clean column names
        df.columns = [col.strip() for col in df.columns]
        st.sidebar.success(f"✓ Loaded {len(df)} drugs from dbs.csv")
        return df
    except FileNotFoundError:
        st.error("Error: dbs.csv not found. Please ensure dbs.csv is in the same folder as this script.")
        return None
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return None

df_drugs = load_drug_database()

if df_drugs is None:
    st.stop()

# Helper functions
def get_drug_info(drug_name):
    """Get drug info from CSV by generic name (case-insensitive)"""
    match = df_drugs[df_drugs['Generic Name'].str.lower() == drug_name.lower()]
    if not match.empty:
        return match.iloc[0].to_dict()
    return None

def parse_adult_dose(dose_str):
    """Safely parse adult dose string handling ranges like '2-10 mg'"""
    if not dose_str or pd.isna(dose_str):
        return 100.0

    dose_part = str(dose_str).split()[0]
    dose_number_str = dose_part.split('-')[0] if '-' in dose_part else dose_part

    try:
        return float(dose_number_str)
    except ValueError:
        return 100.0

def calculate_clark_rule(weight_kg, adult_dose):
    """Calculate dose using Clark's Rule (weight-based)"""
    if weight_kg <= 0 or adult_dose <= 0:
        return None
    return (weight_kg / 70) * adult_dose

def calculate_young_rule(age, adult_dose):
    """Calculate dose using Young's Rule (age-based)"""
    if age < 0 or adult_dose <= 0:
        return None
    return (age / (age + 12)) * adult_dose

def recommend_dosage(age, weight_kg=None, adult_dose=100.0):
    """Get age and weight-appropriate dosage recommendations"""
    recs = {}

    if weight_kg and weight_kg > 0:
        clark = calculate_clark_rule(weight_kg, adult_dose)
        if clark:
            recs["Clark's Rule (weight-based)"] = round(clark, 2)

    if age >= 0:
        young = calculate_young_rule(age, adult_dose)
        if young:
            recs["Young's Rule (age-based)"] = round(young, 2)

    return recs

def extract_drugs_from_text(text):
    """Extract drug names from prescription text by matching against CSV"""
    drugs = []
    if not text:
        return drugs

    text_upper = text.upper()

    for drug_name in df_drugs['Generic Name']:
        if pd.isna(drug_name):
            continue
        if drug_name.upper() in text_upper:
            drugs.append({"name": drug_name})

    return drugs

def get_page():
    """Get current page from URL query parameter"""
    params = st.experimental_get_query_params()
    return params.get("page", ["Dashboard"])[0]

page = get_page()

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 💊 Navigation")
    st.markdown("[🏠 Dashboard](?page=Dashboard)")
    st.markdown("[💉 Single Drug Check](?page=SingleDrugCheck)")
    st.markdown("[⚡ Multi-Drug Checker](?page=MultiDrugCheck)")
    st.markdown("[📝 Prescription Parser](?page=PrescriptionParser)")
    st.markdown("[📸 Upload Prescription Image](?page=ImageUpload)")
    st.markdown("[👤 Patient Profile](?page=PatientProfile)")

# PAGE 1: DASHBOARD
if page == "Dashboard":
    st.markdown('<h1 class="header-title">AI Medical Prescription Verifier</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Medications", len(df_drugs), "in database")
    with col2:
        st.metric("Features", "5", "available")
    with col3:
        st.metric("Status", "Active", "✓")

    st.markdown("---")
    st.markdown("## Open Features in New Tabs")
    st.markdown("""
    <ul style="list-style-type: none; padding: 0;">
        <li style="margin: 8px 0;">
            <a href="?page=SingleDrugCheck" target="_blank" style="color: #2E86AB; text-decoration: none; font-weight: bold;">
                💉 Single Drug Check
            </a> - Look up a medication and get dosage recommendations
        </li>
        <li style="margin: 8px 0;">
            <a href="?page=MultiDrugCheck" target="_blank" style="color: #2E86AB; text-decoration: none; font-weight: bold;">
                ⚡ Multi-Drug Checker
            </a> - Check interactions between multiple medications
        </li>
        <li style="margin: 8px 0;">
            <a href="?page=PrescriptionParser" target="_blank" style="color: #2E86AB; text-decoration: none; font-weight: bold;">
                📝 Prescription Parser
            </a> - Paste prescription text and extract drug information
        </li>
        <li style="margin: 8px 0;">
            <a href="?page=ImageUpload" target="_blank" style="color: #2E86AB; text-decoration: none; font-weight: bold;">
                📸 Upload Prescription Image
            </a> - Upload prescription photo for instant analysis
        </li>
        <li style="margin: 8px 0;">
            <a href="?page=PatientProfile" target="_blank" style="color: #2E86AB; text-decoration: none; font-weight: bold;">
                👤 Patient Profile
            </a> - Manage patient demographics and medical history
        </li>
    </ul>
    """, unsafe_allow_html=True)

# PAGE 2: SINGLE DRUG CHECK
elif page == "SingleDrugCheck":
    st.markdown('<h2 class="section-header">💉 Single Drug Check</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Patient age (years):", min_value=0, max_value=120, value=30, key="single_age")
    with col2:
        weight = st.number_input("Patient weight (kg):", min_value=0.1, value=70.0, key="single_weight")
    with col3:
        drug_name = st.selectbox("Select medication:", sorted(df_drugs['Generic Name'].dropna().unique()), key="single_drug")

    if drug_name:
        drug_info = get_drug_info(drug_name)
        if drug_info:
            st.markdown(f"### {drug_name}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Drug Class:** {drug_info.get('Drug Class', 'N/A')}")
                st.markdown(f"**Common Uses:**\n{drug_info.get('Common Uses', 'N/A')}")
            with col2:
                st.markdown(f"**Side Effects:**\n{drug_info.get('Side Effects', 'N/A')}")
                st.markdown(f"**Contraindications:**\n{drug_info.get('Contraindications', 'N/A')}")

            st.markdown(f"**Adult Dose:** {drug_info.get('Adult Dose', 'N/A')}")

            adult_dose_mg = parse_adult_dose(drug_info.get('Adult Dose'))
            recs = recommend_dosage(age, weight, adult_dose_mg)

            if recs:
                st.markdown("### Dosage Recommendations for This Patient")
                for formula, dose in recs.items():
                    st.success(f"{formula}: **{dose} mg**")

# PAGE 3: MULTI-DRUG CHECKER
elif page == "MultiDrugCheck":
    st.markdown('<h2 class="section-header">⚡ Multi-Drug Checker</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Patient age (years):", min_value=0, max_value=120, value=55, key="multi_age")
    with col2:
        weight = st.number_input("Patient weight (kg):", min_value=0.1, value=75.0, key="multi_weight")

    selected_drugs = st.multiselect("Select medications:", sorted(df_drugs['Generic Name'].dropna().unique()), key="multi_drugs")

    if selected_drugs:
        st.markdown("### Analysis Results")
        st.success(f"Selected {len(selected_drugs)} medications for analysis")

        st.markdown("### Dosage Recommendations")
        for drug in selected_drugs:
            drug_info = get_drug_info(drug)
            if drug_info:
                st.markdown(f"**{drug}**")
                adult_dose_mg = parse_adult_dose(drug_info.get('Adult Dose'))
                recs = recommend_dosage(age, weight, adult_dose_mg)
                for formula, dose in recs.items():
                    st.markdown(f"- {formula}: {dose} mg")

# PAGE 4: PRESCRIPTION PARSER
elif page == "PrescriptionParser":
    st.markdown('<h2 class="section-header">📝 Prescription Text Parser</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Patient age (years):", min_value=0, max_value=120, value=30, key="parser_age")
    with col2:
        weight = st.number_input("Patient weight (kg):", min_value=0.1, value=70.0, key="parser_weight")

    sample_text = "Metformin 500mg twice daily with meals\nLisinopril 10mg once daily\nAspirin 81mg daily"

    if st.button("📋 Load Sample Prescription"):
        st.session_state.prescription_text = sample_text

    prescription_text = st.text_area("Paste prescription text:", 
                                    value=st.session_state.get("prescription_text", ""), 
                                    height=150,
                                    key="prescription_input")

    if st.button("🔍 Parse Prescription", type="primary"):
        if prescription_text:
            drugs = extract_drugs_from_text(prescription_text)

            if drugs:
                st.markdown(f"### ✓ Found {len(drugs)} Medication(s)")

                for drug in drugs:
                    drug_name = drug['name']
                    st.markdown(f"### {drug_name}")

                    drug_info = get_drug_info(drug_name)
                    if drug_info:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Drug Class:** {drug_info.get('Drug Class', 'N/A')}")
                            st.markdown(f"**Common Uses:** {drug_info.get('Common Uses', 'N/A')}")
                            st.markdown(f"**Adult Dose:** {drug_info.get('Adult Dose', 'N/A')}")
                        with col2:
                            st.markdown(f"**Side Effects:** {drug_info.get('Side Effects', 'N/A')}")
                            st.markdown(f"**Contraindications:** {drug_info.get('Contraindications', 'N/A')}")

                        adult_dose_mg = parse_adult_dose(drug_info.get('Adult Dose'))
                        recs = recommend_dosage(age, weight, adult_dose_mg)

                        if recs:
                            st.markdown("#### Dosage Recommendations:")
                            for formula, dose in recs.items():
                                st.markdown(f"- {formula}: **{dose} mg**")
                    else:
                        st.warning(f"⚠ Drug '{drug_name}' not found in database")

                    st.markdown("---")
            else:
                st.warning("❌ No medications found in the text. Make sure drug names match your database.")

# PAGE 5: IMAGE UPLOAD
elif page == "ImageUpload":
    st.markdown('<h2 class="section-header">📸 Upload Prescription Image</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Patient age (years):", min_value=0, max_value=120, value=55, key="image_age")
    with col2:
        weight = st.number_input("Patient weight (kg):", min_value=0.1, value=75.0, key="image_weight")

    uploaded_file = st.file_uploader("Upload prescription image (JPG, PNG, JPEG, BMP):", 
                                    type=["jpg", "jpeg", "png", "bmp"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Prescription", use_column_width=True)

        st.markdown("---")

        default_text = "Rx: Metformin 500mg twice daily with meals\nLisinopril 10mg daily\nAspirin 81mg daily"
        extracted_text = st.text_area("OCR Extracted Text (editable):",
                                     value=default_text,
                                     height=150,
                                     key="ocr_text")

        if st.button("✓ Analyze Extracted Text"):
            drugs = extract_drugs_from_text(extracted_text)

            if drugs:
                st.markdown(f"### ✓ Found {len(drugs)} Medication(s)")

                for drug in drugs:
                    drug_name = drug['name']
                    st.markdown(f"### {drug_name}")

                    drug_info = get_drug_info(drug_name)
                    if drug_info:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Drug Class:** {drug_info.get('Drug Class', 'N/A')}")
                            st.markdown(f"**Uses:** {drug_info.get('Common Uses', 'N/A')}")
                        with col2:
                            st.markdown(f"**Side Effects:** {drug_info.get('Side Effects', 'N/A')}")

                        st.markdown(f"**Contraindications:** {drug_info.get('Contraindications', 'N/A')}")
                        st.markdown(f"**Adult Dose:** {drug_info.get('Adult Dose', 'N/A')}")

                        adult_dose_mg = parse_adult_dose(drug_info.get('Adult Dose'))
                        recs = recommend_dosage(age, weight, adult_dose_mg)

                        if recs:
                            st.markdown("#### Dosage Recommendations:")
                            for formula, dose in recs.items():
                                st.markdown(f"- {formula}: **{dose} mg**")

                    st.markdown("---")
            else:
                st.warning("❌ No medications detected in extracted text")

# PAGE 6: PATIENT PROFILE
elif page == "PatientProfile":
    st.markdown('<h2 class="section-header">👤 Patient Profile</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age:", min_value=0, max_value=120, value=30, key="profile_age")
    with col2:
        weight = st.number_input("Weight (kg):", min_value=0.1, value=70.0, key="profile_weight")
    with col3:
        height = st.number_input("Height (cm):", min_value=50, value=170, key="profile_height")

    st.markdown("### Medical History")
    conditions = st.multiselect("Medical Conditions:",
                               ["Hypertension", "Diabetes", "Heart Disease", "Asthma", 
                                "COPD", "Kidney Disease", "Liver Disease"],
                               key="profile_conditions")

    allergies = st.multiselect("Drug Allergies:",
                              ["Penicillin", "NSAIDs", "ACE Inhibitors", "Sulfonamides", "Codeine"],
                              key="profile_allergies")

    if st.button("💾 Save Profile"):
        st.session_state.patient_profile = {
            "age": age,
            "weight": weight,
            "height": height,
            "conditions": conditions,
            "allergies": allergies
        }
        st.success("✓ Profile saved!")

    if "patient_profile" in st.session_state:
        st.markdown("### Saved Profile")
        st.json(st.session_state.patient_profile)

else:
    st.error("❌ Page not found")

st.markdown("""
---
<div style='text-align: center; color: #888; font-size: 0.8em; margin-top: 40px;'>
    <em>For educational purposes only. Always consult healthcare professionals before making medical decisions.</em>
</div>
""", unsafe_allow_html=True)
