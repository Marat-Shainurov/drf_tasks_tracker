from django.shortcuts import render
from rest_framework import generics

from employees.models import Employee
from employees.serializers import EmployeeSerializer


class EmployeeCreateAPIView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer


class EmployeeListAPIView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
