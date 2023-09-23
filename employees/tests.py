import datetime

import pytz
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks.models import Task
from users.models import CustomUser


class EmployeeTestCase(APITestCase):

    def setUp(self):
        self.user_data = {'email': 'testing@mail.com', 'password': '123'}
        self.user = CustomUser.objects.create(**self.user_data)
        self.client.force_authenticate(user=self.user)

        test_employee_data = {'name': 'TestN', 'surname': 'TestS', 'position': 'TestP', 'is_active': True}
        self.test_employee = Employee.objects.create(**test_employee_data)

    def test_employees_list(self):
        response = self.client.get('http://localhost:8000/employees/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Employee.objects.all().count(), 1)
        self.assertEquals(response.json()['results'][0]['name'], 'TestN')

    def test_create_employee(self):
        employee_data = {'name': 'Test creating', 'surname': 'Test', 'position': 'Test position', 'is_active': True}
        response = self.client.post('http://localhost:8000/employees/create/', data=employee_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Employee.objects.all().count(), 2)
        self.assertEquals(response.json()['name'], 'Test creating')
        self.assertEquals(response.json()['patronymic'], None)

    def test_patch_employee(self):
        employee_data = {'name': 'Test patch'}
        response = self.client.patch(f'http://localhost:8000/employees/update/{self.test_employee.pk}/',
                                     data=employee_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['name'], 'Test patch')
        self.assertEquals(response.json()['id'], self.test_employee.pk)

    def test_put_employee(self):
        employee_data = {'name': 'Test Put', 'surname': 'Test Put', 'position': 'Test Put', 'is_active': False}
        response = self.client.put(f'http://localhost:8000/employees/update/{self.test_employee.pk}/',
                                   data=employee_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['name'], 'Test Put')
        self.assertEquals(response.json()['surname'], 'Test Put')
        self.assertEquals(response.json()['is_active'], False)
        self.assertEquals(response.json()['id'], self.test_employee.pk)

    def test_retrieve_employee(self):
        response = self.client.get(f'http://localhost:8000/employees/retrieve/{self.test_employee.pk}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['results'][0]['name'], 'TestN')
        self.assertEquals(response.json()['results'][0]['surname'], 'TestS')
        self.assertEquals(response.json()['results'][0]['id'], self.test_employee.pk)
        self.assertEquals(len(response.json()['results']), 1)

    def test_delete_employee(self):
        self.user.is_staff = True
        response = self.client.delete(f'http://localhost:8000/employees/delete/{self.test_employee.pk}/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Employee.objects.all().count(), 0)


class EmployeesBusynessTestCase(APITestCase):

    def setUp(self):
        self.user_data = {'email': 'testing@mail.com', 'password': '123'}
        self.user = CustomUser.objects.create(**self.user_data)
        self.client.force_authenticate(user=self.user)
        valid_deadline = datetime.datetime.now(pytz.UTC) + datetime.timedelta(hours=9)

        e1_data = {'name': 'Test1', 'surname': 'Test1', 'position': 'TestP', 'is_active': True}
        e2_data = {'name': 'Test2', 'surname': 'Test2', 'position': 'TestP', 'is_active': True}
        e3_data = {'name': 'Test3', 'surname': 'Test3', 'position': 'TestP', 'is_active': True}
        e1, e2, e3 = Employee.objects.create(**e1_data), Employee.objects.create(**e2_data), Employee.objects.create(
            **e3_data),

        t1_data = {'title': 'Task1', 'description': 'T', 'executor': e1, 'deadline': valid_deadline,
                   'is_active': True, 'status': 'in_progress'}
        t1 = Task.objects.create(**t1_data)
        t2_data = {'title': 'Task2', 'description': 'T', 'executor': e2, 'deadline': valid_deadline,
                   'is_active': True, 'parent_task': t1, 'status': 'in_progress'}
        t2 = Task.objects.create(**t2_data)
        t3_data = {'title': 'Task3', 'description': 'T', 'executor': e3, 'deadline': valid_deadline,
                   'is_active': True, 'parent_task': t2, 'status': 'in_progress'}
        t3 = Task.objects.create(**t3_data)
        t4_data = {'title': 'Task4', 'description': 'T', 'deadline': valid_deadline,
                   'is_active': True, 'parent_task': t3, 'executor': e1}
        Task.objects.create(**t4_data)

    def test_employees_busyness(self):
        response = self.client.get('http://localhost:8000/employees/busyness/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()['results']), 3)
        self.assertEquals(response.json()['results'][0]['name'], 'Test1')
        self.assertEquals(len(response.json()['results'][0]['executor_tasks']), 2)
        self.assertEquals(response.json()['results'][1]['tasks_count'], 1)
        self.assertEquals(len(response.json()['results'][1]['executor_tasks']), 1)
        self.assertEquals(response.json()['results'][2]['tasks_count'], 1)
        self.assertEquals(len(response.json()['results'][2]['executor_tasks']), 1)
