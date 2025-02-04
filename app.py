from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


load_dotenv()


app.secret_key = os.urandom(24)


app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)

db = SQLAlchemy(app)
@app.route("/")
def home():
    return render_template("index.html")
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Message {self.name}>'
with app.app_context():
    db.create_all()

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
    new_message = ContactMessage(name=name, email=email, phone=phone, subject=subject, message=message)
    db.session.add(new_message)
    db.session.commit()
    # Compose Email
    msg = Message(f'New Contact Form (Portfolio): {subject}',
                  sender=email,
                  recipients=[os.environ.get('MAIL_DEFAULT_SENDER')])

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