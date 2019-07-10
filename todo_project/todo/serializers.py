# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers

from models import Todo, Enterprise, UserEnterprise


class EnterpriseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Enterprise
        fields = ('id', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserEnterpriseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserEnterprise
        fields = ('id', 'user', 'enterprise')


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'enterprise', 'text', 'status',
                  'author',
                  'performer',
                  'time_created', 'time_edited')