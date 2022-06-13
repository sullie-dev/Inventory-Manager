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
    return render_template('index.html',
                           page_title="Dukes Inventory",
                           products=product_result)


@app.route('/shipments')
def shipments():

    connection = connect_db()
    cursor = connection.cursor()

    search_query = f"SELECT * FROM shipment"

    cursor.execute(search_query)
    connection.commit()

    shipments_result = cursor.fetchall()
    print(shipments_result)
    return render_template('shipments.html',
                           page_title="Dukes Shipments",
                           shipments=shipments_result)


# Products


@app.route('/new-product')
def newProduct():

	connection = connect_db()
	cursor = connection.cursor()
	
	location_query = f"SELECT * FROM location"
	
	cursor.execute(location_query)
	connection.commit()

	locatios_result = cursor.fetchall()
	
	return render_template('newproduct.html',
                           page_title="New Product",page_function="Add product", locations = locatios_result)


@app.route('/update-product/<product_key>')
def updateProduct(product_key):
    connection = connect_db()
    cursor = connection.cursor()

    product_query = f"SELECT * from product WHERE product_key='{product_key}'"

    cursor.execute(product_query)
    connection.commit()

    product_result = cursor.fetchall()

    location_query = f"SELECT * from location"
    cursor.execute(location_query)
    connection.commit()

    location_result = cursor.fetchall()

    return render_template('updateproduct.html',
                           page_title="Update Product",
                           page_function="Update product",
                           product=product_result, locations = location_result)


@app.route('/update-<product_key_update>', methods=("GET", "POST"))
def updateSingleProduct(product_key_update):
    db = connect_db()
    cursor = db.cursor()

    product_name = request.form.get('productTitle')
    product_qquantity = request.form.get('productQuantity')
    product_sku = request.form.get('productSKU')
    product_image = request.form.get('productMedia')
    product_description = request.form.get('productDescription')
    product_location = request.form.get('productLocation')

    update_product_name_query = """UPDATE product SET product_name = %s WHERE product_key = %s"""
    update_product_qquantity_query = """UPDATE product SET product_qquantity = %s WHERE product_key = %s"""
    update_product_sku_query = """UPDATE product SET product_sku = %s WHERE product_key = %s"""
    update_product_image_query = """UPDATE product SET product_image = %s WHERE product_key = %s"""
    update_product_description_query = """UPDATE product SET product_description = %s WHERE product_key = %s"""
    update_product_location_query = """UPDATE product SET product_location = %s WHERE product_key = %s"""

    cursor.execute(update_product_name_query,
	                   (product_name, product_key_update))
    cursor.execute(update_product_qquantity_query,
	                   (product_qquantity, product_key_update))
    cursor.execute(update_product_sku_query, (product_sku, product_key_update))
    cursor.execute(update_product_image_query,
	                   (product_image, product_key_update))
    cursor.execute(update_product_description_query,
	                   (product_description, product_key_update))
    cursor.execute(update_product_location_query,
	                   (product_location, product_key_update))
	
    db.commit()
	
    flash('Product updated sucessfully', 'success')
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
  product_description = request.form.get('productDescription'), 
  product_location = request.form.get('productLocation'),

  insert_query = """INSERT INTO product (product_key, product_name,product_qquantity,product_sku, product_image, product_description, product_location) VALUES (%s,%s,%s,%s,%s,%s,%s)"""

  record_to_insert = (product_key, product_name, product_qquantity,
                        product_sku, product_image, product_description, product_location)
  cursor.execute(insert_query, record_to_insert)
  db.commit()

  flash('Product created sucessfully', 'success')
  return redirect('/')


@app.route('/delete-<product_key>', methods=("GET", "POST"))
def deleteProduct(product_key):

    connection = connect_db()
    cursor = connection.cursor()
    delete_query = f""" DELETE from product WHERE product_key='{product_key}'"""
    cursor.execute(delete_query)

    connection.commit()

    flash('Product created deleted', 'success')
    return redirect('/')


# Shipments


@app.route('/new-shipment')
def newShipment():
    return render_template('newshipment.html',
                           page_title="New Shipment",
                           page_function="Add shipment")


