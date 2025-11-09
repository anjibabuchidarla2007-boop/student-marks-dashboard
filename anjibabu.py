import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client

# ---------------------------------
# Supabase Connection
# ---------------------------------
url = st.secrets["https://bidqmjsfyjizhttcjkol.supabase.co"]
key = st.secrets["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpZHFtanNmeWppemh0dGNqa29sIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjcxMzE4NSwiZXhwIjoyMDc4Mjg5MTg1fQ.x12d46OLujL3O3DJ2ccAJFMglxLaU-8ka8hymMZUBjY"]
supabase: Client = create_client(url, key)

# ---------------------------------
# Page Setup
# ---------------------------------
st.set_page_config(page_title="Student Marks Analysis Dashboard", layout="wide")
st.title("🎓 Student Marks Analysis Dashboard")

# ---------------------------------
# Fetch Existing Records from Supabase
# ---------------------------------
if "records" not in st.session_state:
    data = supabase.table("students").select("*").execute()
    st.session_state.records = data.data if data.data else []

# ---------------------------------
# Data Entry Form
# ---------------------------------
st.subheader("📝 Enter Student Details")

with st.form("data_entry_form", clear_on_submit=True):
    col_a, col_b = st.columns(2)
    with col_a:
        roll = st.text_input("Roll Number")
        name = st.text_input("Student Name")

    with col_b:
        gender = st.selectbox("Gender", ["Male", "Female"])
        section = st.selectbox("Section", ["A", "B", "C", "D", "E", "F"])

    st.markdown("### Enter Marks (Out of 100)")
    c1, c2, c3 = st.columns(3)
    with c1:
        math = st.number_input("Maths", 0, 100, 0)
        english = st.number_input("English", 0, 100, 0)
    with c2:
        science = st.number_input("Science", 0, 100, 0)
        social = st.number_input("Social", 0, 100, 0)
    with c3:
        hindi = st.number_input("Hindi", 0, 100, 0)
        telugu = st.number_input("Telugu", 0, 100, 0)

    parental_edu = st.selectbox("Parental Education", ["High School", "Some College", "Associate's", "Bachelor's", "Master's"])
    prep = st.selectbox("Test Preparation", ["Completed", "None"])

    add_record = st.form_submit_button("💾 Save Record")

# ---------------------------------
# Save Record to Supabase
# ---------------------------------
if add_record:
    total_score = math + english + science + social + hindi + telugu
    average = round(total_score / 6, 2)

    new_record = {
        "roll_no": roll,
        "name": name,
        "gender": gender,
        "section": section,
        "parental_education": parental_edu,
        "test_preparation": prep,
        "math": math,
        "english": english,
        "science": science,
        "social": social,
        "hindi": hindi,
        "telugu": telugu,
        "average_score": average
    }

    response = supabase.table("students").insert(new_record).execute()
    if response.data:
        st.session_state.records.append(new_record)
        st.success(f"✅ Student '{name}' record saved to Supabase successfully!")
    else:
        st.error("❌ Failed to save record. Check your Supabase connection or table permissions.")

# ---------------------------------
# Dashboard Display
# ---------------------------------
if len(st.session_state.records) > 0:
    df = pd.DataFrame(st.session_state.records)
    st.markdown("## 📊 Performance Analysis")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Students", len(df))
    kpi2.metric("Overall Avg Score", round(df["average_score"].mean(), 2))
    kpi3.metric("Avg Math Score", round(df["math"].mean(), 2))
    kpi4.metric("Highest Total Score", df["average_score"].max())

    st.markdown("---")

    col_chart_1, col_chart_2, col_chart_3 = st.columns(3)

    with col_chart_1:
        fig_section = px.bar(df.groupby("section")["average_score"].mean().reset_index(),
                           x="section", y="average_score", color="section",
                           title="Average Score by Section")
        st.plotly_chart(fig_section, use_container_width=True)

    with col_chart_2:
        fig_edu = px.bar(df.groupby("parental_education")["average_score"].mean().reset_index(),
                         x="parental_education", y="average_score", color="parental_education",
                         title="Average Score by Parental Education")
        st.plotly_chart(fig_edu, use_container_width=True)

    with col_chart_3:
        fig_gender = px.pie(df, names="gender", values="average_score",
                            title="Average Score by Gender")
        st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")

    top5 = df.nlargest(5, "average_score")
    fig_top = px.bar(top5, x="name", y=["math", "english", "science", "social", "hindi", "telugu"],
                     title="Top 5 Students: Subject-wise Breakdown", barmode="group", height=400)
    st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("### 📋 Detailed Records")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No student records added yet. Please use the form above to input data. ⬆️")
