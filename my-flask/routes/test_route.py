from flask import Blueprint, jsonify, request
import db # 루트 경로의 db.py를 임포트

# Blueprint 객체 생성
test_bp = Blueprint('test_route', __name__, url_prefix='/api/test')

# 3. body 방식 : 복합적(이미지) > 회원가입
@test_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    return f'회원가입 성공: {name},{email},{password}'

# 1-2 혼합
@test_bp.route('/tp/products/<product_id>', methods=['GET'])
def coupang(product_id):
    vendor_item_id = request.args.get('vendoritemid')
    source_Type = request.args.get('sourceType')
    # return f'제품 조회 성공 : {product_id,vendor_item_id,source_Type}'
    return jsonify({
        "success":True,
        "message":"제품 조회 성공, data는 제품 정보를 담고 있습니다.",
        "data":{
            "vendoritemid":vendor_item_id,
            "sourceType":source_Type,
            "productId":product_id
        }
    })

# 2. queary string 방식
@test_bp.route('/get-items', methods=['GET'])
def get_items():
    item_name = request.args.get('item_name')
    item_price = request.args.get('item_price')
    print(item_name)
    print(item_price)
    return '아이템 조회 성공'

# 1. params 방식
@test_bp.route('/get-user/<uid>', methods=['GET'])
def get_user(uid):
    print(uid)
    return '회원조회 성공'


@test_bp.route('/test', methods=['POST'])
def hello_world1():
    return 'hello flask'

@test_bp.route('/test2', methods=['GET'])
def hello_world2():
    return 'hello flask2'

@test_bp.route('/')
def hello_world():
    return 'Hello, World!'