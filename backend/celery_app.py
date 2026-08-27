from datetime import date, timedelta, datetime
import csv
import os

from celery import Celery
from celery.schedules import crontab

from app import app
from controllers.database import db
from controllers.models import (
    User,
    Role,
    StudentProfile,
    PlacementDrive,
    CompanyProfile,
    Application,
)
from mail import send_email


celery = Celery(
    'tasks',
    broker='redis://localhost:6380/0',
    backend='redis://localhost:6380/0'
)

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)


@celery.task()
def send_daily_reminder():
    """Send reminder mails to students for drives closing in the next 2 days."""
    with app.app_context():
        today = date.today()
        reminder_until = today + timedelta(days=2)

        upcoming_drives = (
            db.session.query(PlacementDrive, CompanyProfile)
            .join(CompanyProfile, PlacementDrive.company_id == CompanyProfile.id)
            .filter(
                CompanyProfile.is_approved == True,
                PlacementDrive.status == 'Ongoing',
                PlacementDrive.application_deadline >= today,
                PlacementDrive.application_deadline <= reminder_until,
            )
            .all()
        )

        if not upcoming_drives:
            print('No upcoming deadlines found for reminder.')
            return

        lines = ['Upcoming placement application deadlines:']
        for drive, company in upcoming_drives:
            lines.append(
                f"- {drive.job_title} at {company.name} (Deadline: {drive.application_deadline.strftime('%Y-%m-%d')})"
            )

        subject = 'PPA Daily Reminder: Upcoming Placement Deadlines'
        message = '\n'.join(lines)

        total_sent = 0
        students = StudentProfile.query.all()
        for student in students:
            user = User.query.get(student.user_id)
            if not user or not user.active:
                continue
            send_email(user.email, subject, message)
            total_sent += 1

        print(f'Daily reminders sent to {total_sent} students.')


@celery.task()
def send_monthly_activity_report():
    """Send monthly HTML placement activity report to admin."""
    with app.app_context():
        drives_conducted = PlacementDrive.query.filter_by(status='Completed').count()
        students_applied = db.session.query(Application.student_id).distinct().count()
        students_selected = (
            db.session.query(Application.student_id)
            .filter(Application.status.like('Selected%'))
            .distinct()
            .count()
        )

        report_month = datetime.now().strftime('%B %Y')

        html_report = f"""
        <h2>Placement Activity Report - {report_month}</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
          <tr><th>Metric</th><th>Value</th></tr>
          <tr><td>Number of Drives Conducted</td><td>{drives_conducted}</td></tr>
          <tr><td>Number of Students Applied</td><td>{students_applied}</td></tr>
          <tr><td>Number of Students Selected</td><td>{students_selected}</td></tr>
        </table>
        <p style="margin-top: 12px;">This is an automated monthly report from Placement Portal Application.</p>
        """

        admin_user = (
            User.query.join(User.roles)
            .filter(Role.name == 'admin')
            .first()
        )

        if not admin_user:
            print('Admin user not found. Monthly report not sent.')
            return

        send_email(
            admin_user.email,
            f'PPA Monthly Activity Report - {report_month}',
            html_report,
            is_html=True,
        )
        print('Monthly activity report sent to admin.')


@celery.task()
def export_student_applications_csv(student_user_id):
    """Generate student application history CSV and notify via email."""
    with app.app_context():
        student = StudentProfile.query.filter_by(user_id=student_user_id).first()
        user = User.query.get(student_user_id)

        if not student or not user:
            print('Student/user not found for CSV export.')
            return

        applications = (
            db.session.query(Application, PlacementDrive, CompanyProfile)
            .join(PlacementDrive, Application.drive_id == PlacementDrive.id)
            .join(CompanyProfile, PlacementDrive.company_id == CompanyProfile.id)
            .filter(Application.student_id == student.id)
            .all()
        )

        export_dir = os.path.join(app.root_path, 'instance', 'exports')
        os.makedirs(export_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'student_{student.id}_applications_{timestamp}.csv'
        file_path = os.path.join(export_dir, file_name)

        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                'Student ID',
                'Company Name',
                'Drive Title',
                'Application Status',
                'Application Date',
                'Application Deadline',
            ])

            for app_row, drive, company in applications:
                writer.writerow([
                    student.id,
                    company.name,
                    drive.job_title,
                    app_row.status,
                    app_row.application_date.strftime('%Y-%m-%d') if app_row.application_date else 'N/A',
                    drive.application_deadline.strftime('%Y-%m-%d') if drive.application_deadline else 'N/A',
                ])

        send_email(
            user.email,
            'PPA CSV Export Ready',
            f'Your application history CSV has been generated successfully. File: {file_name}',
        )
        print(f'CSV export generated: {file_path}')


celery.conf.beat_schedule = {
    'send-daily-reminder': {
        'task': 'celery_app.send_daily_reminder',
        # Daily at 09:00 AM.
        'schedule': crontab(minute=0, hour=9),
    },
    'send-monthly-activity-report': {
        'task': 'celery_app.send_monthly_activity_report',
        # First day of every month at 09:30 AM.
        'schedule': crontab(minute=30, hour=9, day_of_month=1),
    },
}
