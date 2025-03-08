from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from user_data import User_data

data = User_data()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Admin login check
    if username == "admin" and password == "password":
        session['user'] = 'admin'  # Storing session data
        return redirect(url_for('admin.home'))

    # Check user in database
    user = data.get_user(username, password)

    if user:
        session['user'] = username  # Store user in session
        return redirect(url_for('user.dashboard'))  # Redirect to user dashboard

    flash("Invalid credentials! Please try again.")
    return redirect(url_for('auth.index'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for('auth.index'))




@auth_bp.route('/signup', methods=['POST'])
def signup():
    email_ID = request.form.get("email")
    fname = request.form.get("first_name")
    lname = request.form.get("last_name")
    username = request.form.get("username")
    password = request.form.get("password")

    success = data.adder(email_ID, fname, lname, username, password)

    if success:
        flash("Signup successful! You can now log in.", "success")
        return redirect(url_for('auth.index'))
    else:
        flash("Username or Email already exists. Try a different one.", "error")
        return redirect(url_for('auth.index'))  # Redirect back to signup page
