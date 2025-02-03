from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

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
    if not name or not email or not message or not subject or not phone:
        flash("All fields are required. Please fill in all the fields before submitting.", "danger")
        return redirect('/#contact')
    else:
        # Compose Email
        msg = Message(f'New Contact Form (Portfolio): {subject}',
                      sender=email,
                      recipients=[os.getenv('MAIL_USERNAME')])

        msg.body = f"""
                Name: {name}
                Email: {email}
                Phone: {phone}
                Subject: {subject}
    
                Message:
                {message}
                """
        with mail.connect() as conn:
            conn.send(msg)

        try:
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash("Error sending message. Please try again later.", "danger")
            print(f"Email Error: {e}")  # Debugging

        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)