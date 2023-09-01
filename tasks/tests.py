from datetime import datetime, timedelta
import pytz

from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Employee
from tasks.models import Task
from users.models import CustomUser


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user_data = {'email': 'testing@mail.com', 'password': '123'}
        self.user = CustomUser.objects.create(**self.user_data)
        self.client.force_authenticate(user=self.user)

        self.valid_deadline = datetime.now(pytz.UTC) + timedelta(hours=9)

        employee_data = {'name': 'Test', 'surname': 'Test', 'position': 'TestP', 'is_active': True}
        self.employee = Employee.objects.create(**employee_data)

        task_data = {'title': 'TaskTest', 'description': 'T', 'executor': self.employee, 'status': 'in_progress',
                     'deadline': self.valid_deadline, 'is_active': True}
        self.task = Task.objects.create(**task_data)

    def test_task_list(self):
        response = self.client.get('http://localhost:8000/tasks/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Task.objects.all().count(), 1)
        self.assertEquals(response.json()['results'][0]['title'], 'TaskTest')
        self.assertEquals(response.json()['results'][0]['executor'], self.employee.pk)

    def test_create_task(self):
        task_data = {'title': 'Test creating', 'description': 'T', 'executor': self.employee.pk,
                     'deadline': self.valid_deadline, 'is_active': True}
        response = self.client.post('http://localhost:8000/tasks/create/', data=task_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Task.objects.all().count(), 2)
        self.assertEquals(response.json()['title'], 'Test creating')
        self.assertEquals(response.json()['status'], 'created')
        self.assertEquals(response.json()['executor'], self.employee.pk)
        self.assertEquals(response.json()['owner'], self.user.pk)
        self.assertEquals(datetime.fromisoformat(response.json()['deadline']), self.valid_deadline)

    #
    def test_patch_task(self):
        task_data = {'title': 'Test patched'}
        response = self.client.patch(f'http://localhost:8000/tasks/update/{self.task.pk}/',
                                     data=task_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['title'], 'Test patched')
        self.assertEquals(response.json()['id'], self.task.pk)

    def test_put_task(self):
        task_data = {'title': 'Task put', 'description': 'T', 'executor': self.employee.pk, 'status': 'created',
                     'deadline': self.valid_deadline + timedelta(hours=2)}
        response = self.client.put(f'http://localhost:8000/tasks/update/{self.task.pk}/',
                                   data=task_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['title'], 'Task put')
        self.assertEquals(response.json()['status'], 'created')
        self.assertEquals(datetime.fromisoformat(response.json()['deadline']), self.valid_deadline + timedelta(hours=2))
        self.assertEquals(response.json()['id'], self.task.pk)

    def test_retrieve_task(self):
        response = self.client.get(f'http://localhost:8000/tasks/retrieve/{self.task.pk}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['title'], 'TaskTest')
        self.assertEquals(response.json()['description'], 'T')
        self.assertEquals(response.json()['id'], self.task.pk)

    def test_delete_task(self):
        self.user.is_staff = True
        response = self.client.delete(f'http://localhost:8000/tasks/delete/{self.task.pk}/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Task.objects.all().count(), 0)
