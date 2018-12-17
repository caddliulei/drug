# coding=utf-8
"""drug URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from __future__ import unicode_literals
from django.conf.urls import url, include
from drug.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from users.views import UserRegViewset, EmailCodeViewset, AutoDockOrderViewset, AutoDock2OrderViewset,\
    VirtualScreenOrderViewset, VirtualScreen2OrderViewset, UserinfoViewset, PasswordresetViewset
from works.views import BannerViewset, ProductViewset, AutoDockViewset, VirtualScreenViewset
from works.views import VsBlastViewset, ReverseVirtualScreenViewset, DynamicViewset, AdmetViewset
from works.views import AutoDock2Viewset, VirtualScreen2Viewset, ScreenViewset
import xadmin
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token


router = DefaultRouter()
# forgets = UserForGetPWViewset.as_view({
#     'post': 'update',
# })
router.register(r'codes', EmailCodeViewset, base_name='验证码')
router.register(r'banners', BannerViewset, base_name='首页轮播图')
router.register(r'products', ProductViewset, base_name='服务内容')
router.register(r'autodocts', AutoDockViewset, base_name='分子对接')
router.register(r'autodock2s', AutoDock2Viewset, base_name='分子对接2')
router.register(r'virtualscreens', VirtualScreenViewset, base_name='虚拟筛选')
router.register(r'virtualscreen2s', VirtualScreen2Viewset, base_name='虚拟筛选2')
router.register(r'vsleadblasts', VsBlastViewset, base_name='vsleadblast')
router.register(r'reversevirtualscreens', ReverseVirtualScreenViewset, base_name='反向虚拟筛选')
router.register(r'dynamics', DynamicViewset, base_name='动力学模拟')
router.register(r'admets', AdmetViewset, base_name='admet预测')
router.register(r'registers', UserRegViewset, base_name='用户注册')
router.register(r'autodockorders', AutoDockOrderViewset, base_name='autoduckorder')
router.register(r'autodock2orders', AutoDock2OrderViewset, base_name='autoduck2order')
router.register(r'virtualscreenorders', VirtualScreenOrderViewset, base_name='virtualscreenorders')
router.register(r'virtualscreen2orders', VirtualScreen2OrderViewset, base_name='virtualscreen2orders')
router.register(r'users', UserinfoViewset, base_name="user")
router.register(r'passwordreset', PasswordresetViewset, base_name='passwordreset')
router.register(r'screens', ScreenViewset, base_name='screen')


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^docs/', include_docs_urls(title="高通量药物筛选平台")),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^rest-auth/', include('rest_auth.urls')),
    ]
