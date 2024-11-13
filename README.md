# AI-Based Class Attendance System
## Overview
The AI-Based Class Attendance System is a web application built using the Django web framework. It utilizes computer vision and machine learning techniques to automatically track and record student attendance in a classroom setting. The system is designed to provide an efficient and reliable solution for managing class attendance, reducing the time and effort required by instructors.

## Key Features

- Facial Recognition: The system uses a deep learning-based facial recognition model to identify and track students as they enter the classroom.
- Attendance Tracking: The application automatically records the attendance data, including student names, entry and exit times, and total class duration.
- Instructor Dashboard: Instructors can access a dashboard to view real-time attendance data, generate attendance reports, and manage student records.
- Student Portal: Students can view their own attendance records and receive notifications about their attendance status.
- Reporting and Analytics: The system provides comprehensive attendance reports and analytics, allowing instructors to monitor student engagement and identify patterns or trends.
- Attendance Policy Enforcement: The application can be configured to enforce attendance policies, such as marking students as absent or late based on predefined rules.
- Secure Access: The system incorporates user authentication and authorization mechanisms to ensure secure access to sensitive data and features.

## Technology Stack

- Backend: Django (Python web framework)
- Database: PostgreSQL
- Frontend: React.js
- Computer Vision: OpenCV, TensorFlow/Keras
- Authentication: Django's built-in authentication system
- Deployment: Docker, Nginx, Gunicorn

## Installation and Setup

Clone the repository:

 https://github.com/steve-ongera/ai-based-class-attendance-system.git

## Create a virtual environment and activate it:

python3 -m venv env

source env/bin/activate

Install the required dependencies:

pip install -r requirements.txt

## Set up the database:

Copypython manage.py migrate

Start the development server:

Copypython manage.py runserver

Access the application at http://localhost:8000.

## Configuration
The application can be configured by modifying the settings.py file in the Django project. Some key configuration options include:

- Database settings
- Facial recognition model parameters
- Attendance policy rules
- Email notifications
- SMTP server settings

## Deployment
The application can be deployed using Docker and containerization. The repository includes a Dockerfile and a docker-compose.yml file for easy deployment.

## Contributing
Contributions to the AI-Based Class Attendance System are welcome. Please follow the standard GitHub workflow:

## Fork the repository

- Create a new branch for your feature or bug fix
- Make your changes and commit them
- Push your changes to your forked repository
- Create a pull request to the main repository

## License
This project is licensed under the MIT License.

## Contact
For any questions or inquiries, please contact the project maintainers at gadafisteve001@gmail.com.