
#archivo creado por Peter_Code182 
# Example from youtube for a api in flask whit marshmellow and sqlalchemy librarys

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init App

app = Flask(__name__)

# @app.route('/hello',methods=['GET'])
# def get():
#     return jsonify({'msg':'hello word'})

basedir = os.path.abspath(os.path.dirname(__file__))
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)

# product class

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String)
    price = db.Column(db.String(200))
    qry = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#create a product

@app.route('/product',methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#get one product

@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = Product.query.get(id)    
    return product_schema.jsonify(product)

#update a product

@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    
    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.qty = request.json['qty']

   
    db.session.commit()

    return product_schema.jsonify(product)


#delete product

@app.route('/product/<id>',methods=['DELETE'])
def delet_product(id):
    product = Product.query.get(id)   
    db.session.delete(product)
    db.session.commit() 
    return product_schema.jsonify(product)


#get all products

@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
