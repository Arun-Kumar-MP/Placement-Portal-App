# /controllers/company_api.py
# This file contains the Company APIs for the application.

from datetime import datetime

from flask import make_response, jsonify, request
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted, current_user

from .models import db, StudentProfile, CompanyProfile, PlacementDrive, Application


ALLOWED_APPLICATION_STATUSES = (
    "Applied",
    "Shortlisted",
    "Interview Scheduled",
    "Selected",
    "Rejected",
)





# --- Company APIs ---
class CompanyApplicationStatusAPI(Resource):
    @auth_token_required
    @roles_accepted('company')
    def post(self, application_id):
        data = request.get_json() or {}
        status = data.get("status")

        if status not in ALLOWED_APPLICATION_STATUSES:
            return {"message": "Invalid status"}, 400

        application = Application.query.get(application_id)
        if not application:
            return {"message": "Application not found"}, 404

        application.status = status
        db.session.commit()
        return {"message": "Status updated successfully"}, 200


class CompanyApplicationsAPI(Resource):
    @auth_token_required
    @roles_accepted('company')
    def get(self, drive_id):
        apps = Application.query.filter_by(drive_id=drive_id).all()
        result = []

        for a in apps:
            student = StudentProfile.query.get(a.student_id)
            result.append({
                "id": a.id,
                "student_id": student.id if student else None,
                "student_name": student.name if student else "Unknown",
                "name": student.name if student else "Unknown",
                "branch": student.branch if student else "Unknown",
                "cgpa": student.cgpa if student else "N/A",
                "year": student.year if student else "N/A",
                "resume": student.resume if student else None,
                "status": a.status,
                "application_date": a.application_date.strftime("%Y-%m-%d") if a.application_date else "N/A"
            })

        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_accepted('company')
    def post(self, drive_id):
        # Kept for backward compatibility with earlier frontend flow.
        data = request.get_json() or {}
        app_id = data.get("application_id")
        new_status = data.get("status")

        if new_status not in ALLOWED_APPLICATION_STATUSES:
            return {"message": "Invalid status"}, 400

        application = Application.query.get(app_id)
        if not application:
            return {"message": "Application not found"}, 404

        application.status = new_status
        db.session.commit()
        return {"message": f"Application {app_id} updated to {new_status}"}, 200


class CompanyCreateDriveAPI(Resource):
    @auth_token_required
    @roles_accepted('company')
    def post(self):
        data = request.get_json() or {}
        company = CompanyProfile.query.filter_by(user_id=current_user.id).first()

        if not company or not company.is_approved:
            return {"message": "Company not approved"}, 403

        new_drive = PlacementDrive(
            company_id=company.id,
            job_title=data.get("job_title"),
            job_description=data.get("job_description"),
            salary=data.get("salary"),
            skills_required=data.get("skills_required"),
            min_cgpa=data.get("min_cgpa", 0.0),
            eligibility_branch=data.get("eligibility_branch"),
            eligibility_year=data.get("eligibility_year"),
            status="Ongoing",
            application_deadline=datetime.strptime(data.get('application_deadline'), "%Y-%m-%d").date()
        )

        db.session.add(new_drive)
        db.session.commit()
        return {"message": "Drive created successfully"}, 201


class CompanyCompleteDriveAPI(Resource):
    @auth_token_required
    @roles_accepted('company')
    def post(self, drive_id):
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message": "Drive not found"}, 404

        if drive.status != "Ongoing":
            return {"message": "Only approved ongoing drives can be completed"}, 400

        drive.status = "Completed"
        db.session.commit()
        return {"message": "Drive marked as completed"}, 200


class CompanyDriveAPI(Resource):
    @auth_token_required
    @roles_accepted('company')
    def get(self, drive_id):
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message": "Drive not found"}, 404

        company = CompanyProfile.query.get(drive.company_id)

        return {
            "id": drive.id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "salary": drive.salary,
            "skills_required": drive.skills_required,
            "min_cgpa": drive.min_cgpa,
            "eligibility_branch": drive.eligibility_branch,
            "eligibility_year": drive.eligibility_year,
            "status": drive.status,
            "applicants_count": Application.query.filter_by(drive_id=drive.id).count(),
            "application_deadline": drive.application_deadline.strftime("%Y-%m-%d") if drive.application_deadline else "N/A",
            "company_name": company.name if company else "Unknown"
        }, 200


class CompanyDrivesAPI(Resource):
    @auth_token_required
    @roles_accepted('company')
    def get(self):
        company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
        if not company:
            return {"message": "Company profile not found"}, 404

        drives = PlacementDrive.query.filter_by(company_id=company.id).all()
        result = []

        for d in drives:
            result.append({
                "id": d.id,
                "job_title": d.job_title,
                "status": d.status,
                "applicants_count": Application.query.filter_by(drive_id=d.id).count(),
                "description": d.job_description[:50] if d.job_description else "",
                "application_deadline": d.application_deadline.strftime("%Y-%m-%d") if d.application_deadline else "N/A"
            })

        return make_response(jsonify(result), 200)


class CompanyUpdateDriveAPI(Resource):
    @auth_token_required
    @roles_accepted('company')
    def post(self, drive_id):
        data = request.get_json() or {}
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message": "Drive not found"}, 404

        drive.job_title = data.get("job_title", drive.job_title)
        drive.job_description = data.get("job_description", drive.job_description)
        drive.salary = data.get("salary", drive.salary)
        drive.skills_required = data.get("skills_required", drive.skills_required)
        drive.min_cgpa = data.get("min_cgpa", drive.min_cgpa)
        drive.eligibility_branch = data.get("eligibility_branch", drive.eligibility_branch)
        drive.eligibility_year = data.get("eligibility_year", drive.eligibility_year)

        if data.get("application_deadline"):
            drive.application_deadline = datetime.strptime(data.get("application_deadline"), "%Y-%m-%d").date()

        # Re-submit rejected drives for approval after editing.
        if drive.status == "Rejected":
            drive.status = "Pending"

        db.session.commit()
        return {"message": "Drive updated successfully"}, 200


