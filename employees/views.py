from django.db.models import Count
from django.shortcuts import render
from rest_framework import generics

from employees.models import Employee
from employees.serializers import EmployeeSerializer, EmployeeBusynessSerializer


class EmployeeCreateAPIView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer


class EmployeeListAPIView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeBusynessListAPIView(generics.ListAPIView):
    serializer_class = EmployeeBusynessSerializer
    queryset = Employee.objects.annotate(tasks_count=Count('executor_tasks')).order_by('-tasks_count')


class EmployeeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
