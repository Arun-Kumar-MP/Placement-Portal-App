# controllers/models.py
# This file defines the database models for the application.

from .database import db
from flask_security import UserMixin, RoleMixin


# Authentication Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True)

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

# PPA Models
class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    website = db.Column(db.String(255))
    is_approved = db.Column(db.Boolean(), default=False)

    # Relationships
    drives = db.relationship('PlacementDrive', backref='company', lazy=True)


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255))
    cgpa = db.Column(db.Float)
    branch = db.Column(db.String(255))
    year = db.Column(db.Integer)
    resume = db.Column(db.String(255))

    # Relationships
    applications = db.relationship('Application', backref='student', lazy=True)


class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.id'), nullable=False)
    job_title = db.Column(db.String(255))
    job_description = db.Column(db.Text)
    salary = db.Column(db.Float)
    skills_required = db.Column(db.String(255))
    min_cgpa = db.Column(db.Float)
    eligibility_branch = db.Column(db.String(255))
    eligibility_year = db.Column(db.Integer)
    status = db.Column(db.String(20), default='Pending')
    application_deadline = db.Column(db.Date)

    # Relationships
    applications = db.relationship('Application', backref='drive', lazy=True)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'))
    application_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Applied')
