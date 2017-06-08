import pymysql


def db_connection():
    return pymysql.connect("YOUR_HOST", "YOUR_USER", "YOUR_PASSWORD", "YOUR_USERNAME", charset='utf8')
