from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Gitkoding2024$@localhost/factory_management_system'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255))
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    order_date = db.Column(db.Date)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2))

@app.route('/orders', methods=['GET', 'POST'])
def manage_orders():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        orders = Order.query.paginate(page=page, per_page=per_page, error_out=False)
        results = [{'id': o.id, 'customer_name': o.customer_name, 'product_id': o.product_id, 'quantity': o.quantity, 'order_date': o.order_date.isoformat()} for o in orders.items]
        return jsonify({'orders': results, 'total': orders.total, 'pages': orders.pages, 'current_page': orders.page})
    
    if request.method == 'POST':
        data = request.get_json()
        if not all(key in data for key in ['customer_name', 'product_id', 'quantity', 'order_date']):
            return jsonify({'message': 'Missing data'}), 400
        
        new_order = Order(
            customer_name=data['customer_name'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            order_date=data['order_date']
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'id': new_order.id, 'message': 'Order created successfully'}), 201

@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        results = [{'id': p.id, 'name': p.name, 'price': str(p.price)} for p in products.items]
        return jsonify({'products': results, 'total': products.total, 'pages': products.pages, 'current_page': products.page})

    if request.method == 'POST':
        data = request.get_json()
        if not all(key in data for key in ['name', 'price']):
            return jsonify({'message': 'Missing data'}), 400
        
        new_product = Product(
            name=data['name'],
            price=data['price']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'id': new_product.id, 'message': 'Product created successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
