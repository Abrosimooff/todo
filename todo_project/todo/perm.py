# -*- coding:utf-8 -*-

from django.conf import settings

from models import UserEnterprise

ENTERPRISE_PARAM = settings.ENTERPRISE_PARAM


class EnterprisePerm(object):
    """ Проверки, связанные с организацией

        Авторизацию пользователя не проверяем т.к это делается ранее в
        rest_framework.permissions.IsAuthenticated
    """

    def has_permission(self, request, view):
        # Проверка обязательного присутствия enterprise_id в сессии пользователя
        session_enterprise_id = request.session.get(ENTERPRISE_PARAM)
        if not session_enterprise_id:
            return False

        # Проверка связки организации с пользователем
        if not UserEnterprise.objects.filter(user=request.user, enterprise_id=session_enterprise_id).exists():
            return False

        # Проверка view.kwargs.enterprise_id (если есть) на соответствие session_enterprise_id
        if view.kwargs.get(ENTERPRISE_PARAM):
            try:
                return int(view.kwargs.get(ENTERPRISE_PARAM, 0)) == session_enterprise_id
            except (ValueError, TypeError):
                return False
        return True

    def has_object_permission(self, request, view, obj):
        return True
