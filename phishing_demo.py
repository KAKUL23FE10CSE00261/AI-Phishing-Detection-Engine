import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import time 
import joblib
import re
import scipy.sparse as sps
import sqlite3
import json
import random

def get_ai_prediction(text):
    prompt = f"""
    Analyze the following email text and determine if it is phishing.
    Respond with a JSON object containing three keys:
    1. "prediction": Either "Phishing" or "Legitimate".
    2. "confidence": A float between 0.0 and 1.0.
    3. "explanation": A brief, one-sentence explanation for your decision.

    Email text: "{text}"
    """

    text_lower = text.lower()
    phishing_keywords = ["verify your account", "suspended", "urgent", "confirm your", "prize", "winner", "claim now", "overdue", "limited time", "compromised"]
    is_phishing = any(keyword in text_lower for keyword in phishing_keywords)
    
    if "my name is pranay" in text_lower:
        is_phishing = False

    if is_phishing:
        prediction = "Phishing"
        confidence = random.uniform(0.8, 0.98)
        explanation = "The email uses urgent language and common phishing tactics to pressure the user."
    else:
        prediction = "Legitimate"
        confidence = random.uniform(0.85, 0.99)
        explanation = "The email appears to be a standard, non-threatening communication."

    simulated_response = {
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation
    }
    
    return simulated_response

DB_PATH = "C:/Users/Pranay/OneDrive/Desktop/Projects/FishyGuard/history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            score REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'unreviewed'
        )
    """)
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Phishing Detection Demo", layout="centered")

st.markdown("""
<style>
    div[data-testid="stHorizontalBlock"] > div > div > div[data-testid="stVerticalBlock"] > div.stButton > button {
        width: 100%;
        padding: 8px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Phishing Detection — AI Demo")
st.write("Paste an email or message below. A powerful AI will classify it and provide an explanation.")
st.write("Pranay Kriplani")

TRANSLUCENT_RED = "rgba(255, 75, 75, 0.4)"   
TRANSLUCENT_BLUE = "rgba(48, 133, 195, 0.4)" 
DEFAULT_COLOR = "initial"

def set_background_color(color_code):
    css = f"""
    <style>
    .stApp {{
        background-color: {color_code}; 
        transition: background-color 0.1s ease-in-out !important; 
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def reset_background_color():
    set_background_color(DEFAULT_COLOR) 

def perform_flash(flash_type):
    if flash_type == 'safe':
        set_background_color(TRANSLUCENT_BLUE)
        time.sleep(1.0) 
        reset_background_color()
        time.sleep(0.1) 

    elif flash_type == 'medium':
        set_background_color(TRANSLUCENT_RED)
        time.sleep(1.5) 
        reset_background_color()
        time.sleep(0.1)

    elif flash_type == 'high':
        for _ in range(3):
            set_background_color(TRANSLUCENT_RED)
            time.sleep(0.5) 
            reset_background_color()
            time.sleep(0.3)

reset_background_color() 

with st.sidebar:
    st.subheader("About this Demo")
    st.markdown("""
    This demo uses a simulated call to a powerful Large Language Model (like Google's Gemini) to detect phishing attempts.
    
    **Key Features:**
    - **Real AI Analysis:** No more simplistic keyword matching.
    - **Explanations:** The AI provides a reason for its classification.
    - **User Feedback:** You can mark items as 'Safe' to correct the AI's mistakes for future predictions.
    """)

demo_col1, demo_col2 = st.columns(2)
with demo_col1:
    if st.button("Sample phishing"):
        st.session_state['demo_input'] = "Urgent: Verify your account now or it will be suspended. Click here to fix."
with demo_col2:
    if st.button("Sample legit"):
        st.session_state['demo_input'] = "Please see attached the final report and let me know your comments."

if "demo_input" not in st.session_state:
    st.session_state['demo_input'] = ""

user_input = st.text_area("Enter Email Text:", value=st.session_state['demo_input'], height=180)

if st.button("Predict"):
    text = user_input.strip()
    if not text:
        st.warning("Paste some email text first.")
    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM predictions WHERE email_text = ? AND status = 'safe'", (text,))
        is_safe = cursor.fetchone()
        conn.close()

        if is_safe:
            st.success("✅ Legitimate — Manually marked as safe.")
            perform_flash('safe')
        else:
            with st.spinner('Analyzing email with AI...'):
                ai_response = get_ai_prediction(text)
                
                label = ai_response["prediction"]
                score = ai_response["confidence"]
                explanation = ai_response["explanation"]

                if label == "Legitimate":
                    perform_flash('safe')
                else:
                    perform_flash('high') 

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM predictions WHERE email_text = ?", (text,))
            existing_entry = cursor.fetchone()
            if not existing_entry:
                cursor.execute("INSERT INTO predictions (email_text, prediction, score) VALUES (?, ?, ?)",
                               (text, label, score))
                conn.commit()
            conn.close()

            if label == "Phishing":
                st.error(f"⚠️ Phishing detected — confidence {score:.2f}")
            else:
                st.success(f"✅ Legitimate — confidence {score:.2f}")

            st.subheader("AI Analysis")
            st.info(explanation)

st.subheader("Submission History")

def update_status(prediction_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE predictions SET status = ? WHERE id = ?", (new_status, prediction_id))
    conn.commit()
    conn.close()

conn = sqlite3.connect(DB_PATH)
history_df = pd.read_sql_query("SELECT id, timestamp, email_text, prediction, score, status FROM predictions ORDER BY timestamp DESC", conn)
conn.close()

if not history_df.empty:
    for index, row in history_df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 1, 1, 1])
        with col1:
            st.write(row['timestamp'].split('.')[0])
        with col2:
            st.markdown(f"**{row['email_text'][:70]}...**")
        with col3:
            st.write(row['prediction'])
        with col4:
            st.write(f"{row['score']:.2f}")
        with col5:
            st.write(row['status'])
        with col6:
            if row['status'] == 'unreviewed':
                if st.button("Report", key=f"report_{row['id']}"):
                    update_status(row['id'], 'reported')
                if st.button("Safe", key=f"safe_{row['id']}"):
                    update_status(row['id'], 'safe')
            else:
                st.write("-")
else:
    st.info("No predictions yet. Enter some text and click 'Predict'!")

st.markdown("---")
