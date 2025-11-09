import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Setup
# ---------------------------------
st.set_page_config(page_title="Student Marks Analysis Dashboard", layout="wide")
st.title("🎓 Student Marks Analysis Dashboard")

# ---------------------------------
# Data Storage (Session State)
# ---------------------------------
if "records" not in st.session_state:
    st.session_state.records = []

# ---------------------------------
# Data Entry Form
# ---------------------------------
st.subheader("📝 Enter Student Details")

with st.form("data_entry_form", clear_on_submit=True):
    col_a, col_b = st.columns(2)
    with col_a:
        roll = st.text_input("Roll Number") # Changed to Roll Number
        name = st.text_input("Student Name")

    with col_b:
        gender = st.selectbox("Gender", ["Male", "Female"])
        section = st.selectbox("Section", ["A", "B", "C", "D", "E", "F"]) # Changed to Section

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
        telugu = st.number_input("Telugu", 0, 100, 0) # Use Telugu instead of Lang2

    # Additional Factors
    parental_edu = st.selectbox("Parental Education", ["High School", "Some College", "Associate's", "Bachelor's", "Master's"])
    prep = st.selectbox("Test Preparation", ["Completed", "None"])

    add_record = st.form_submit_button("💾 Save Record")

# ---------------------------------
# Record Submission Logic
# ---------------------------------
if add_record:
    # Calculate average based on 6 subjects
    total_score = math + english + science + social + hindi + telugu
    average = round(total_score / 6, 2)

    new_record = {
        "Roll No": roll, 
        "Name": name, 
        "Gender": gender,
        "Section": section, 
        "Parental Education": parental_edu, 
        "Test Preparation": prep,
        "Math": math, 
        "English": english, 
        "Science": science, 
        "Social": social, 
        "Hindi": hindi, 
        "Telugu": telugu, 
        "Average Score": average
    }
    st.session_state.records.append(new_record)
    st.success(f"✅ Student '{name}' record saved successfully!")

# ---------------------------------
# Dashboard Display
# ---------------------------------
if len(st.session_state.records) > 0:
    df = pd.DataFrame(st.session_state.records)
    st.markdown("## 📊 Performance Analysis")

    # KPIs
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Students", len(df))
    kpi2.metric("Overall Avg Score", round(df["Average Score"].mean(), 2))
    kpi3.metric("Avg Math Score", round(df["Math"].mean(), 2))
    kpi4.metric("Highest Total Score", df["Average Score"].max())

    st.markdown("---")

    col_chart_1, col_chart_2, col_chart_3 = st.columns(3)

    # 1️⃣ Average Score by Section
    with col_chart_1:
        fig_section = px.bar(df.groupby("Section")["Average Score"].mean().reset_index(),
                           x="Section", y="Average Score", color="Section", 
                           title="Average Score by Section")
        st.plotly_chart(fig_section, use_container_width=True)

    # 2️⃣ Average Score by Parental Education
    with col_chart_2:
        fig_edu = px.bar(df.groupby("Parental Education")["Average Score"].mean().reset_index(),
                             x="Parental Education", y="Average Score", color="Parental Education", 
                             title="Average Score by Parental Education")
        st.plotly_chart(fig_edu, use_container_width=True)

    # 3️⃣ Gender Distribution of Average Score (Pie)
    with col_chart_3:
        fig_gender = px.pie(df, names="Gender", values="Average Score", title="Average Score by Gender")
        st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")
    
    # Top 5 Students Comparison
    top5 = df.nlargest(5, "Average Score")
    fig_top = px.bar(top5, x="Name", y=["Math", "English", "Science", "Social", "Hindi", "Telugu"],
                     title="Top 5 Students: Subject-wise Breakdown", barmode="group",
                     height=400)
    st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("### 📋 Detailed Records")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No student records added yet. Please use the form above to input data. ⬆️")
