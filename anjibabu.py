import streamlit as st
from supabase import create_client, Client
import pandas as pd

# ---------------------------------
# Supabase Direct Connection
# ---------------------------------
SUPABASE_URL = "https://bidqmjsfyjizhttcjkol.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpZHFtanNmeWppemh0dGNqa29sIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjcxMzE4NSwiZXhwIjoyMDc4Mjg5MTg1fQ.x12d46OLujL3O3DJ2ccAJFMglxLaU-8ka8hymMZUBjY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------------
# Streamlit App
# ---------------------------------
st.set_page_config(page_title="Student Marks Dashboard", layout="wide")
st.title("🎓 Student Marks Analysis Dashboard")

# --- Form to Add Students ---
st.subheader("📝 Add Student Record")

col1, col2 = st.columns(2)
with col1:
    roll_no = st.text_input("Roll Number")
    name = st.text_input("Name")
with col2:
    math = st.number_input("Maths", 0, 100)
    english = st.number_input("English", 0, 100)
    science = st.number_input("Science", 0, 100)

if st.button("💾 Save Record"):
    avg = round((math + english + science) / 3, 2)
    data = {
        "roll_no": roll_no,
        "name": name,
        "math": math,
        "english": english,
        "science": science,
        "average_score": avg
    }
    response = supabase.table("students").insert(data).execute()
    if response.data:
        st.success("✅ Student record added successfully!")
    else:
        st.error("❌ Error adding record!")

# --- Display Records ---
st.subheader("📋 Student Records")
students = supabase.table("students").select("*").execute()
if students.data:
    df = pd.DataFrame(students.data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No records found yet.")

# --- Optional: Average Stats ---
if students.data:
    st.markdown("### 📊 Average Scores Summary")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Students", len(df))
    col_b.metric("Highest Average", df["average_score"].max())
    col_c.metric("Overall Average", round(df["average_score"].mean(), 2))
