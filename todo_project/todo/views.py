# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import viewsets

from base import BaseEnterpriseMixin
from models import Todo, Enterprise, UserEnterprise
from serializers import TodoSerializer, UserSerializer, EnterpriseSerializer, UserEnterpriseSerializer


class EnterpriseViewSet(BaseEnterpriseMixin, viewsets.ModelViewSet):
    """ ModelViewSet Предприятия """
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer

    def get_queryset(self):
        return Enterprise.objects.filter(id=self.user_enterprise.id)


class TodoViewSet(BaseEnterpriseMixin, viewsets.ModelViewSet):
    """ ModelViewSet Задач """
    queryset = Todo.objects.all().order_by('-time_created')
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(enterprise=self.user_enterprise)


class UserViewSet(BaseEnterpriseMixin, viewsets.ModelViewSet):
    """ ModelViewSet Юзеров """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserEnterpriseViewSet(BaseEnterpriseMixin, viewsets.ModelViewSet):
    """ ModelViewSet Юзеров предприятия """
    queryset = UserEnterprise.objects.all()
    serializer_class = UserEnterpriseSerializer



