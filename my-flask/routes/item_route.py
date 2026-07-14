from flask import Blueprint, jsonify,request
import db # 루트 경로의 db.py를 임포트

# Blueprint 객체 생성
item_bp = Blueprint('item_route', __name__, url_prefix='/api/item')

# 상품조회
@item_bp.route('/', methods=['GET'])
def item_all():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM item")
            item = cursor.fetchall()
            return jsonify({'data':item,'success':True,'message':'성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'실패','error':str(e)})
    finally:
        db.close_db()

# 상품등록
@item_bp.route('/insert', methods=['POST'])
def item_insert():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            data = request.get_json()
            item_name = data.get('name')
            item_price = data.get('price')
            item_maker = data.get('maker')
            item_stock = data.get('stock')

            cursor.execute("""
                INSERT INTO item(name,price,created_at,maker,stock)
                VALUES(%s,%s,NOW(),%s,%s)
            """,(item_name,item_price,item_maker,item_stock))
            conn.commit()
            return jsonify({'data':None,'success':True,'message':'성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'실패','error':str(e)})
    finally:
        db.close_db()

# 상품명으로 조회
@item_bp.route('/search', methods=['GET'])
def item_search():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            name = request.args.get('name')
            cursor.execute("SELECT * FROM item WHERE name = %s", (name,))
            item = cursor.fetchall()
            return jsonify({'data':item,'success':True,'message':'성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'실패','error':str(e)})
    finally:
        db.close_db()
        

# 상품삭제
@item_bp.route('/delete', methods=['POST'])
def item_delete():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            data = request.get_json()
            idx = data.get('idx')
            cursor.execute("SELECT idx,name,stock FROM item")
            item = cursor.fetchall()

            cursor.execute("DELETE FROM item WHERE idx = %s", (idx,))
            conn.commit()
            return jsonify({'data':item,'success':True,'message':'성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'실패','error':str(e)})
    finally:
        db.close_db()


# 상품 정보 변경
@item_bp.route('/update', methods=['POST'])
def item_update():
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            data = request.get_json()
            idx = data.get('idx')
            name = data.get('name')
            price = data.get('price')
            maker = data.get('maker')
            stock = data.get('stock')
            cursor.execute("SELECT name, price, maker, stock FROM item WHERE idx = %s", (idx,))
            item = cursor.fetchone()

            cursor.execute("""
                UPDATE item
                SET name = %s, price = %s, maker = %s, stock = %s
                WHERE idx = %s
            """, (name if name is not None else item['name'],
                  price if price is not None else item['price'],
                  maker if maker is not None else item['maker'],
                  stock if stock is not None else item['stock'],
                  idx))
            conn.commit()
            return jsonify({'data':item,'success':True,'message':'성공'})
    except Exception as e:
        return jsonify({'data':[],'success':False,'message':'실패','error':str(e)})
    finally:
        db.close_db()