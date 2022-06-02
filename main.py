from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page_title="Dukes Inventory")

@app.route('/shipments')
def shipments():
	return render_template('shipments.html', page_title="Dukes Shipments")

@app.route('/new-product')
def newProduct():
	return render_template('newproduct.html', page_title="New Product", page_function="Add product")

app.run(host='0.0.0.0', port=81)
