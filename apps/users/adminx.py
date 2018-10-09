# coding=utf-8
import xadmin
from xadmin import views
from .models import VerifyCode, UserProfile


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "高通量药物筛选平台"
    site_footer = "药物筛选平台"
    menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'email', 'add_time']
    search_fields = ['code', 'email', 'add_time']
    list_filter = ['code', 'email', 'add_time']


class UserProfileAdmin(object):
    list_display = ['name', 'mobile', 'email', 'work_org', 'research_dir', 'add_time']
    search_fields = ['name', 'mobile', 'email', 'work_org', 'research_dir', 'add_time']
    list_filter = ['name', 'mobile', 'email', 'work_org', 'research_dir', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

