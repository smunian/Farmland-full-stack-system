"""agriculture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# schema_view = get_schema_view(
#     openapi.Info(
#         title="API Title",
#         default_version='v1',
#         description="API Description",
#         terms_of_service="https://www.example.com/terms/",
#         contact=openapi.Contact(email="contact@django-rest-framework.dev"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )
import api.views

urlpatterns = [
    # path('swagger/json/', SpectacularJSONAPIView.as_view(), name='schema'),
    # # Optional UI:
    # path('swagger/ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('swagger/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # YOUR PATTERNS
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('', api.views.web_login),
    path('admin/', admin.site.urls),
    # 登入接口
    path('test/', api.views.web_login),
    # 鸿蒙app web端接口
    path('login/', api.views.login),
    path('forgot_password/', api.views.forgot_password),
    path('text_select/', api.views.text_select),
    path('cgq/', api.views.cgq),
    path('water/status/', api.views.water_status),
    path('selecet/list/', api.views.agriculture_list),
    path('wate/time/', api.views.wate_time),
    path('guangai/time/', api.views.guangai_time),
    path('histry/data/', api.views.histry_data),
    # 用户管理界面
    path('index/', api.views.index, name='index'),
    path('user/add/', api.views.add),
    path('user/<int:nid>/edit/', api.views.updata),
    path('user/delete/', api.views.delete),
    path('datadisplay/', api.views.datadisplay_no_param, name='datadisplay_no_param'),
    path('datadisplay/<str:param>/', api.views.datedisplay, name='datadisplay'),
    path('farmland/', api.views.farmland, name='farmland'),
    path('farmland//farmland_delete/', api.views.farmland_delete),
    path('farmland/farmland_add/', api.views.farmland_add),
    path('Valve/', api.views.Valve),
    path('threshold/', api.views.threshold),
    # 后端接口
    path('user/login/', api.views.api_login),  # 用户登入
    path('add/', api.views.add_user),  # 用户登入
    path('device/', api.views.device_data),
]
