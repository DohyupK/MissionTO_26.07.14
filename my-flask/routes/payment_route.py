from flask import Blueprint, jsonify, request
import db # 루트 경로의 db.py를 임포트

payment_bp = Blueprint('payment_route', __name__, url_prefix='/api/payment')

#결제 로직
@payment_bp.route('/buy-item', methods=['POST'])
def buy_item():
    try:
        data = request.get_json()
        item_idx = data.get('item_idx') #상품 인덱스
        user_idx = data.get('user_idx') #구매자 인덱스
        count = data.get('count') #구매 수량

        #필수 입력 항목 체크
        if not item_idx or not user_idx or not count:
            return jsonify({
                'data': None,
                'success': False,
                'message': 'item_idx, user_idx, count 필수 입력 항목을 확인해주세요'
            })
        
        user=None
        item=None
            
        #idx로 회원조회, 상품조회    
        conn = db.get_db()
        with conn.cursor() as cursor:

            #회원조회
            cursor.execute("SELECT * FROM user WHERE idx = %s", (user_idx,))
            user = cursor.fetchone()
            if not user:
                return jsonify({'data': None, 'success': False, 'message': '회원이 존재하지 않습니다'})

            #상품조회
            cursor.execute("SELECT * FROM item WHERE idx = %s", (item_idx,))
            item = cursor.fetchone()
            if not item:
                return jsonify({'data': None, 'success': False, 'message': '상품이 존재하지 않습니다'})
            
            #가격 비교
            total_price = item['price'] * count

            if user['point'] < total_price:
                return jsonify({'data': None, 'success': False, 'message': '포인트가 부족합니다'})
            
            #재고 체크
            if item['stock'] < count:
                return jsonify({'data': None, 'success': False, 'message': '상품 재고가 부족합니다'})

            #결제 로직
            cursor.execute("UPDATE user SET point = point - %s WHERE idx = %s", (total_price, user_idx))
            cursor.execute("UPDATE item SET stock = stock - %s WHERE idx = %s", (count, item_idx))
            cursor.execute("""
            INSERT INTO payment 
            (user_idx, item_idx, count, total_price, created_at) 
            VALUES (%s, %s, %s, %s, now())""", (user_idx, item_idx, count, total_price))
            conn.commit()
            return jsonify({'data': None, 'success': True, 'message': '결제 성공'})
        
    except Exception as e:
        conn.rollback()
        return jsonify({'data': [],'success': False,'message': '결제 실패, 내부 서버에러','error': str(e)
        })
    finally:
        db.close_db()


# user_idx로 결제 내역 조회
@payment_bp.route('/get-payment-history/<user_idx>', methods=['GET'])    
def get_payment_history(user_idx):
    try:
        conn = db.get_db()
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM payment AS p
            INNER JOIN user AS u
            ON p.user_idx = u.idx
            INNER JOIN item AS i
            ON p.item_idx = i.idx
            WHERE user_idx = %s""", (user_idx,))
            payments = cursor.fetchall()
            return jsonify({'data': payments,'success': True,'message': '결제 내역 조회 성공'})
    except Exception as e:
        return jsonify({
            'data': [],'success': False,'message': '결제 내역 조회 실패, 내부 서버에러','error': str(e)
        })    
    finally:
        db.close_db()