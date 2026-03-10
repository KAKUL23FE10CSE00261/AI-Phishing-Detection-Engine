# AI-Phishing-Detection-Engine
An intelligent AI-powered phishing email detection system that analyzes email content and determines whether it is Safe or Phishing.
The project combines Transformer-based NLP models, heuristic filtering, database logging, and interactive UI dashboards to provide a complete cybersecurity analysis tool.

This project demonstrates the practical application of Artificial Intelligence in Cybersecurity, helping users identify phishing attempts and understand the reasons behind the detection.

##🚀 Features
-🔍 AI-Powered Email Detection using DistilBERT
-🧠 Transformer NLP Model for phishing classification
-⚡ Hybrid Detection System
     -AI Model Prediction
     -Heuristic Rules
-🖥 Interactive Desktop UI (Tkinter)
-📊 Security Analytics Dashboard
-🧾 Prediction History Logging
-🤖 AI Analyst Explanation using Google Gemini
-📈 Threat Trend Visualization
-🗄 SQLite Database Storage

#🧠 AI Model
The system uses a pretrained transformer model for phishing detection.

Model Used:
DistilBERT Phishing Email Detection
cybersectony/phishing-email-detection-distilbert_v2.1

Technology Stack:
-HuggingFace Transformers
-Natural Language Processing (NLP)
-Binary Text Classification

Output:
Input: Email Text
Output: 
   - Safe
   - Phishing
Confidence score is also generated.

## 🏗 System Architecture
User Email Input
        │
        ▼
AI Phishing Detection Model (DistilBERT)
        │
        ▼
Prediction Engine
        │
        ├── Safe
        └── Phishing
                │
                ▼
AI Forensic Analyst (Gemini API)
                │
                ▼
Threat Explanation
All predictions are stored in SQLite Database for analytics and history tracking.

## 🖥 User Interface
The system includes a modern Tkinter desktop interface with:
-Email input area
-Scan button
-Detection result
-Confidence score
-Prediction history
-Analytics dashboard
-Threat explanation window
Users can also:
-Clear input
-Wipe logs
-View analytics dashboard

## 📊 Analytics Dashboard
The dashboard displays:
1️⃣ Detection Distribution (Pie Chart)
-Safe Emails
-Phishing Emails
2️⃣ Threat Trends Over Time
-Daily phishing detection statistics
Libraries used:
Matplotlib
-Tkinter
-SQLite

## 📂 Project Structure
AI-Phishing-Detection-Engine
│
├── main.py
├── model.py
├── analyst.py
├── database.py
├── ui.py
│
├── phishing_demo.py
│
├── history.db
│
└── README.md

## 📜 File Description
1- main.py
Main application entry point that initializes:
-AI model
-Database
-Analyst module
-User interface

2- model.py
Handles AI phishing prediction using DistilBERT.
Responsibilities:
-Load transformer model
-Perform text classification
-Return prediction and confidence score

3- analyst.py
Provides AI forensic analysis using Google Gemini API.
It generates:
-A 3-point explanation
-Why the email is phishing or safe

4- database.py
Manages SQLite database operations.
Features:
-Store predictions
-Fetch history
-Generate statistics
-Track phishing trends

5- ui.py
Creates the desktop interface using Tkinter.
Includes:
-Email scanner
-Prediction result display
-History table
-Dashboard visualization
-AI forensic analysis window

6- phishing_demo.py
A Streamlit-based demo version of the phishing detection system.
Features:
-Email classification
-AI explanation
-Prediction history
-Manual feedback system

## ⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/AI-Phishing-Detection-Engine.git
cd AI-Phishing-Detection-Engine

2️⃣ Install dependencies
pip install -r requirements.txt
Required libraries include:
  transformers
  torch
  streamlit
  scikit-learn
  pandas
  matplotlib
  sqlite3
  google-genai
  joblib
  scipy

3️⃣ Add Gemini API Key
In main.py
Replace:
API_KEY = "YOUR_API_KEY"

## ▶️ Running the Project
Run the desktop application:
  python main.py
Run the Streamlit demo:
  streamlit run phishing_demo.py

## 🧪 Example
Input Email:
  Urgent: Verify your account now or it will be suspended. Click here to fix.
Output:
  ⚠️ Phishing Detected
   Confidence: 0.94
AI Explanation:
  • The email uses urgent language to pressure the recipient.
  • It requests account verification through a suspicious link.
  • These are common phishing tactics used to steal credentials.  


## 🔮 Future Improvements
-URL phishing detection
-Attachment malware scanning
-Browser extension integration
-Real-time email monitoring
-Deep learning ensemble models
-Threat intelligence integration

## 📚 Technologies Used
  Python
  NLP
  HuggingFace Transformers
  DistilBERT
  Tkinter
  Streamlit
  SQLite
  Matplotlib
  Google Gemini API
