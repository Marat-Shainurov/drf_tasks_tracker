# General description
tasks_tracker is a django-rest-framework project.
The project is created for work with a database for effective monitoring management of employees tasks.
Main stack: Djangorestframework, Postgresql.

# Install and usage
1. Clone the project from https://github.com/Marat-Shainurov/drf_tasks_tracker to your local machine.

2. Build a new image and run the project container from the root project directory:
    - docker-compose build
    - docker-compose up

3. Read the project's documentation (swagger or redoc format):
    - http://127.0.0.1:8000/swagger/
    - http://127.0.0.1:8000/redoc/

4. Go to the main page on your browser http://127.0.0.1:8000/ and start working with the app's endpoints.

# Apps and models
1. tasks - tasks app.
    - Task - tasks model.
2. employees - employees app.
    - Employee - employee model.
3. users - users app.
    - CustomUser - customized User model.
    - UersManager class is overridden and customized as well (./users/manager.py).

# Fixture
You can load the fixture with several testing objects if necessary:
- docker-compose exec app python manage.py loaddata project_test_data.json
- Credentials:\
  {
  "email": "m_shainurov@mail.ru",
  "password": "123"
  }

# Testing
- All the endpoints are covered by pytest tests in <app_name>/test.py \
- Run tests:\
  docker-compose exec app python manage.py test
