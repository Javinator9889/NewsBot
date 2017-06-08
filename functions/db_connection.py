import pymysql


def db_connection():
    return pymysql.connect("localhost", "javialonso", "p@ssw0rd", "javialonso", charset='utf8')
