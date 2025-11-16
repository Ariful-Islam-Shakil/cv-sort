import streamlit as st
import pandas as pd
import os
from root import pipeline

# -------------------- Streamlit App --------------------
st.set_page_config(page_title="CV Sorter", page_icon="🧠", layout="wide")
st.title("🧠 Smart CV Sorting & Analysis Pipeline")

RESULTS_DIR = "./results"

with st.sidebar:
    st.header("⚙️ Configuration Panel")

    # Mode selection
    mode = st.radio("Choose Action", ["🔍 Run New Sorting", "📂 View Existing Results"])

    if mode == "🔍 Run New Sorting":
        # Inputs for pipeline
        folder = st.text_input(
            "📁 Folder Path (where CV files are stored)",
            "./AI-Intern-9-Nov-2025"
        )
        JDI = st.text_input("🆔 Job Description ID", "SE001")
        Department = st.text_input("🏢 Department Name", "Software_Engineering")
        output_version = st.text_input("📄 Output Version Tag", "v2")

        # 🆕 New input for job description text
        job_description = st.text_area(
            "📝 Job Description",
            placeholder="Paste the full job description here...",
            height=200
        )

        run_button = st.button("🚀 Start CV Sorting & Analysis")

    else:
        # Show existing CSV files
        csv_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".csv")]
        selected_csv = st.selectbox("📄 Select an existing result file", csv_files)
        load_button = st.button("📂 Load Selected CSV")

# -------------------- MAIN DISPLAY LOGIC --------------------
if mode == "🔍 Run New Sorting" and 'run_button' in locals() and run_button:
    if not job_description.strip():
        st.warning("⚠️ Please enter the job description before running the analysis.")
    else:
        st.info("⚙️ Running CV sorting pipeline... please wait ⏳")
        try:
            formatted_df = pipeline(folder, JDI, job_description, Department, output_version)
            st.success("✅ CV Sorting & Analysis completed successfully!")

            st.subheader("📊 Analyzed Candidate Data")
            st.dataframe(formatted_df, use_container_width=True)

            csv = formatted_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Analyzed CSV",
                data=csv,
                file_name=f"cv_analysis_{Department}_{output_version}.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"❌ Pipeline failed: {e}")

elif mode == "📂 View Existing Results" and 'load_button' in locals() and load_button:
    try:
        file_path = os.path.join(RESULTS_DIR, selected_csv)
        df = pd.read_csv(file_path)
        st.success(f"✅ Loaded file: {selected_csv}")
        st.dataframe(df, use_container_width=True)

        st.download_button(
            label="⬇️ Download This CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=selected_csv,
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"❌ Failed to load CSV: {e}")

else:
    st.info("👈 Use the sidebar to run a new CV sorting or open an existing result.")
