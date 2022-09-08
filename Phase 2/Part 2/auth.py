# Login
from flask_login import login_user, logout_user, login_required, LoginManager

# Sign up
from werkzeug.security import generate_password_hash, check_password_hash

from models import FitwellUser

class Auth():
    def load(app):
        # Login Manager to manage the login and logout sessions
        login_manager = LoginManager()
        login_manager.login_view = 'index'
        login_manager.login_message = '* Please log in to access this page'
        login_manager.init_app(app)

        # This load_user method will be called by app.py to check if the input email is in the database
        @login_manager.user_loader
        def load_user(user_id):
            # Checking against the email address to get the email, password
            return FitwellUser.get_user_byEmail(email=user_id)

    def login(user, password):
        if not user or not check_password_hash(user.get_record()['password'], password):
            return False
        else:
            login_user(user)
            return True

    def register(user, email, password, weight, gender, height, date_of_birth):
        if user:
            return False

        new_user = FitwellUser(
            email = email,
            password = generate_password_hash(password, method='sha256'),
            weight = weight,
            gender = gender,
            height = height,
            date_of_birth = date_of_birth
        )

        return True
