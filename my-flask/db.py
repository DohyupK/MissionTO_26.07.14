import pymysql
from flask import g

# 1. DB 설정 정보 (실무에서는 환경 변수나 config 파일로 분리하는 것을 추천합니다)
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'db': 'shop_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

DB_CONFIG_IRIS = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'db': 'iris',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
def get_db_IRIS():
    if 'db' not in g:
        g.db = pymysql.connect(**DB_CONFIG_IRIS)
    return g.db
def close_db_IRIS(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def get_db():
    """요청당 하나의 DB 연결을 생성하고 반환합니다."""
    if 'db' not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db

def close_db(e=None):
    """요청 처리가 끝나면 DB 연결을 안전하게 종료합니다."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """
    Flask 앱(app) 객체를 받아, 앱이 종료되거나 요청이 끝날 때 
    자동으로 close_db 함수가 실행되도록 등록합니다.
    """
    app.teardown_appcontext(close_db)