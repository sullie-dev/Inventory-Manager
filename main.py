from flask import Flask, render_template, redirect, flash, request
import os
import psycopg2
import random
import string

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

def keyGenerator():
	upper_string = string.ascii_uppercase
	lower_string = string.ascii_lowercase
	numerical = string.digits
	
	alphabet = upper_string + lower_string + numerical
	random_character = random.sample(alphabet, 12)
	key = "".join(random_character)
	return key

def connect_db():
	"""Connects to the database"""
	database_uri = os.environ['DATABASEURI']
	db_connection = psycopg2.connect(database_uri, sslmode="require")
	return db_connection


@app.route('/')
def index():
	connection = connect_db()
	cursor = connection.cursor()
	
	search_query = f"SELECT * FROM product"
	
	cursor.execute(search_query)
	connection.commit()
	
	product_result = cursor.fetchall()
	return render_template('index.html',page_title="Dukes Inventory", products = product_result)


@app.route('/shipments')
def shipments():
	return render_template('shipments.html', page_title="Dukes Shipments")

# Products
	
@app.route('/new-product')
def newProduct():
	return render_template('newproduct.html', page_title="New Product", page_function="Add product")


@app.route('/update-product/<product_key>')
def updateProduct(product_key):
	connection = connect_db()
	cursor = connection.cursor()
	
	search_query = f"SELECT * from product WHERE product_key='{product_key}'"
	
	cursor.execute(search_query)
	connection.commit()
	
	product_result = cursor.fetchall()
	
	return render_template('updateproduct.html', page_title="Update Product", page_function="Update product", product = product_result)


@app.route('/update-<product_key_update>', methods=("GET", "POST"))
def updateProductKey(product_key_update):
	db = connect_db()
	cursor = db.cursor()

	product_name = request.form.get('productTitle')
	product_qquantity = request.form.get('productQuantity')
	product_sku = request.form.get('productSKU')
	product_image = request.form.get('productMedia')
	product_description = request.form.get('productDescription')

	update_product_name_query = """UPDATE product SET product_name = %s WHERE product_key = %s"""
	update_product_qquantity_query = """UPDATE product SET product_qquantity = %s WHERE product_key = %s"""
	update_product_sku_query = """UPDATE product SET product_sku = %s WHERE product_key = %s"""
	update_product_image_query = """UPDATE product SET product_image = %s WHERE product_key = %s"""
	update_product_description_query = """UPDATE product SET product_description = %s WHERE product_key = %s"""
	
	cursor.execute(update_product_name_query, (product_name, product_key_update))
	cursor.execute(update_product_qquantity_query, (product_qquantity, product_key_update))
	cursor.execute(update_product_sku_query, (product_sku, product_key_update))
	cursor.execute(update_product_image_query, (product_image, product_key_update))
	cursor.execute(update_product_description_query, (product_description, product_key_update))
	
	db.commit()
	
	flash('Product updated sucessfully','success')
	return redirect('/')



@app.route('/create-product', methods=("GET", "POST"))
def createProdcut():
	db = connect_db()
	cursor = db.cursor()
	
	product_key = keyGenerator(),
	product_name = request.form.get('productTitle'),
	product_qquantity = request.form.get('productQuantity'),
	product_sku = request.form.get('productSKU'),
	product_image = request.form.get('productMedia'),
	product_description = request.form.get('productDescription')

	insert_query = """INSERT INTO product (product_key, product_name,product_qquantity,product_sku, product_image, product_description) VALUES (%s,%s,%s,%s,%s,%s)"""

	record_to_insert = (product_key, product_name,product_qquantity,product_sku, product_image, product_description)
	cursor.execute(insert_query, record_to_insert)
	db.commit()

	flash('Product created sucessfully','success')
	return redirect('/')


@app.route('/delete-<product_key>', methods=("GET", "POST"))
def delete(product_key):
	
		connection = connect_db()
		cursor = connection.cursor()
		# delete_query = """DELETE product
  #   WHERE product_key = %s"""
		delete_query = f""" DELETE from product WHERE product_key='{product_key}'"""
		cursor.execute(delete_query)
	
		connection.commit()

		flash('Product created deleted','success')
		return redirect('/')
# Shipments
		
@app.route('/new-shipment')
def newShipment():
	return render_template('newshipment.html', page_title="New Shipment", page_function="Add shipment")

@app.route('/update-shipment')
def updateShipment():
	return render_template('updateshipments.html', page_title="Update Shipment", page_function="Update shipment")

@app.route('/create-shipment', methods=("GET", "POST"))
def createShipment():
	flash('Shipment created sucessfully','success')
	return redirect('/')

app.run(host='0.0.0.0', port=81)
