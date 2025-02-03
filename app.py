from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Flask Configuration
app.secret_key = os.urandom(24)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "sahilbanerjee51@gmail.com"
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = "sahilbanerjee51@gmail.com"

mail = Mail(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit-form", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    subject = request.form.get("subject")
    phone = request.form.get("phone")

    # Validate form data
    if not name or not email or not message or not subject or not phone:
        flash("All fields are required. Please fill in all the fields before submitting.", "danger")
        return redirect('/#contact')

    # Compose Email
    msg = Message(f'New Contact Form (Portfolio): {subject}',
                  sender=email,
                  recipients=["sahilbanerjee51@gmail.com"])

    msg.body = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}

            Message:
            {message}
            """

    try:
        mail.send(msg)  # Directly send email using Flask-Mail (no need to call connect())
        flash("Your message has been sent successfully!", "success")
    except Exception as e:
        flash("Error sending message. Please try again later.", "danger")
        print(f"Email Error: {e}")  # Log the error for debugging

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)