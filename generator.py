# =========================================
# ENGLISH REPORT COMMENT GENERATOR - Streamlit Version
# Supports Year 7 and Year 8
# =========================================

import random
import streamlit as st
from docx import Document

# ---------- IMPORT STATEMENT BANKS ----------
import statements_year7 as s7
import statements_year8 as s8

# Map years to their banks
year_banks = {
    "Year 7": s7,
    "Year 8": s8
}

# ---------- SETTINGS ----------
TARGET_CHARS = 499  # character limit for comment

# ---------- HELPERS ----------
def get_pronouns(gender):
    gender = gender.lower()
    if gender == "male":
        return "he", "his"
    elif gender == "female":
        return "she", "her"
    return "they", "their"

def lowercase_first(text):
    return text[0].lower() + text[1:] if text else ""

def truncate_comment(comment, target=TARGET_CHARS):
    if len(comment) <= target:
        return comment
    truncated = comment[:target].rstrip(" ,;.")
    if "." in truncated:
        truncated = truncated[:truncated.rfind(".")+1]
    return truncated

def generate_comment(name, att, read, write, read_t, write_t, pronouns, banks, attitude_target=None):
    p, p_poss = pronouns

    opening = random.choice(banks.opening_phrases)
    attitude_sentence = f"{opening} {name} {banks.attitude_bank[att]}."
    reading_sentence = f"In reading, {p} {banks.reading_bank[read]}."
    writing_sentence = f"In writing, {p} {banks.writing_bank[write]}."
    reading_target_sentence = f"For the next term, {p} should {lowercase_first(banks.reading_target_bank[read_t])}."
    writing_target_sentence = f"Additionally, {p} should {lowercase_first(banks.writing_target_bank[write_t])}."

    # optional attitude next steps
    attitude_target_sentence = f" {lowercase_first(attitude_target)}" if attitude_target else ""

    closer_sentence = random.choice(banks.closer_bank)

    comment_parts = [
        attitude_sentence + attitude_target_sentence,
        reading_sentence,
        writing_sentence,
        reading_target_sentence,
        writing_target_sentence,
        closer_sentence
    ]

    comment = " ".join(comment_parts)
    comment = truncate_comment(comment, TARGET_CHARS)
    return comment

# ---------- STREAMLIT APP ----------
st.title("English Report Comment Generator (~499 chars)")

st.markdown(
    "Fill in the student details and click **Generate Comment**. You can add multiple students before downloading the full report."
)

# Session state to store all generated comments
if 'all_comments' not in st.session_state:
    st.session_state['all_comments'] = []

with st.form("report_form"):
    year = st.selectbox("Select Year", ["Year 7", "Year 8"])
    name = st.text_input("Student Name")
    gender = st.selectbox("Gender", ["Male", "Female"])
    att = st.selectbox("Attitude band", [90,85,80,75,70,65,60,55,40,0])
    read = st.selectbox("Reading achievement band", [90,85,80,75,70,65,60,55,40,0])
    write = st.selectbox("Writing achievement band", [90,85,80,75,70,65,60,55,40,0])
    read_t = st.selectbox("Reading target band", [90,85,80,75,70,65,60,55,40,0])
    write_t = st.selectbox("Writing target band", [90,85,80,75,70,65,60,55,40,0])

    # optional attitude next steps
    attitude_target = st.text_input("Optional Attitude Next Steps")

    submitted = st.form_submit_button("Generate Comment")

if submitted and name:
    pronouns = get_pronouns(gender)
    banks = year_banks[year]
    comment = generate_comment(name, att, read, write, read_t, write_t, pronouns, banks, attitude_target)
    char_count = len(comment)

    st.text_area("Generated Comment", comment, height=200)
    st.write(f"Character count (including spaces): {char_count} / {TARGET_CHARS}")

    # Save comment
    st.session_state['all_comments'].append(f"{name}: {comment}")

    if st.button("Add Another Comment"):
        st.experimental_rerun()

# ---------- DOWNLOAD FULL REPORT ----------
if st.session_state['all_comments']:
    if st.button("Download Full Report (Word)"):
        doc = Document()
        for c in st.session_state['all_comments']:
            doc.add_paragraph(c)
        file_name = "English_Report_Comments.docx"
        doc.save(file_name)
        with open(file_name, "rb") as f:
            st.download_button(
                label="Download Word File",
                data=f,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# ---------- SHOW ALL COMMENTS SO FAR ----------
if st.session_state['all_comments']:
    st.markdown("### All Generated Comments:")
    for c in st.session_state['all_comments']:
        st.write(c)
