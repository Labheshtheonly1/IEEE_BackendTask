from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from user_data import User_data

data = User_data()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from Postman

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    # Admin login check
    if username == "admin" and password == "password":
        session['user'] = 'admin'
        return jsonify({"message": "Admin login successful!", "role": "admin"}), 200

    # Check user in database
    user = data.get_user(username, password)

    if user:
        session['user'] = username
        return jsonify({"message": "Login successful!", "role": "user"}), 200

    return jsonify({"error": "Invalid credentials! Please try again."}), 401


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for('auth.index'))




@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.is_json:  # Handling Postman JSON requests
            data_json = request.get_json()
            email_ID = data_json.get("email_ID")
            fname = data_json.get("fname")
            lname = data_json.get("lname")
            username = data_json.get("username")
            password = data_json.get("password")
        else:  # Handling Form Submission
            email_ID = request.form.get("email_ID")
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            username = request.form.get("username")
            password = request.form.get("password")

        # Debugging step
        print(email_ID, fname, lname, username, password)

        # Ensure no values are empty before proceeding
        if not all([email_ID, fname, lname, username, password]):
            if request.is_json:
                return jsonify({"error": "All fields are required!"}), 400
            flash("All fields are required!", "danger")
            return redirect(url_for('signup'))

        success = data.adder(email_ID, fname, lname, username, password)

        if success:
            if request.is_json:
                return jsonify({"message": "Signup successful! You can now log in."}), 201
            flash("Signup successful! You can now log in.", "success")
            return redirect(url_for('auth.index'))
        else:
            if request.is_json:
                return jsonify({"error": "User already exists!"}), 409
            flash("User already exists!", "danger")
            return redirect(url_for('signup'))

    return render_template("signup.html")  

        flash("Username or Email already exists. Try a different one.", "error")
        return redirect(url_for('auth.index'))  # Redirect back to signup page
