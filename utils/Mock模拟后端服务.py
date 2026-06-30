from flask import Flask, jsonify, request
# Flask 是一个轻量级的 Python Web 框架

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
# 配置Flask的JSON编码设置：
# False表示允许JSON响应中包含非ASCII字符（如中文），确保中文正常显示

# 模拟数据库
orders = []
drivers = []


# 司机注册接口
@app.route('/driver', methods=['POST'])  # 1定义路由装饰器;2指定URL路径为'/driver';3只允许POST方法访问该接口
def register_driver():
    data = request.get_json()  # 从HTTP请求中解析JSON格式的数据体
    name = data.get('name')
    if not name:
        return jsonify({"code":205,"error": "司机姓名是必需的"}), 400  # 返回错误响应：JSON格式的错误信息和HTTP状态码400
    if len(name)<3:
        return jsonify({"code":205,"msg":"太小了"}),200  # 返回业务逻辑错误响应，HTTP状态码200但业务状态码205
    if len(name)>6:
        return jsonify({"code":206,"msg":"太大了"}),200
    driver = {
        "code":100,
        "id": len(drivers) + 1,
        "name": name,
        "available": True,
        "extends":{"type":1
                   },
        "token": "hrheerhefvhublhieripweheroiweugpwevwe79w8e",
        "msg":"用户注册成功"
    }
    drivers.append(driver)
    return jsonify(driver), 200

# 用户下单接口
@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    start_location = data.get('start_location')
    end_location = data.get('end_location')
    if not start_location or not end_location:
        return jsonify({"error": "起始位置和结束位置是必需的"}), 400
    order = {
        "id": len(orders) + 1,

        "start_location": start_location,
        "end_location": end_location,
        "status": "待接单",
        "driver": None
    }
    orders.append(order)
    return jsonify(order), 201

# 司机接单接口
@app.route('/order/<int:order_id>/accept', methods=['POST'])
def accept_order(order_id):
    data = request.get_json()
    driver_id = data.get('driver_id')
    driver = next((d for d in drivers if d["id"] == driver_id), None)
    order = next((o for o in orders if o["id"] == order_id), None)
    if not driver or not order:
        return jsonify({"error": "司机或订单不存在"}), 404
    if not driver["available"]:
        return jsonify({"error": "司机不可用"}), 400
    if order["status"] != "待接单":
        return jsonify({"error": "订单已被接单或已完成"}), 400
    order["status"] = "已接单"
    order["driver"] = driver["name"]
    driver["available"] = False
    return jsonify(order), 200

# 行程结束接口
@app.route('/order/<int:order_id>/complete', methods=['POST'])
def complete_order(order_id):
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "订单不存在"}), 404
    if order["status"] != "已接单":
        return jsonify({"error": "订单未被接单，无法完成行程"}), 400
    order["status"] = "已完成"
    driver = next((d for d in drivers if d["name"] == order["driver"]), None)
    if driver:
        driver["available"] = True
    return jsonify(order), 200

# 获取所有订单接口
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(debug=True)