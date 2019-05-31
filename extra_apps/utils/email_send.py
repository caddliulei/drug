# coding:utf-8
from __future__ import unicode_literals
from django.core.mail import send_mail
from drug.settings import EMAIL_FROM


def email_send(email, code, send_type="register"):

    if send_type == "register":
        email_title = "邮箱注册验证码"
        email_body = "注册高通量药物筛选平台邮箱验证码为 %s" % code

        send_status = send_mail(subject=email_title, message=email_body,
                                from_email=EMAIL_FROM,
                                recipient_list=[email])
        return send_status
    elif send_type == "forget":
        email_title = "邮箱找回验证码"
        email_body = "重置高通量药物筛选平台邮箱验证码为 %s" % code

        send_status = send_mail(subject=email_title, message=email_body,
                                from_email=EMAIL_FROM, recipient_list=[email])
        return send_status


def email_status(email):
    email_title = '虚拟筛选服务器'
    email_body = '您的任务已经完成,请登录网站查看'
    send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
    return send_status
