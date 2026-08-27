# /controllers/student_api.py
# This file contains the Student APIs for the application.

from datetime import date

from flask import request
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted, current_user

from .models import db, PlacementDrive, CompanyProfile, StudentProfile, Application, User


class StudentDrivesAPI(Resource):
    @auth_token_required
    @roles_accepted('student')
    def get(self):
        drives = (
            db.session.query(PlacementDrive, CompanyProfile)
            .join(CompanyProfile, PlacementDrive.company_id == CompanyProfile.id)
            .filter(
                CompanyProfile.is_approved == True,
                PlacementDrive.status == "Ongoing",
                PlacementDrive.application_deadline >= date.today()
            )
            .all()
        )

        result = []
        for drive, company in drives:
            result.append({
                "id": drive.id,
                "job_title": drive.job_title,
                "company_name": company.name,
                "application_deadline": drive.application_deadline.strftime("%Y-%m-%d"),
                "salary": drive.salary,
                "skills_required": drive.skills_required,
                "min_cgpa": drive.min_cgpa,
                "eligibility_branch": drive.eligibility_branch,
                "eligibility_year": drive.eligibility_year,
                "status": drive.status
            })

        return result, 200


class StudentApplicationsAPI(Resource):
    @auth_token_required
    @roles_accepted('student')
    def get(self):
        student = StudentProfile.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404

        apps = (
            db.session.query(Application, PlacementDrive, CompanyProfile)
            .join(PlacementDrive, Application.drive_id == PlacementDrive.id)
            .join(CompanyProfile, PlacementDrive.company_id == CompanyProfile.id)
            .filter(Application.student_id == student.id)
            .all()
        )

        result = []
        for app_row, drive, company in apps:
            result.append({
                "id": app_row.id,
                "job_title": drive.job_title,
                "company_name": company.name,
                "application_date": app_row.application_date.strftime("%Y-%m-%d") if app_row.application_date else "N/A",
                "application_deadline": drive.application_deadline.strftime("%Y-%m-%d"),
                "status": app_row.status,
                "drive_id": drive.id
            })

        return result, 200

    @auth_token_required
    @roles_accepted('student')
    def post(self):
        student = StudentProfile.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404

        data = request.get_json() or {}
        drive_id = data.get("drive_id")
        if not drive_id:
            return {"message": "Drive ID is required"}, 400

        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message": "Drive not found"}, 404

        company = CompanyProfile.query.get(drive.company_id)
        if not company or not company.is_approved:
            return {"message": "Cannot apply: company is not approved"}, 403

        if drive.status != "Ongoing":
            return {"message": "Cannot apply: drive is not open"}, 400

        if drive.application_deadline and drive.application_deadline < date.today():
            return {"message": "Cannot apply: deadline has passed"}, 400

        existing = Application.query.filter_by(student_id=student.id, drive_id=drive.id).first()
        if existing:
            return {"message": "You have already applied to this drive"}, 409

        if student.cgpa is None or student.branch is None:
            return {"message": "Please complete your student profile before applying"}, 400

        if drive.min_cgpa is not None and student.cgpa < drive.min_cgpa:
            return {"message": "Not eligible: minimum CGPA requirement not met"}, 403

        if drive.eligibility_branch:
            allowed_branches = [b.strip().lower() for b in drive.eligibility_branch.split(",") if b.strip()]
            if allowed_branches and student.branch.strip().lower() not in allowed_branches:
                return {"message": "Not eligible: branch requirement not met"}, 403

        new_application = Application(
            student_id=student.id,
            drive_id=drive.id,
            application_date=date.today(),
            status="Applied"
        )
        db.session.add(new_application)
        db.session.commit()
        return {"message": "Application submitted successfully"}, 201


class StudentExportApplicationsAPI(Resource):
    @auth_token_required
    @roles_accepted('student')
    def post(self):
        from celery_app import export_student_applications_csv

        export_student_applications_csv.delay(current_user.id)
        return {
            "message": "Your CSV export has started. You will receive an email once it is ready."
        }, 202


class StudentProfileAPI(Resource):
    @auth_token_required
    @roles_accepted('student')
    def get(self):
        student = StudentProfile.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404

        user = User.query.get(current_user.id)
        return {
            "id": student.id,
            "name": student.name or "",
            "email": user.email if user else "",
            "branch": student.branch or "",
            "cgpa": student.cgpa if student.cgpa is not None else "",
            "year": student.year if student.year is not None else "",
            "resume": student.resume or ""
        }, 200

    @auth_token_required
    @roles_accepted('student')
    def put(self):
        student = StudentProfile.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404

        data = request.get_json() or {}
        student.name = data.get("name", student.name)
        student.branch = data.get("branch", student.branch)
        student.resume = data.get("resume", student.resume)

        cgpa = data.get("cgpa")
        if cgpa not in (None, ""):
            student.cgpa = float(cgpa)

        year = data.get("year")
        if year not in (None, ""):
            student.year = int(year)

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200


class StudentDriveDetailsAPI(Resource):
    @auth_token_required
    @roles_accepted('student')
    def get(self, id):
        drive = PlacementDrive.query.get(id)
        if not drive:
            return {"message": "Drive not found"}, 404

        company = CompanyProfile.query.get(drive.company_id)
        if not company or not company.is_approved:
            return {"message": "Company not approved"}, 403

        result = {
            "id": drive.id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "salary": drive.salary,
            "skills_required": drive.skills_required,
            "min_cgpa": drive.min_cgpa,
            "eligibility_branch": drive.eligibility_branch,
            "eligibility_year": drive.eligibility_year,
            "status": drive.status,
            "application_deadline": drive.application_deadline.strftime("%Y-%m-%d"),
            "company_name": company.name,
            "company_website": company.website
        }

        return result, 200
