from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from database import get_user, create_user, User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash("Invalid email or password.")
    
    return render_template('login.html')

@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if get_user(email):
            flash("Email already exists.")
        else:
            create_user(email, generate_password_hash(password))
            flash("Signup successful. Please login.")
            return redirect(url_for('auth.login'))

    return render_template('signup.html')
