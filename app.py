from flask import Flask, render_template, request, redirect, flash
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure app
app.config['SECRET_KEY'] = 'ajwaqas12345'

# Get email credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Print debug info
print("\nDEBUG INFORMATION:")
print(f"Email Address: {EMAIL_ADDRESS}")
print(f"Password Length: {len(EMAIL_PASSWORD) if EMAIL_PASSWORD else 'No password found'}")

# Projects data
projects = [
    {
        "name": "Diabetes Prediction System",
        "desc": "A machine learning-based system that predicts diabetes using health data.",
        "link": "https://github.com/Waqas-110/diabetes-prediction.git"
    },
    {
        "name": "Personal Voice Assistant",
        "desc": "An AI-powered voice assistant that performs tasks based on voice commands.",
        "link": "https://github.com/Waqas-110/personal-voice-assistant.git"
    },
    {
        "name": "YouExcel Management System",
        "desc": "A Django-based platform for managing college courses, staff, and students.",
        "link": "https://github.com/Waqas-110/Collage_Managment_System.git"
    }
]

@app.route("/")
def index():
    return render_template("index.html", projects=projects, year=datetime.now().year)

@app.route("/contact", methods=["POST"])
def contact():
    print("\nDEBUG: Starting contact form submission")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("ERROR: Missing email configuration")
        flash("Email configuration is missing. Please contact administrator.", "danger")
        return redirect("/")

    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    msg = EmailMessage()
    msg['Subject'] = 'New Contact Message from Portfolio'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage:\n{message}")

    try:
        print("Attempting SMTP connection...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            print("Connected to SMTP server")
            print(f"Attempting login with {EMAIL_ADDRESS}")
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("Login successful")
            smtp.send_message(msg)
            print("Message sent successfully")
        flash("Message sent successfully!", "success")
    except Exception as e:
        print(f"ERROR DETAILS: {str(e)}")
        flash("Message failed to send. Please try again later.", "danger")

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)