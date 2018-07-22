# coding: utf-8
import os

# base64.b64encode(os.urandom(12))
SECRET_KEY = os.urandom(24)

DEBUG = True

# DB CONFIG
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'eru_bbs'

# mysql+pymysql://root:root@localhost:3306/eru_bbs?charset=utf8
DB_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 邮箱配置
# MAIL_USE_TLS: 端口号587
# MAIL_USE_SSL: 端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱服务器地址

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USERNAME = '1027926875@qq.com'
MAIL_PASSWORD = 'vbahjutuwthcbbch'
MAIL_DEFAULT_SENDER = '1027926875@qq.com'