import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 使用当前路径
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'ASDWJDJnasdjniwASDansdnkw'
HOST = "127.0.0.1"
PORT = 3306
USERNAME = ""
PASSWD = ""
DATABASE = ""
# SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWD, HOST, PORT, DATABASE)