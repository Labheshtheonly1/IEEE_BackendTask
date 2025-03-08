from flask import Flask
from auth import auth_bp
from admin import admin_bp
from user import user_bp  # Import the user blueprint
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Register blueprints
app.register_blueprint(auth_bp)    # Authentication routes
app.register_blueprint(admin_bp)   # Admin routes
app.register_blueprint(user_bp)    # User routes

if __name__ == '__main__':
    app.run(debug=True)
