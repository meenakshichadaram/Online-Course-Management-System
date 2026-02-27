OCMS_capstone_project
About the Project
This project is a backend application developed using Django and Django REST Framework (DRF). It provides RESTful APIs to manage data efficiently with secure authentication, filtering, and pagination support.

The objective of this project is to design a structured and scalable backend system that follows best practices in REST API development. It demonstrates proper project organization, secure access using JWT authentication, and clean implementation of CRUD operations with PostgreSQL as the database.

Features
REST API development using Django REST Framework

JWT-based authentication system

Create, Read, Update, and Delete (CRUD) operations

Pagination for efficient data handling

Filtering using Django Filter

PostgreSQL database integration

Well-structured and maintainable codebase

API testing using Postman or Swagger

Technologies Used
Python 3.x

Django

Django REST Framework

Simple JWT

PostgreSQL

Installation and Setup
Follow the steps below to run the project locally:

Clone the Repository
git clone https://github.com/your-username/your-repo-name.git

cd your-repo-name

Create a Virtual Environment
python -m venv env

Activate the Virtual Environment
On Windows: env\Scripts\activate

On Mac/Linux: source env/bin/activate

Install Dependencies
pip install -r requirements.txt

Configure PostgreSQL
Install PostgreSQL and ensure it is running.

Create a new database.

Update the DATABASES configuration in settings.py:

DATABASES = { 'default': { 'ENGINE': 'django.db.backends.postgresql', 'NAME': 'your_database_name', 'USER': 'your_username', 'PASSWORD': 'your_password', 'HOST': 'localhost', 'PORT': '5432', } }

Apply Migrations
python manage.py makemigrations python manage.py migrate

Run the Server
python manage.py runserver

The application will be available at: http://127.0.0.1:8000/
