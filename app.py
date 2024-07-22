from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Auston123!@127.0.0.1/e_commerce_api'

class Base(DeclarativeBase):
    pass

ma = Marshmallow(app)
db = SQLAlchemy(app, model_class=Base)
CORS(app)

# Schemas
class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("name", "email", "phone", "id")
        
class CustomerAccountSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    
    class Meta:
        fields = ("username", "password", "id")

class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    price = fields.String(required=True)
    
    class Meta:
        fields = ("name", "price", "id")

class OrderSchema(ma.Schema):
    orders = fields.String(required=True)
    track = fields.String(required=True)
    
    class Meta:
        fields = ("orders", "track", "id")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
customer_account_schema = CustomerAccountSchema()
customers_account_schema = CustomerAccountSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Database connection
db_name = "e_commerce_api"
user = "root"
password = "Auston123!"
host = "127.0.0.1"

try:
    conn = mysql.connector.connect(
        database=db_name,
        user=user,
        password=password,
        host=host
    )
    if conn.is_connected():
        print("Connected")
except Error as e:
    print(f"Error: {e}")

# Routes to PostMan
@app.route('/')
def home():
    return "Welcome Ecommerce Customers"

# Retrieve Customers/CustomerAccount/Products
@app.route("/customers", methods=["GET"])
def get_customers():
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM customers"
        cursor.execute(query)
        customers = cursor.fetchall()
        return customers_schema.jsonify(customers)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        

@app.route("/customeraccount", methods=["GET"])
def get_customer_account():
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM customeraccount"
        cursor.execute(query)
        customers_account = cursor.fetchall()
        return customers_account_schema.jsonify(customers_account)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

@app.route("/products", methods=["GET"])
def get_products():
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM products"
        cursor.execute(query)
        products = cursor.fetchall()
        return products_schema.jsonify(products)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

#@app.route("/orders", methods=["GET"])
#def get_orders():
    #try:
        #cursor = conn.cursor(dictionary=True)
       # query = "SELECT * FROM orders"
       # cursor.execute(query)
       # orders = cursor.fetchall()
        #return orders_schema.jsonify(orders)
    #except Error as e:
        #print(f"Error: {e}")
       # return jsonify({"error": "Internal server error"}), 500
  #  finally:
    #    cursor.close()

# Add customers/customer accounts/products          
@app.route("/customers", methods=["POST"])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        cursor = conn.cursor()
        new_customer = (customer_data['name'], customer_data['email'], customer_data['phone'])
        query = "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, new_customer)
        conn.commit()
        return jsonify({"message": "New customer added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

@app.route("/customeraccount", methods=["POST"])
def add_customer_account():
    try:
        customer_data = customer_account_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        cursor = conn.cursor()
        new_customer_account = (customer_data['username'], customer_data['password'])
        query = "INSERT INTO customeraccount (username, password) VALUES (%s, %s)"
        cursor.execute(query, new_customer_account)
        conn.commit()
        return jsonify({"message": "New customer account added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

@app.route("/products", methods=["POST"])
def add_products():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        cursor = conn.cursor()
        new_product = (product_data['name'], product_data['price'])
        query = "INSERT INTO products (name, price) VALUES (%s, %s)"
        cursor.execute(query, new_product)
        conn.commit()
        return jsonify({"message": "New product added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

# Update customers, customer accounts, products
@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        cursor = conn.cursor()
        updated_customer = (customer_data['name'], customer_data['email'], customer_data['phone'], id)
        query = "UPDATE customers SET name = %s, email = %s, phone = %s WHERE id = %s"
        cursor.execute(query, updated_customer)
        conn.commit()
        return jsonify({"message": "Customer updated successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

@app.route("/customeraccount/<int:id>", methods=["PUT"])
def update_customer_account(id):
    try:
        customer_data = customer_account_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        cursor = conn.cursor()
        updated_customer_account = (customer_data['username'], customer_data['password'], id)
        query = "UPDATE customeraccount SET username = %s, password = %s WHERE id = %s"
        cursor.execute(query, updated_customer_account)
        conn.commit()
        return jsonify({"message": "Customer account updated successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        cursor = conn.cursor()
        updated_product = (product_data['name'], product_data['price'], id)
        query = "UPDATE products SET name = %s, price = %s WHERE id = %s"
        cursor.execute(query, updated_product)
        conn.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

# Delete customer, customer account, products
@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        cursor.execute("DELETE FROM customers WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"message": "Customer removed successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

@app.route("/customeraccount/<int:id>", methods=["DELETE"])
def delete_customer_account(id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customeraccount WHERE id = %s", (id,))
        customer_account = cursor.fetchone()
        if not customer_account:
            return jsonify({"error": "Customer account not found"}), 404
        cursor.execute("DELETE FROM customeraccount WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"message": "Customer account removed successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"message": "Product removed successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
