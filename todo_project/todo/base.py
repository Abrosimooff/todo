# -*- coding:utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from common import JsonResponseMix
from models import Enterprise, UserEnterprise
from django.conf import settings

ENTERPRISE_PARAM = settings.ENTERPRISE_PARAM


class BaseEnterpriseMixin(object):
    """ Базовый миксин с user_enterprise """
    user_enterprise = None

    def dispatch(self, request, *args, **kwargs):
        if ENTERPRISE_PARAM in request.session:
            self.user_enterprise = Enterprise.objects.filter(pk=request.session[ENTERPRISE_PARAM]).first()
        return super(BaseEnterpriseMixin, self).dispatch(request, *args, **kwargs)


class EnterpriseAuthForm(AuthenticationForm):
    """  Базовая форма авторизации +  привязка к enterprise_id"""
    enterprise_id = forms.IntegerField()

    def clean_enterprise_id(self):
        enterprise = self.cleaned_data.get('enterprise_id')
        if not Enterprise.objects.filter(pk=enterprise).exists():
            raise ValidationError(u"Орагнизации не существует")
        return enterprise

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:

                # пробуем авторизовать по email
                try:
                    user_by_email = User.objects.get(email=username)
                    self.user_cache = authenticate(username=user_by_email.username, password=password)
                except (User.DoesNotExist, User.MultipleObjectsReturned):
                    pass

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        if not UserEnterprise.objects.filter(user=self.user_cache, enterprise_id=self.cleaned_data['enterprise_id']).exists():
            raise forms.ValidationError(
                u'Пользователю нельзя авторизоваться в данную организацию',
                code='login_protect',
            )
        return self.cleaned_data


class LoginView(TemplateView):
    """  View авторизации для браузера """
    http_method_names = ['get', 'post']
    template_name = 'todo/login.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return self.success_response()
        return super(LoginView, self).get(request, *args, **kwargs)

    def success_response(self):
        return HttpResponseRedirect('/')

    def fail_response(self, form):
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        login_form = EnterpriseAuthForm(data=self.request.POST)
        if login_form.is_valid():
            from django.contrib.auth import login
            login(request, login_form.get_user())
            # записываем в сессию id предприятия, на которое залогинились
            self.request.session[ENTERPRISE_PARAM] = login_form.cleaned_data[ENTERPRISE_PARAM]
            return self.success_response()
        else:
            return self.fail_response(login_form)


class LoginViewJson(JsonResponseMix, LoginView):
    """  View авторизации c json-ответами  """

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return self.success_response()
        return self.render_to_response({})

    def success_response(self):
        return self.render_to_response({'success': True})

    def fail_response(self, form):
        return self.render_to_response({'success': False, 'errors': form.errors.as_json()})