@app.route('/create-shipment', methods=("GET", "POST"))
def createShipment():
    db = connect_db()
    cursor = db.cursor()

    shipment_key = keyGenerator(),
    shipment_name = request.form.get('shipmentTitle'),
    shipment_tracking = request.form.get('shipmentTracking'),
    shipment_delivery_date = request.form.get('shipmentDeliveryDate'),
    shipment_status = bool(request.form.get('shipmentStatus')),
    shipment_description = request.form.get('shipmentDescription')

    insert_query = """INSERT INTO shipment (shipment_key, shipment_name,shipment_tracking,shipment_delivery_date, shipment_status, shipment_description) VALUES (%s,%s,%s,%s,%s,%s)"""

    record_to_insert = (shipment_key, shipment_name, shipment_tracking,
                        shipment_delivery_date, shipment_status,
                        shipment_description)

    cursor.execute(insert_query, record_to_insert)
    db.commit()

    flash('Shipment created sucessfully', 'success')
    return redirect('/shipments')


@app.route('/update-shipment/<shipment_key>')
def updateShipment(shipment_key):
    connection = connect_db()
    cursor = connection.cursor()

    search_query = f"SELECT * from shipment WHERE shipment_key='{shipment_key}'"

    cursor.execute(search_query)
    connection.commit()

    shipment_result = cursor.fetchall()

    print(shipment_result)

    return render_template('updateshipments.html',
                           page_title="Update Shipment",
                           page_function="Update Shipment",
                           shipment=shipment_result)


@app.route('/update-shipment/<shipment_key>', methods=("GET", "POST"))
def updateSingleShipment(shipment_key):
    db = connect_db()
    cursor = db.cursor()

    shipment_name = request.form.get('shipmentTitle'),
    shipment_tracking = request.form.get('shipmentTracking'),
    shipment_delivery_date = request.form.get('shipmentDeliveryDate'),
    shipment_status = bool(request.form.get('shipmentStatus')),
    shipment_description = request.form.get('shipmentDescription')

    update_shipment_name_query = """UPDATE shipment SET shipment_name = %s WHERE shipment_key = %s"""
    update_shipment_tracking_query = """UPDATE shipment SET shipment_tracking = %s WHERE shipment_key = %s"""
    shipment_delivery_date_query = """UPDATE shipment SET shipment_delivery_date = %s WHERE shipment_key = %s"""
    shipment_status_query = """UPDATE shipment SET shipment_status = %s WHERE shipment_key = %s"""
    update_shipment_description_query = """UPDATE shipment SET shipment_description = %s WHERE shipment_key = %s"""

    cursor.execute(update_shipment_name_query, (shipment_name, shipment_key))
    cursor.execute(update_shipment_tracking_query,
                   (shipment_tracking, shipment_key))
    cursor.execute(shipment_delivery_date_query,
                   (shipment_delivery_date, shipment_key))

    cursor.execute(shipment_status_query, (shipment_status, shipment_key))
    cursor.execute(update_shipment_description_query,
                   (shipment_description, shipment_key))

    db.commit()

    flash('Shipment updated sucessfully', 'success')
    return redirect('/shipments')


@app.route('/delete-shipment-<shipment_key>', methods=("GET", "POST"))
def deleteShipment(shipment_key):

    connection = connect_db()
    cursor = connection.cursor()
    # delete_query = """DELETE product
    #   WHERE product_key = %s"""
    delete_query = f""" DELETE from shipment WHERE shipment_key='{shipment_key}'"""
    cursor.execute(delete_query)

    connection.commit()

    flash('Shipment deleted', 'success')
    return redirect('/shipments')




#Warehouse routes
@app.route('/warehouse')
def warehouse():
	connection = connect_db()
	cursor = connection.cursor()
	
	search_query = f"SELECT * FROM location"
	
	cursor.execute(search_query)
	connection.commit()

	location_result = cursor.fetchall()
	return render_template("warehouse.html", page_title="Dukes Locations", page_function="Locations", locations = location_result)

@app.route('/new-location')
def newLocation():
    return render_template('newwarehouse.html',
                           page_title="New Location",
                           page_function="Add Location")
@app.route('/create-location', methods=("GET", "POST"))
def createLocation():
    db = connect_db()
    cursor = db.cursor()

    location_key = keyGenerator(),
    location_name = request.form.get('locationName'),
    location_address = request.form.get('locationAddress'),
    location_number = request.form.get('locationContct'),

    insert_query = """INSERT INTO location (location_key, location_name,location_address, location_number) VALUES (%s,%s,%s,%s)"""

    record_to_insert = (location_key, location_name,location_address, location_number)
    cursor.execute(insert_query, record_to_insert)
    db.commit()

    flash('Location created sucessfully', 'success')
    return redirect('/warehouse')

