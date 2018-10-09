# coding=utf-8
from django import forms


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    code = forms.CharField(error_messages={"invalid": u"验证码错误"})
