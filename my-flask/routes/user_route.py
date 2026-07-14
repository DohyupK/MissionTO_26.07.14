from flask import Blueprint, jsonify,request
import db # 루트 경로의 db.py를 임포트

# Blueprint 객체 생성
user_bp = Blueprint('user_route', __name__, url_prefix='/api/user')

# 회원가입
@user_bp.route('/create', methods=['POST'])
def create():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            data = request.get_json()
            id = data.get('id')
            pw = data.get('pw')
            nick = data.get('nick')
            address = data.get('address')
            point = data.get('point')

            # ID 중복 체크
            cursor.execute("SELECT * FROM user WHERE id = %s", (id,))
            user = cursor.fetchone()
            if user:
                return jsonify({'data':None,'success':False,'message':'중복된 ID'})
            
            # 닉네임 중복 체크
            cursor.execute("SELECT * FROM user WHERE nick = %s", (nick,))
            user = cursor.fetchone()
            if user:
                return jsonify({'data':None,'success':False,'message':'중복된 닉네임'})

            # 필수 입력 항목 체크
            if not id or not pw or not nick:
                return jsonify({'data':None,'success':False,'message':'필수 입력 항목 누락'})

            cursor.execute("""
            INSERT INTO user (id, pw, nick, address, created_at, point)
            VALUES
            (%s, %s, %s, %s, NOW(), %s)
            """, (id,pw,nick,address,point))
            conn.commit()
            return jsonify({'data':None,'success':True,'message':'회원가입 성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'회원가입 실패, 내부 서버에러','error':str(e)})
    finally:
        db.close_db()

# query string 방식으로 id 조회
@user_bp.route('/get-user-by-id', methods=['GET'])
def get_user_by_id():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            id = request.args.get('id')
            cursor.execute("SELECT * FROM user WHERE id = %s", (id,))
            user = cursor.fetchone()
            return jsonify({'data':user,'success':True,'message':'회원조회 성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'회원조회 실패, 내부 서버에러','error':str(e)})
    finally:
        db.close_db()

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            id = request.args.get('id')
            pw = request.args.get('pw')
            cursor.execute("SELECT * FROM user WHERE id = %s and pw = %s", (id,pw,))
            user = cursor.fetchone()
            return jsonify({'data':user,'success':True,'message':'회원조회 성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'회원조회 실패, 내부 서버에러','error':str(e)})
    finally:
        db.close_db()

# idx로 회원조회
@user_bp.route('/get-user/<idx>', methods=['GET'])
def get_user(idx):
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE idx = %s", (idx,))
            user = cursor.fetchone()
            return jsonify({'data':user,'success':True,'message':'회원조회 성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'회원조회 실패, 내부 서버에러','error':str(e)})
    finally:
        db.close_db()

# 회원조회
@user_bp.route('/all', methods=['GET'])
def get_all_users():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM user")
            users = cursor.fetchall()
            return jsonify({'data':users,'success':True,'message':'회원 전체 조회 성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'회원조회 실패, 내부 서버에러','error':str(e)})
    finally:
        db.close_db()

@user_bp.route('/test', methods=['GET'])
def test():
    return 'Hello, World!'