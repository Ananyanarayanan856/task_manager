# Task Manager Web App

A beautiful, premium task and project management system built with Django and PostgreSQL. This application features a modern  role-based access control, and seamless project tracking.

## ✨ Features

- **Role-Based Access Control**:
  - **Admins**: Can create/manage projects, add members to the system, create tasks, and oversee all progress.
  - **Members**: Have a personalized dashboard to view their assigned projects, project details, and update the status of their assigned tasks.
- **Premium User Interface**: A cohesive, modern lavender and soft-gold aesthetic with smooth hover animations and clean typography (Outfit font).
- **PostgreSQL Ready**: Pre-configured with `dj-database-url` and `psycopg2` for robust database management.
- **Deployment Ready**: Fully configured for 1-click deployment on Railway (includes `Procfile`, `requirements.txt`, and automated migrations).

## 🚀 Tech Stack

- **Backend**: Python, Django (v5.2.13)
- **Database**: PostgreSQL
- **Frontend**: HTML5, Vanilla CSS (Custom UI Theme)
- **Server/Deployment**: Gunicorn, WhiteNoise (for static files)

## 💻 Local Setup Instructions

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repository-url>
   cd TASK/task_manager
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup the Database**:
   - Ensure PostgreSQL is running on your local machine.
   - Create a database named `task_manager_db`.
   - In `task_manager/settings.py`, update the `DATABASES` connection string with your local PostgreSQL password.

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create an Admin Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.


---
*Built with using Django*
