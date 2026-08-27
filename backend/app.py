# app.py
# This file initializes the Flask application and sets up the necessary configurations.

from flask import Flask, jsonify, request
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from flask_restful import Api
from flask_cors import CORS

from controllers.config import Config
from controllers.database import db
from controllers.user_datastore import user_datastore


def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object(Config)

    # Database configuration
    db.init_app(app)

    # Initialize Flask-Security
    Security(app, user_datastore)

    # Initialize Flask-RESTful API
    api = Api(app, prefix='/api')

    # Create Database tables and default roles/users
    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Superuser')
        user_datastore.find_or_create_role(name='company', description='Recruiter')
        user_datastore.find_or_create_role(name='student', description='Candidate')

        if not user_datastore.find_user(email='admin@ppa.com'):
            user_datastore.create_user(
                email='admin@ppa.com',
                password=hash_password('54321'),
                roles=[admin_role]
            )
        db.session.commit()

    return app, api


app, api = create_app()

CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


from controllers.auth_api import *

# Auth Routes
api.add_resource(AuthCheckEmailAPI, '/auth/check-email')
api.add_resource(AuthLoginAPI, '/auth/login')
api.add_resource(AuthLogoutAPI, '/auth/logout')
api.add_resource(AuthRegisterAPI, '/auth/register')

# Admin Routes
from controllers.admin_api import *

api.add_resource(AdminApplicationsAPI, '/admin/applications')
api.add_resource(AdminApproveCompanyAPI, '/admin/companies/<int:user_id>/approve')
api.add_resource(AdminBlacklistCompanyAPI, '/admin/companies/<int:user_id>/blacklist')
api.add_resource(AdminCompaniesAPI, '/admin/companies', '/admin/companies/<int:company_id>')
api.add_resource(AdminDriveAPI, '/admin/drives/<int:drive_id>')
api.add_resource(AdminDriveCompleteAPI, '/admin/drives/<int:drive_id>/complete')
api.add_resource(AdminOngoingDrivesAPI, '/admin/drives/ongoing')
api.add_resource(AdminStudentAPI, '/admin/students/<int:student_id>')
api.add_resource(AdminStudentsAPI, '/admin/students')

# Company Routes
from controllers.company_api import *

api.add_resource(CompanyApplicationStatusAPI, '/company/applications/<int:application_id>/status')
api.add_resource(CompanyApplicationsAPI, '/company/drives/<int:drive_id>/applications')
api.add_resource(CompanyCreateDriveAPI, '/company/drives')
api.add_resource(CompanyCompleteDriveAPI, '/company/drives/<int:drive_id>/complete')
api.add_resource(CompanyDriveAPI, '/company/drives/<int:drive_id>')
api.add_resource(CompanyDrivesAPI, '/company/drives')
api.add_resource(CompanyUpdateDriveAPI, '/company/drives/<int:drive_id>/update')

# Student Routes
from controllers.student_api import *

api.add_resource(StudentDrivesAPI, '/student/drives')
api.add_resource(StudentApplicationsAPI, '/student/applications')
api.add_resource(StudentExportApplicationsAPI, '/student/applications/export')
api.add_resource(StudentDriveDetailsAPI, '/student/drives/<int:id>')
api.add_resource(StudentProfileAPI, '/student/profile')

# Task Routes
from controllers.tasks_api import *

api.add_resource(SendReminderNowAPI, '/tasks/send-reminder-now')
api.add_resource(SendMonthlyReportNowAPI, '/tasks/send-monthly-report-now')


if __name__ == '__main__':
    app.run(debug=True)
