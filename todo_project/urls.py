"""todo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from rest_framework import routers

from todo.base import LoginView, LoginViewJson
from todo import views
from settings import ENTERPRISE_PARAM

router = routers.DefaultRouter()
router.register(r'enterprise', views.EnterpriseViewSet)
router.register(r'user', views.UserViewSet)
# router.register(r'user-enterprise', views.UserEnterpriseViewSet)
router.register(r'enterprise/(?P<%s>.+)/todo' % ENTERPRISE_PARAM, views.TodoViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login-page'),
    url(r'^login/json/$', LoginViewJson.as_view(), name='login-page-json'),
    url(r'^logout/', logout, {'next_page': 'login-page'}),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('', include(router.urls)),
]
