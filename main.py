from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page_title="Dukes Inventory")

@app.route('/shipments')
def shipments():
	return render_template('shipments.html', page_title="Dukes Shipments")

# Products
@app.route('/new-product')
def newProduct():
	return render_template('newproduct.html', page_title="New Product", page_function="Add product")

@app.route('/update-product')
def updateProduct():
	return render_template('updateproduct.html', page_title="Update Product", page_function="Update product")

# Shipments
@app.route('/new-shipment')
def newShipment():
	return render_template('newshipment.html', page_title="New Shipment", page_function="Add shipment")

@app.route('/update-shipment')
def updateShipment():
	return render_template('updateshipments.html', page_title="Update Shipment", page_function="Update shipment")

app.run(host='0.0.0.0', port=81)
