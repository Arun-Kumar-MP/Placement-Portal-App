# /controllers/admin_api.py
# This file contains the Admin APIs for the application.

from flask import make_response, jsonify, request
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted
from .models import db, User, StudentProfile, CompanyProfile, PlacementDrive, Application


# --- Admin APIs ---
class AdminApplicationsAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        apps = Application.query.all()
        result = []
        for i, a in enumerate(apps, start=1):
            student = StudentProfile.query.get(a.student_id)
            drive = PlacementDrive.query.get(a.drive_id)
            company = CompanyProfile.query.get(drive.company_id) if drive else None
            result.append({
                "id": i,
                "student_id": student.id if student else None,
                "student_name": student.name if student else "Unknown",
                "drive_title": drive.job_title if drive else "Unknown",
                "company_name": company.name if company else "Unknown",
                "application_date": a.application_date.strftime("%Y-%m-%d") if a.application_date else "N/A",
                "status": a.status,
                "drive_id": a.drive_id
            })
        return make_response(jsonify(result), 200)


class AdminApproveCompanyAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.active = True
        company = CompanyProfile.query.filter_by(user_id=user_id).first()
        if company:
            company.is_approved = True
        db.session.commit()
        return {"message": "Company approved successfully"}, 200


class AdminBlacklistCompanyAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.active = False
        company = CompanyProfile.query.filter_by(user_id=user_id).first()
        if company:
            company.is_approved = False
        db.session.commit()
        return {"message": "Company blacklisted successfully"}, 200


class AdminCompaniesAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        companies = CompanyProfile.query.all()
        registered, applications = [], []
        for c in companies:
            user = User.query.get(c.user_id)
            if not user:
                continue
            data = {
                "id": c.id,
                "name": c.name,
                "email": user.email,
                "user_id": user.id,
                "active": user.active,
                "is_approved": c.is_approved
            }
            if user.active:
                registered.append(data)
            else:
                applications.append(data)
        return make_response(jsonify({"registered": registered, "applications": applications}), 200)

    @auth_token_required
    @roles_accepted('admin')
    def put(self, company_id):
        company = CompanyProfile.query.get(company_id)
        if not company:
            return {"message": "Company not found"}, 404
        user = User.query.get(company.user_id)
        data = request.get_json() or {}
        if "active" in data:
            user.active = data["active"]
            company.is_approved = data["active"]
            db.session.commit()
            return {"message": "Company status updated"}, 200
        return {"message": "Invalid payload"}, 400


class AdminDriveAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self, drive_id):
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message": "Drive not found"}, 404
        company = CompanyProfile.query.get(drive.company_id)
        applicants_count = Application.query.filter_by(drive_id=drive.id).count()
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
            "applicants_count": applicants_count,
            "application_deadline": drive.application_deadline.strftime("%Y-%m-%d") if drive.application_deadline else "N/A",
            "company_name": company.name if company else "Unknown",
            "company_website": company.website if company and company.website else "N/A"
        }, 200


class AdminDriveCompleteAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def post(self, drive_id):
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message": "Drive not found"}, 404
        drive.status = "Completed"
        db.session.commit()
        return {"message": "Drive marked as completed"}, 200


class AdminOngoingDrivesAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        drives = PlacementDrive.query.filter_by(status="Ongoing").all()
        result = []
        for d in drives:
            company = CompanyProfile.query.get(d.company_id)
            applicants_count = Application.query.filter_by(drive_id=d.id).count()
            result.append({
                "id": d.id,
                "job_title": d.job_title,
                "company_name": company.name if company else "Unknown",
                "application_deadline": d.application_deadline.strftime("%Y-%m-%d") if d.application_deadline else "N/A",
                "applicants_count": applicants_count,
                "drive_id": d.id
            })
        return make_response(jsonify(result), 200)


class AdminStudentAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self, student_id):
        student = StudentProfile.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404
        user = User.query.get(student.user_id)
        return {
            "id": student.id,
            "name": student.name,
            "branch": student.branch or "Unknown",
            "cgpa": student.cgpa or "N/A",
            "year": student.year or "N/A",
            "resume": student.resume or None,
            "email": user.email if user else "N/A"
        }, 200

    @auth_token_required
    @roles_accepted('admin')
    def put(self, student_id):
        student = StudentProfile.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        user = User.query.get(student.user_id)
        if not user:
            return {"message": "Associated user not found"}, 404

        data = request.get_json() or {}
        if "active" not in data:
            return {"message": "Invalid payload"}, 400

        user.active = bool(data["active"])
        db.session.commit()
        return {"message": "Student status updated"}, 200


class AdminStudentsAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        students = db.session.query(StudentProfile).join(User).filter(User.active == True).all()
        result = []
        for s in students:
            user = User.query.get(s.user_id)
            result.append({
                "id": s.id,
                "name": s.name,
                "cgpa": s.cgpa or "N/A",
                "branch": s.branch or "N/A",
                "year": s.year or "N/A",
                "email": user.email if user else "N/A",
                "user_id": s.user_id
            })
        return make_response(jsonify(result), 200)


