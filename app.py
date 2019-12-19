from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
import pyodbc
from sqlalchemy import text

app = Flask(__name__)
server = 'quasar'
database = 'ChocolateBiscuitFactoryIMS'
username = 'sa'
password = 'Cse-3055'
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


@app.route('/index')
def index():
    cursor = cnxn.cursor()
    cursor.execute('select * from ChocolateBiscuitFactoryIMS.dbo.Worker')
    print("cursor type is", type(cursor))
    arr = list()
    for row in cursor:
        # print(type(row))
        arr.append(list(row))
    return render_template('index.html', out=arr)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/production')
def production():
    return render_template('production.html')


@app.route('/production_machine')
def production_machine():
    return render_template('production_machine.html')


@app.route('/production_product')
def production_product():
    return render_template('production_products.html')


@app.route('/sales')
def sales():
    return render_template('sales.html')


@app.route('/sales_customer')
def sales_customer():
    return render_template('sales_customer.html')


@app.route('/sales_order')
def sales_order():
    return render_template('sales_order.html')


@app.route('/sales_shipping')
def sales_shipping():
    return render_template('sales_shipping.html')


@app.route('/workers')
def workers():
    return render_template('workers.html')


@app.route('/warehouse')
def warehouse():
    return render_template('warehouse.html')


@app.route('/warehouse_rawmaterial')
def warehouse_rawmaterial():
    return render_template('warehouse_rawmaterial.html')


@app.route('/warehouse_storedproduct')
def warehouse_storedproduct():
    return render_template('warehouse_storedproduct.html')


if __name__ == '__main__':
    app.run(debug=True)
