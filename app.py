from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import stego_image
import stego_audio
import stego_qr

# Flask App Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

UPLOAD_FOLDER = "static/uploads"

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('home'))

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash("Email already exists!", "danger")
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful! You can now log in.", "success")
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home Route
@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

# Image Steganography Route
@app.route('/image_stego', methods=['GET', 'POST'])
@login_required
def image_stego_route():
    success_hide = False
    success_extract = False
    extracted_message = ""
    output_image = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "hide":
            if 'image' not in request.files:
                flash("No image selected!", "danger")
                return redirect(request.url)

            image_file = request.files['image']
            secret_text = request.form.get('message')

            if image_file.filename == '':
                flash("No file selected!", "danger")
                return redirect(request.url)

            input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
            output_image = os.path.join(app.config['UPLOAD_FOLDER'], "stego_image.png")
            image_file.save(input_image_path)

            stego_image.hide_text_in_image(input_image_path, secret_text, output_image)
            flash("Message hidden successfully!", "success")
            success_hide = True

        elif action == "extract":
            if 'image' not in request.files:
                flash("No image selected!", "danger")
                return redirect(request.url)

            image_file = request.files['image']
            input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
            image_file.save(input_image_path)

            extracted_message = stego_image.extract_text_from_image(input_image_path)
            success_extract = True

    return render_template(
        'image_stego.html', 
        success_hide=success_hide, 
        success_extract=success_extract, 
        extracted_message=extracted_message,
        output_image=output_image
    )

# Audio Steganography Route
@app.route('/audio_stego', methods=['GET', 'POST'])
@login_required
def audio_stego_route():
    output_audio = None
    extracted_message = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "hide":
            if 'audio' not in request.files:
                flash("No file selected!", "danger")
                return redirect(request.url)

            audio_file = request.files['audio']
            secret_text = request.form.get('message')

            if audio_file.filename == '':
                flash("No file selected!", "danger")
                return redirect(request.url)

            input_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(audio_file.filename))
            output_audio = os.path.join(app.config['UPLOAD_FOLDER'], "stego_audio.wav")
            audio_file.save(input_audio_path)

            stego_audio.hide_text_in_audio(input_audio_path, secret_text, output_audio)
            flash("Message hidden successfully!", "success")

        elif action == "extract":
            if 'audio' not in request.files:
                flash("No file selected!", "danger")
                return redirect(request.url)

            audio_file = request.files['audio']
            input_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(audio_file.filename))
            audio_file.save(input_audio_path)

            extracted_message = stego_audio.extract_text_from_audio(input_audio_path)
            flash("Message extracted successfully!", "success")

    return render_template('audio_stego.html', output_audio=output_audio, extracted_message=extracted_message)

# QR Code Steganography Route
@app.route('/qr_stego', methods=['GET', 'POST'])
@login_required
def qr_stego_route():
    output_qr_path = os.path.join(UPLOAD_FOLDER, "stego_qr.png")

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "hide":
            secret_message = request.form.get('message')

            # Generate and save QR Code
            qr = qrcode.make(secret_message)
            qr.save(output_qr_path)

            return render_template('qr_stego.html', output_qr="uploads/stego_qr.png")

        elif action == "extract":
            if 'qr_code' not in request.files:
                flash("No file selected!", "danger")
                return redirect(request.url)

            qr_file = request.files['qr_code']
            qr_file_path = os.path.join(UPLOAD_FOLDER, "uploaded_qr.png")
            qr_file.save(qr_file_path)

            # Decode QR Code
            from pyzbar.pyzbar import decode
            from PIL import Image

            decoded_data = decode(Image.open(qr_file_path))
            result = decoded_data[0].data.decode("utf-8") if decoded_data else "No hidden message found."

            return render_template('qr_stego.html', result=result)

    return render_template('qr_stego.html')

@app.route('/download_qr')
@login_required
def download_qr():
    output_qr_path = os.path.join(UPLOAD_FOLDER, "stego_qr.png")

    if os.path.exists(output_qr_path):
        return send_file(output_qr_path, as_attachment=True)
    else:
        flash("QR code not found!", "danger")
        return redirect(url_for('qr_stego_route'))

# Run App
if __name__ == "__main__":
    app.run(debug=True)
