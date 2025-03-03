# PR Tracker

A comprehensive web application for PR professionals to track media coverage, calculate AVE (Advertising Value Equivalent), and generate reports.

## Features

- Track media coverage across publications and editions
- Calculate AVE based on publication rates
- Generate custom reports
- Manage clients and campaigns
- Upload coverage data via Excel
- Search and filter functionality
- User authentication and authorization

## Deployment on Render

### Prerequisites

- A Render account (https://render.com)
- A GitHub repository with your code

### Deployment Steps

1. **Create a new Web Service on Render**

   - Connect your GitHub repository
   - Select the repository and branch
   - Name your service (e.g., "pr-tracker")
   - Set the Environment to "Python"
   - Set the Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Set the Start Command: `gunicorn ave_calculator.wsgi:application`

2. **Add Environment Variables**

   - `SECRET_KEY`: A secure random string
   - `DEBUG`: Set to "False" for production
   - `DATABASE_URL`: This will be automatically set if you create a PostgreSQL database on Render

3. **Create a PostgreSQL Database on Render**

   - Go to the Render Dashboard
   - Click on "New" and select "PostgreSQL"
   - Configure your database settings
   - Link it to your web service

4. **Run Migrations**

   - After deployment, use the Render Shell to run:
     ```
     python manage.py migrate
     ```

5. **Create a Superuser**
   - In the Render Shell, run:
     ```
     python manage.py createsuperuser
     ```

## Local Development

1. Clone the repository

   ```
   git clone https://github.com/yourusername/PR_Tracker.git
   cd PR_Tracker
   ```

2. Create a virtual environment

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```
   pip install -r requirements.txt
   ```

4. Set up the database

   ```
   python manage.py migrate
   ```

5. Create a superuser

   ```
   python manage.py createsuperuser
   ```

6. Run the development server
   ```
   python manage.py runserver
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
