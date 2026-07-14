from flask import Flask
from routes.user_route import user_bp
from routes.ai_route import ai_bp
from routes.view_route import view_bp
from routes.test_route import test_bp
from routes.item_route import item_bp
from routes.payment_route import payment_bp
from routes.iris_route import iris_bp


app = Flask(__name__)

# 블루프린트 등록
app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(view_bp)
app.register_blueprint(test_bp)
app.register_blueprint(item_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(iris_bp)

if __name__ == '__main__':
    app.run(debug=True)