# Placement Portal Application (PPA) – V2

Placement Portal Application (PPA) is a role-based web platform designed to manage and automate campus recruitment activities within an institute. The system enables structured interaction between the Institute (Admin), Companies, and Students for managing placement drives, applications, approvals, and reporting.

---

## Tech Stack

- **Backend:** Flask (API)
- **Frontend:** VueJS
- **Templates:** Jinja2 (Entry point only)
- **Styling:** Bootstrap
- **Database:** SQLite (Programmatically created using SQLAlchemy)
- **Caching:** Redis
- **Background Jobs:** Celery + Redis

All components run locally and adhere strictly to the mandated framework requirements.

---

## User Roles

### Admin (Institute)
- Pre-created superuser (no registration)
- Approves/rejects company registrations
- Approves/rejects placement drives
- Manages students, companies, and applications
- Views placement statistics and reports
- Can deactivate/blacklist users

### Company
- Registers company profile
- Creates placement drives (after admin approval)
- Views applicants
- Shortlists and updates application status
- Schedules interviews and publishes final results

### Student
- Self-registration and login
- Views approved placement drives
- Applies for drives (with eligibility validation)
- Tracks application status
- Views placement history
- Exports application history as CSV

---

## Core Features

- Role-based authentication and authorization
- Unified user model
- Placement drive management
- Application tracking system
- Eligibility validation before application
- Prevention of duplicate applications
- Search functionality for drives and users
- Placement history maintenance

---

## Background Jobs

- **Daily Reminder Job:** Sends reminders about upcoming deadlines.
- **Monthly Activity Report:** Generates and emails placement statistics to Admin.
- **CSV Export Job:** Allows students to export application history asynchronously.

---

## Project Structure

The application follows a modular backend architecture with separated frontend and backend folders. The database schema is defined using SQLAlchemy models and created programmatically.

---

## Summary

PPA replaces manual placement coordination processes with a structured, scalable, and automated web application. It ensures efficient management of recruitment workflows, transparent application tracking, and automated reporting within an institute placement ecosystem.
