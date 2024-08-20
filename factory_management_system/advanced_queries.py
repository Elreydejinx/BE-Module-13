from app import app, db, Order, Product, Production, Employee
from flask import jsonify, request

@app.route('/employee_performance', methods=['GET'])
def employee_performance():
    query = db.session.query(Employee.name, db.func.sum(Production.quantity).label('total_quantity')) \
        .join(Production, Employee.id == Production.employee_id) \
        .group_by(Employee.name).all()
    results = [{'employee': e.name, 'total_quantity': e.total_quantity} for e in query]
    return jsonify(results)

@app.route('/top_selling_products', methods=['GET'])
def top_selling_products():
    query = db.session.query(Product.name, db.func.sum(Order.quantity).label('total_quantity')) \
        .join(Order, Product.id == Order.product_id) \
        .group_by(Product.name) \
        .order_by(db.func.sum(Order.quantity).desc()).all()
    results = [{'product': p.name, 'total_quantity': p.total_quantity} for p in query]
    return jsonify(results)

@app.route('/customer_lifetime_value', methods=['GET'])
def customer_lifetime_value():
    threshold = request.args.get('threshold', 1000, type=float)
    query = db.session.query(Order.customer_name, db.func.sum(Order.quantity * Product.price).label('total_value')) \
        .join(Product, Order.product_id == Product.id) \
        .group_by(Order.customer_name) \
        .having(db.func.sum(Order.quantity * Product.price) >= threshold).all()
    results = [{'customer': c.customer_name, 'total_value': str(c.total_value)} for c in query]
    return jsonify(results)

@app.route('/production_efficiency', methods=['GET'])
def production_efficiency():
    date = request.args.get('date')
    query = db.session.query(Product.name, db.func.sum(Production.quantity).label('total_quantity')) \
        .join(Production, Product.id == Production.product_id) \
        .filter(Production.production_date == date) \
        .group_by(Product.name).all()
    results = [{'product': p.name, 'total_quantity': p.total_quantity} for p in query]
    return jsonify(results)
