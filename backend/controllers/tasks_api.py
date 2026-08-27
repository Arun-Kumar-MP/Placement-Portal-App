# /comtrollers/tasks_api.py

from flask import make_response, jsonify
from flask_restful import Resource
from flask_security import auth_token_required, roles_accepted


class SendReminderNowAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def post(self):
        from celery_app import send_daily_reminder
        send_daily_reminder.delay()
        return make_response(jsonify({'message': 'Daily reminder task has been queued!'}), 200)


class SendMonthlyReportNowAPI(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def post(self):
        from celery_app import send_monthly_activity_report
        send_monthly_activity_report.delay()
        return make_response(jsonify({'message': 'Monthly report task has been queued!'}), 200)
