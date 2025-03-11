# CampusConnect

CampusConnect is a comprehensive Django-based campus management system that streamlines administrative tasks and communication among various user roles—Head of Department (HOD), Staff, and Students. The project features role-based dashboards, attendance tracking, result management, leave applications, notifications, and feedback mechanisms.

## Table of Contents

- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Features

### HOD Panel

- **Dashboard:** Overview of students, courses, subjects, and staff counts.
- **Student Management:** Add, view, edit, update, and delete student records.
- **Course Management:** Add, view, edit, update, and delete courses.
- **Staff Management:** Add, view, edit, update, and delete staff records.
- **Subject Management:** Manage subjects by assigning courses and staff.
- **Session Management:** Add, view, edit, update, and delete session years.
- **Notifications:** Send notifications (with email integration) to both staff and students.
- **Leave & Feedback:** Approve/Disapprove leave applications and respond to feedback.
- **Attendance:** View detailed attendance reports and student details.

### Staff Panel

- **Dashboard:** Role-specific home screen for staff.
- **Notifications:** View notifications and mark them as done.
- **Leave Application:** Apply for leave and view leave history.
- **Feedback:** Submit feedback to the HOD.
- **Attendance Management:** Take attendance for assigned subjects, save records, and view attendance history.
- **Result Management:** Add and update student results.

### Student Panel

- **Dashboard:** Student home view.
- **Notifications:** Receive and mark notifications.
- **Leave Application:** Apply for leave.
- **Feedback:** Provide feedback.
- **Attendance:** View attendance records for enrolled subjects.
- **Results:** View and download results as a PDF.

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/rachitshah07/CampusConnect.git
   cd CampusConnect
   ```
2. **Create a Virtual Environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables: Create a .env file in the project root with at least the following:**

   ```dotenv
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   SERVER_EMAIL= your_server_email
   ```

5. **Run Database Migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Application:**

   ```bash
   python manage.py runserver
   ```

## Usage

### Authentication

The project uses a custom authentication backend (see `EmailBackend.py`) allowing users to log in with their **email addresses**. The custom user model (`CustomUser` in `models.py`) differentiates between **HOD**, **Staff**, and **Student** roles.

### Role-Based Access

- **HOD**  
  Manage courses, students, staff, subjects, sessions, attendance, notifications, leave, and feedback.
- **Staff**  
  Take attendance, add or update results, apply for leave, and submit feedback.
- **Student**  
  View attendance, results, and notifications; apply for leave, and provide feedback.

### Attendance and Results

- **Staff** can mark attendance and later add or update student results.
- **Students** can view their attendance records and download their results in PDF format (implemented using [ReportLab](https://www.reportlab.com/) in `Student_Views.py`).

---

## Customization

### Models and Views

Customize data models in `models.py` and extend views in `Hod_Views.py`, `Staff_Views.py`, and `Student_Views.py` as needed to fit your project’s requirements.

### Templates

Update or reorganize the HTML templates located in the `templates/` directory to change the UI/UX for each user role (HOD, Staff, Student).

### Email Integration

Modify email settings and templates in the views (for example, in `Hod_Views.py` for sending notifications) to suit your mailing requirements. You can configure SMTP or other email providers by adjusting your Django `settings.py` or `.env` file.
