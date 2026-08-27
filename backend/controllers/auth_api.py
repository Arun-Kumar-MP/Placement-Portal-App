# controllers/auth_api.py
# This file contains the Authentication APIs for the application.

from flask import jsonify, request, make_response
from flask_restful import Resource
from flask_security import utils, auth_token_required
from .user_datastore import user_datastore
from .database import db
from .models import StudentProfile, CompanyProfile


# --- Auth APIs ---

class AuthCheckEmailAPI(Resource):
    def post(self):
        email = request.get_json().get('email')
        if not email:
            return make_response(jsonify({'error': 'Email is required'}), 400)

        user = user_datastore.find_user(email=email)
        return make_response(jsonify({'available': not bool(user)}), 200)


class AuthLoginAPI(Resource):
    def post(self):
        creds = request.get_json()
        if not creds:
            return make_response(jsonify({'error': 'Missing credentials'}), 400)

        email, password = creds.get('email'), creds.get('password')
        if not email or not password:
            return make_response(jsonify({'error': 'Email and password required'}), 400)

        user = user_datastore.find_user(email=email)
        if not user or not utils.verify_password(password, user.password):
            return make_response(jsonify({'error': 'Invalid email or password'}), 401)

        user_roles = [role.name for role in user.roles]

        # Company users must be approved by admin before they can login.
        if 'company' in user_roles:
            company = CompanyProfile.query.filter_by(user_id=user.id).first()
            if not user.active or not company or not company.is_approved:
                return make_response(jsonify({
                    'error': 'Your company account is pending admin approval. Please try again later!'
                }), 403)

        auth_token = user.get_auth_token()
        utils.login_user(user)

        return make_response(jsonify({
            'message': 'Login successful',
            'user': {
                'email': user.email,
                'roles': user_roles,
                'auth_token': auth_token
            }
        }), 200)


class AuthLogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        return make_response(jsonify({'message': 'Logout successful'}), 200)


class AuthRegisterAPI(Resource):
    def post(self):
        creds = request.get_json()
        username, email, password, role_name = (
            creds.get('username'),
            creds.get('email'),
            creds.get('password'),
            creds.get('role_name')
        )

        if not email or not password or not role_name or not username:
            return make_response(jsonify({'error': 'Email, password, role, and username are required'}), 400)

        if user_datastore.find_user(email=email):
            return make_response(jsonify({'error': 'User already exists'}), 409)

        role = user_datastore.find_role(role_name)
        if not role:
            return make_response(jsonify({'error': 'Invalid role'}), 400)

        new_user = user_datastore.create_user(
            email=email,
            password=utils.hash_password(password),
            roles=[role],
            active=(role_name == 'student')
        )
        db.session.flush()  # ensures new_user.id is available

        if role_name == 'student':
            db.session.add(StudentProfile(user_id=new_user.id, name=username))
        elif role_name == 'company':
            db.session.add(CompanyProfile(user_id=new_user.id, name=username))

        db.session.commit()

        return make_response(jsonify({
            'message': f'{role_name.capitalize()} registered successfully',
            'user': {
                'username': username,
                'email': email,
                'role': role_name
            }
        }), 201)
