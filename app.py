from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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
            image_path = request.files['image']
            secret_text = request.form.get('message')
            output_image = "static/stego_image.png"  # Save inside static folder

            if image_path:
                image_path.save(output_image)
                stego_image.hide_text_in_image(output_image, secret_text, output_image)
                success_hide = True

        elif action == "extract":
            image_path = request.files['image']
            if image_path:
                image_path.save("static/temp_extract.png")
                extracted_message = stego_image.extract_text_from_image("static/temp_extract.png")
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
    result = None
    if request.method == 'POST':
        action = request.form.get('action')
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                if action == "hide":
                    secret_text = request.form.get('message')
                    output_audio = os.path.join(app.config['UPLOAD_FOLDER'], "stego_audio.wav")
                    result = stego_audio.hide_text_in_audio(file_path, secret_text, output_audio)
                elif action == "extract":
                    result = stego_audio.extract_text_from_audio(file_path)
    
    return render_template('audio_stego.html', result=result)

# QR Code Steganography Route
@app.route('/qr_stego', methods=['GET', 'POST'])
@login_required
def qr_stego_route():
    result = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == "hide":
            message = request.form.get('message')
            output_qr = os.path.join(app.config['UPLOAD_FOLDER'], "qr_code.png")
            result = stego_qr.generate_qr(message, output_qr)
        elif action == "extract":
            if 'file' in request.files:
                file = request.files['file']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    result = stego_qr.decode_qr(file_path)
    
    return render_template('qr_stego.html', result=result)

# Run App
if __name__ == "__main__":
    app.run(debug=True)
