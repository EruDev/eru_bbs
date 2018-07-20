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
