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
                     'deadline': self.valid_deadline + timedelta(hours=2), 'is_active': True}
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


class ActiveImportantTasksTests(APITestCase):

    def setUp(self):
        self.user_data = {'email': 'testing@mail.com', 'password': '123'}
        self.user = CustomUser.objects.create(**self.user_data)
        self.client.force_authenticate(user=self.user)
        self.valid_deadline = datetime.now(pytz.UTC) + timedelta(hours=9)

        e1_data = {'name': 'Test1', 'surname': 'Test1', 'position': 'TestP', 'is_active': True}
        e2_data = {'name': 'Test2', 'surname': 'Test2', 'position': 'TestP', 'is_active': True}
        e3_data = {'name': 'Test3', 'surname': 'Test3', 'position': 'TestP', 'is_active': True}
        self.e1, self.e2, self.e3 = Employee.objects.create(**e1_data), Employee.objects.create(
            **e2_data), Employee.objects.create(**e3_data)

        t1_data = {'title': 'Task1', 'description': 'T', 'executor': self.e1, 'deadline': self.valid_deadline,
                   'is_active': True, 'status': 'in_progress'}
        self.t1 = Task.objects.create(**t1_data)
        t2_data = {'title': 'Task2', 'description': 'T', 'executor': self.e2, 'deadline': self.valid_deadline,
                   'is_active': True, 'parent_task': self.t1, 'status': 'in_progress'}
        self.t2 = Task.objects.create(**t2_data)
        t3_data = {'title': 'Task3', 'description': 'T', 'executor': self.e3, 'deadline': self.valid_deadline,
                   'is_active': True, 'parent_task': self.t2, 'status': 'in_progress'}
        self.t3 = Task.objects.create(**t3_data)
        t4_data = {'title': 'Task4', 'description': 'T', 'deadline': self.valid_deadline,
                   'is_active': True, 'parent_task': self.t3, 'executor': self.e1}
        self.t4 = Task.objects.create(**t4_data)
        t5_data = {'title': 'Task5', 'description': 'T', 'deadline': self.valid_deadline,
                   'is_active': True, 'parent_task': self.t4, 'executor': self.e1, 'status': 'in_progress'}
        self.t5 = Task.objects.create(**t5_data)
        t6_data = {'title': 'Task6', 'description': 'T', 'deadline': self.valid_deadline,
                   'is_active': True, 'parent_task': self.t4, 'executor': self.e2, 'status': 'in_progress'}
        self.t6 = Task.objects.create(**t6_data)

    def test_active_task_list(self):
        response = self.client.get('http://localhost:8000/tasks/active/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()['results']), 6)
        self.t5.status = 'done'
        self.t5.save()
        response = self.client.get('http://localhost:8000/tasks/active/')
        self.assertEquals(len(response.json()['results']), 5)
        self.assertEquals(response.json()['results'][-1]['title'], 'Task6')
        self.assertEquals(response.json()['results'][-2]['title'], 'Task4')

    def test_active_with_parents(self):
        self.t6.status = 'done'
        self.t6.save()
        response = self.client.get('http://localhost:8000/tasks/active/with-parents/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.json()['results']), 4)
        self.assertEquals(response.json()['results'][-1]['title'], 'Task5')
        self.assertEquals(response.json()['results'][-2]['title'], 'Task4')
        self.assertEquals(response.json()['results'][0]['id'], self.t2.pk)

    def test_active_with_parents_executor(self):
        response = self.client.get('http://localhost:8000/tasks/active/with-parents/with-executor/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []})

        self.t6.status = 'created'
        self.t6.executor = None
        self.t6.save()

        response = self.client.get('http://localhost:8000/tasks/active/with-parents/with-executor/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['results'][0]['id'], self.t6.pk)
        self.assertEquals(response.json()['results'][0]['employee_for_task'], ['Test1 Test1'])
