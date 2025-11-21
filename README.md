# PDCQ4-Srikanth
FormulaQ Solutions company task
# Flask Google OAuth Login App

This is a simple Flask application that allows users to log in using their **Google Account**.  
The project uses Google's OAuth 2.0 API to authenticate users and fetch basic profile details.

---

## 🚀 Features

- Google OAuth 2.0 login
- Fetch user profile: name, email, profile picture
- Secure OAuth token handling
- Logout support
- Easy to deploy on any server

---

## 📦 Tech Stack

- Python (Flask)
- Google OAuth API
- Requests
- OAuthLib
- dotenv for environment variables

---

## 📁 Folder Structure
/project
│── app.py
│── client_secret.json (Google OAuth Credentials)
│── requirements.txt
└── README.md

## 🔧 Setup Instructions

### 1️⃣ Clone this repository

```bash
git clone https://github.com/chebrolusrikanth/PDCQ4-Srikanth.git
cd project

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Set up Google OAuth Credentials

Go to Google Cloud Console:

Create a project

Enable Google OAuth Consent Screen

Create OAuth 2.0 credentials (Web application)

Add authorized redirect URI:http://localhost:5000/callback

### 4️⃣ Run the Flask App
python app.py