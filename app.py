import streamlit as st
import json
from src.rag_engine import run_query

st.set_page_config(page_title="PRA Regulatory Assistant", layout="wide")

st.title("AI Regulatory Assistant (COREP)")
st.markdown("### UK Prudential Regulation Authority (PRA) Compliance Tool")
st.warning("""
**Disclaimer:** The answers provided are solely based on the **PRA Rulebook 2025** and **Annex II Instructions**. 
While this AI uses advanced reasoning to map regulations, it **may not** always generate 100% accurate values. 
**Always double-check outputs against official technical standards before any regulatory submission.**
""")

with st.sidebar:
    st.header("Financial Scenario")
    user_input = st.text_area(
        "Enter bank financial details:",
        placeholder="e.g. The bank has £500m in CET1 instruments and £50m in goodwill...",
        height=200
    )
    submit_button = st.button("Generate Report")

if submit_button and user_input:
    with st.spinner("Analyzing PRA Rulebook and generating report..."):
        try:
            raw_response = run_query(user_input)
            
            clean_json = raw_response.replace("```json", "").replace("```", "").strip()
            report_data = json.loads(clean_json)

            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("COREP CA1 Report Extract")
                st.table(report_data.get("rows", []))
            
            with col2:
                st.subheader("Audit Log & Justification")
                for row in report_data.get("rows", []):
                    with st.expander(f"Row {row['row']}: {row['label']}"):
                        st.write(f"**Value:** {row['value']}")
                        st.write(f"**Source Reference:** {row['source_ref']}")
                        if "reasoning" in row:
                            st.info(row["reasoning"])

            st.divider()
            with st.expander("View Raw Structured JSON"):
                st.json(report_data)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Check if you have run 'python src/ingest.py' first!")
else:
    st.info("<-- Enter a financial scenario in the sidebar to begin.")