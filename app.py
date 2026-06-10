import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
from pypdf import PdfReader
from docx import Document

# 1. SETUP & CONFIG
st.set_page_config(page_title="Citation Proof Pro", layout="wide")

# 2. OPTIMIZED AUDIT FUNCTION
@st.cache_data(show_spinner=False)
def get_contextual_fit_analysis(context_paragraph, reference_content):
    """
    Forensic audit using 6-point verification schema.
    Uses 'gemini-1.5-flash' for high-speed performance.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an academic forensic auditor. Compare the provided Body Text excerpt and the cited Reference for factual consistency.

    1. Body Text: "{context_paragraph}"
    2. Reference: "{reference_content}"

    Audit the following 6 core data points:
    1. Study Sites: Do the hospitals match?
    2. Methodology: Does the study design/type match?
    3. Sample Size: Does the 'n' match?
    4. Study Year: Do the timeframes match?
    5. Objectives: Do the study goals align?
    6. Abstract Context: Does the reference abstract support the body text's claim?

    Output the result in the following JSON format:
    {{
        "Status": "ALIGNED" or "MISMATCH",
        "Discrepancies": ["list any specific failures here or 'None'"],
        "Reasoning": "One sentence explanation."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(json_text)
        return {
            "status": data.get("Status", "MISMATCH"),
            "discrepancies": data.get("Discrepancies", []),
            "reasoning": data.get("Reasoning", "Could not parse audit.")
        }
    except Exception:
        return {"status": "MISMATCH", "discrepancies": ["Parsing Error"], "reasoning": "API failed to return valid JSON."}

# 3. STREAMLIT UI LOGIC (Skeleton)
def main():
    st.title("Citation Proof Pro")
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        
        # ... [Your logic to load files / extract data] ...
        
        # Example of the optimized call (Line 351 replacement)
        if st.button("Run Audit"):
            # Ensure your loop iterates through citations
            result = get_contextual_fit_analysis(combined_context, abstract_text)
            
            # Display results using the 'stretch' fix
            status = result.get("status")
            reason = result.get("reasoning")
            
            st.write(f"Status: {status}")
            st.write(f"Reasoning: {reason}")
            
            # Using the new 'stretch' width
            st.dataframe(flagged_df, width='stretch', hide_index=True)

if __name__ == "__main__":
    main()