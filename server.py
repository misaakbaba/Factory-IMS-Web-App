from flask import Flask, render_template, jsonify, request
from sqlalchemy.orm.scoping import meth

from Utils import *
import json
import pyodbc

app = Flask(__name__)
server = 'quasar'
database = 'ChocolateBiscuitFactoryIMS2'
username = 'sa'
password = 'Cse-3055'
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


@app.route('/index')
def index():
    cursor = conn.cursor()
    cursor.execute('select * from ChocolateBiscuitFactoryIMS2.dbo.Worker')
    print("cursor type is", type(cursor))
    arr = list()
    for row in cursor:
        # print(type(row))
        arr.append(list(row))
    return render_template('temp.html', out=arr)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/production_machine')
def production_machine():
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Machine")
    table = create_copy(cursor)
    # for i in table:
    #     print(i)
    return render_template('production_machine.html', machine_table=table)


@app.route('/production_updatemachine')
def production_updatemachine():
    return render_template('production_updatemachine.html')


@app.route('/getmachine', methods=['POST'])
def getmachine():
    id = request.form.get('id')[1:-1]
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Machine where Serial_Number=?", id)
    result = list()
    for row in cursor:
        result.append(list(row))
    return jsonify(
        {'status': 'OK', 'productiondate': result[0][1], 'maintenancetime': result[0][2],
         'machinefunction': result[0][3]})


@app.route('/updatemachine', methods=['POST'])
def updatemachine():
    id = request.form['id'][1:-1]
    production_date = request.form['productiondate'][1:-1]
    maintenance_time = request.form['maintenancetime'][1:-1]
    machine_function = request.form['machinefunction'][1:-1]
    print(id)
    print(production_date)
    print(maintenance_time)
    print(machine_function)
    cursor = conn.cursor()
    cursor.execute(
        "update ChocolateBiscuitFactoryIMS2.dbo.Machine set Production_Date=?, Maintanence_Time=?, Machine_Function=? where Serial_Number=?",
        production_date, maintenance_time, machine_function, id)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/production')
def production_product():
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Products")
    product = create_copy(cursor)
    return render_template('production.html', table=product)


@app.route('/production_addproduct', methods=['GET', 'POST'])
def production_addproduct():
    return render_template('production_addproduct.html')


@app.route('/addproduct', methods=['POST'])
def addproduct():
    id = request.form['product_id'][1:-1]
    price = int(request.form['price'])
    product_type = request.form['product_type'][1:-1]
    print(type(id))
    print(type(int(price)))
    print(type(product_type))
    cursor = conn.cursor()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Products (Product_ID,Price,Product_Type) " \
        "values (?,?,?)", id, price, product_type)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/sales')
def sales():
    cursor = conn.cursor()
    cursor.execute(
        "select  Order_ID,Product_ID,Ordered_Quantity from ChocolateBiscuitFactoryIMS2.dbo.Order_Line")
    order_line = create_copy(cursor)
    cursor.execute("select Product_ID,Product_Type from ChocolateBiscuitFactoryIMS2.dbo.Products")
    products = create_copy(cursor)
    cursor.execute("SELECT * FROM ChocolateBiscuitFactoryIMS2.dbo.Orders")
    orders = create_copy(cursor)
    sales_table = set_orders(orders, order_line, products)
    return render_template('sales.html', sales_table=sales_table)


@app.route('/sales_customer')
def sales_customer():
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Person")
    person = create_copy(cursor)
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Customer")
    customer = create_copy(cursor)
    table = set_workers(customer, person)
    return render_template('sales_customer.html', customer_list=table)


@app.route('/sales_addcustomer', methods=['GET', 'POST'])
def sales_addcustomer():
    return render_template('sales_addcustomer.html')


@app.route('/addcustomer', methods=['POST'])
def addcustomer():
    ssn = request.form['ssn'][1:-1]
    name = request.form['name'][1:-1]
    street_address = request.form['street_address'][1:-1]
    district = request.form['district'][1:-1]
    city = request.form['city'][1:-1]
    postal_code = request.form['postal_code'][1:-1]
    gender = request.form['gender'][1:-1]
    age = request.form.get('age')
    business_id = request.form.get('business_id')[1:-1]
    email = request.form.get('email')[1:-1]

    cursor = conn.cursor()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Person (SSN,Name,Street_Address,District,City,Postal_Code,Gender,Age) " \
        "values (?,?,?,?,?,?,?,?)", ssn, name, street_address, district, city, postal_code, gender, age)
    conn.commit()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Customer (Business_ID,E_mail,Customer_ID) " \
        "values (?,?,?)", business_id, email, ssn)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/sales_deletecustomer', methods=['GET', 'POST'])
def sales_deletecustomer():
    return render_template('sales_deletecustomer.html')


@app.route('/deletecustomer', methods=['POST'])
def deletecustomer():
    ssn = request.form['ssn'][1:-1]
    print(ssn)
    cursor = conn.cursor()
    cursor.execute("delete from ChocolateBiscuitFactoryIMS2.dbo.Customer where Customer_ID=?", ssn)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/sales_order')
def sales_order():
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Orders")
    table = create_copy(cursor)
    return render_template('sales_order.html', order_table=table)


@app.route('/sales_addorder', methods=['POST', 'GET'])
def sales_addorder():
    return render_template('sales_addorder.html')


@app.route('/addorder', methods=['POST'])
def addorder():
    id = request.form['id'][1:-1]
    order_price = int(request.form.get('orderprice'))
    customer_id = request.form['customerid'][1:-1]
    shipping_id = request.form['shippingid'][1:-1]
    print(id)
    print(order_price)
    print(customer_id)
    print(shipping_id)
    cursor = conn.cursor()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Orders (Order_ID,Order_Price,Customer_ID,Shipping_ID) " \
        "values (?,?,?,?)", id, order_price, customer_id, shipping_id)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/sales_addorderline', methods=['POST', 'GET'])
def sales_addorderline():
    return render_template('sales_addorderline.html')


@app.route('/addorderline', methods=['POST'])
def addorderline():
    ordered_quantity = int(request.form.get('quantity'))
    order_id = request.form['orderid'][1:-1]
    product_id = request.form['product_id'][1:-1]
    print(ordered_quantity, order_id, product_id)
    cursor = conn.cursor()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Order_Line (Ordered_Quantity,Order_ID,Product_ID) " \
        "values (?,?,?)", ordered_quantity, order_id, product_id)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/sales_shipping')
def sales_shipping():
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Shipping")
    table = create_copy(cursor)
    return render_template('sales_shipping.html', shipping_table=table)


@app.route('/sales_addshipping', methods=['POST', 'GET'])
def sales_addshipping():
    return render_template('sales_addshipping.html')


@app.route('/addshipping', methods=['POST'])
def addshipping():
    id = request.form['id'][1:-1]
    departure_time = request.form['departuretime'][1:-1]
    arrival_time = request.form['arrivaltime'][1:-1]
    print(id)
    print(departure_time)
    print(arrival_time)
    cursor = conn.cursor()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Shipping (Shipping_ID,Departure_Time,Arrival_Time) " \
        "values (?,?,?)", id, departure_time, arrival_time)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/workers')
def workers():
    cursor = conn.cursor()
    cursor.execute(
        'select [Salary],[Department],[Worker_ID],[Working_Machine] from ChocolateBiscuitFactoryIMS2.dbo.Worker')
    worker = create_copy(cursor)
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Person")
    person = create_copy(cursor)
    table = set_workers(workers=worker, person=person)
    return render_template('workers.html', worker_list=table)


@app.route('/workers_addworker', methods=['GET', 'POST'])
def workers_addworker():
    return render_template('workers_addworker.html')


@app.route('/workers_deleteworker', methods=['GET', 'POST'])
def workers_deleteworker():
    return render_template('workers_deleteworker.html')


@app.route('/deleteworker', methods=['POST'])
def deleteworker():
    ssn = request.form['ssn'][1:-1]
    print(ssn)
    cursor = conn.cursor()
    cursor.execute("delete from ChocolateBiscuitFactoryIMS2.dbo.Worker where Worker_ID=?", ssn)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/addworker', methods=['POST'])
def addworker():
    ssn = request.form['ssn'][1:-1]
    name = request.form['name'][1:-1]
    street_address = request.form['street_address'][1:-1]
    district = request.form['district'][1:-1]
    city = request.form['city'][1:-1]
    postal_code = request.form['postal_code'][1:-1]
    gender = request.form['gender'][1:-1]
    age = int(request.form.get('age'))
    salary = int(request.form.get('salary'))
    department = request.form['department'][1:-1]
    date_employed = request.form['date_employed'][1:-1]
    working_machine = request.form['working_machine'][1:-1]

    cursor = conn.cursor()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Person (SSN,Name,Street_Address,District,City,Postal_Code,Gender,Age) " \
        "values (?,?,?,?,?,?,?,?)", ssn, name, street_address, district, city, postal_code, gender, age)
    conn.commit()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Worker (Salary,Department,Date_Employed,Worker_ID,Working_Machine) " \
        "values (?,?,?,?,?)", salary, department, date_employed, ssn, working_machine)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/warehouse')
def warehouse():
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Warehouse")
    table = create_copy(cursor)
    return render_template('warehouse.html', warehouse_table=table)


@app.route('/warehouse_rawmaterial')
def warehouse_rawmaterial():
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Raw_Material")
    table = create_copy(cursor)
    return render_template('warehouse_rawmaterial.html', rawmaterial_table=table)


@app.route('/warehouse_addrawmaterial', methods=['GET', 'POST'])
def warehouse_addrawmaterial():
    return render_template('warehouse_addrawmaterial.html')


@app.route('/addrawmaterial', methods=['POST'])
def addrawmaterial():
    material_id = request.form['id'][1:-1]
    material_type = request.form['materialtype'][1:-1]
    quantity = int(request.form.get('quantity'))
    price = int(request.form.get('price'))
    expiration_date = request.form['expirationdate'][1:-1]
    warehouse_id = request.form['warehouseid'][1:-1]

    print(material_id)
    print(material_type)
    print(quantity)
    print(price)
    print(expiration_date)
    print(warehouse_id)

    cursor = conn.cursor()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Raw_Material (Material_ID,Material_Type,Quantity,Price,Expiration_Date,Warehouse_ID) " \
        "values (?,?,?,?,?,?)", material_id, material_type, quantity, price, expiration_date, warehouse_id)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/warehouse_deleterawmaterial', methods=['GET', 'POST'])
def warehouse_deleterawmaterial():
    return render_template('warehouse_deleterawmaterial.html')


@app.route('/deleterawmaterial', methods=['POST'])
def deleterawmaterial():
    id = request.form['id'][1:-1]
    # print(id)
    cursor = conn.cursor()
    cursor.execute("delete from ChocolateBiscuitFactoryIMS2.dbo.Raw_Material where Material_ID=?", id)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/warehouse_storedproduct')
def warehouse_storedproduct():
    cursor = conn.cursor()
    cursor.execute("select * from ChocolateBiscuitFactoryIMS2.dbo.Stored_Product")
    stored_product = create_copy(cursor)
    cursor.execute("select Product_ID,Product_Type from ChocolateBiscuitFactoryIMS2.dbo.Products")
    product = create_copy(cursor)
    table = set_storedproduct(stored_product, product)
    return render_template('warehouse_storedproduct.html', storedproduct_table=table)


@app.route('/warehouse_addstoredproduct', methods=['POST', 'GET'])
def warehouse_addstoredproduct():
    return render_template('warehouse_addstoredproduct.html')


@app.route('/addstoredproduct', methods=['POST'])
def addstoredproduct():
    id = request.form['id'][1:-1]
    production_date = request.form['productiondate'][1:-1]
    expiration_date = request.form['expirationdate'][1:-1]
    quantity = int(request.form.get('quantity'))
    warehouse_id = request.form['warehouseid'][1:-1]
    machine_serial_number = request.form['machineserialnumber'][1:-1]
    print(id)
    print(production_date)
    print(expiration_date)
    print(quantity)
    print(warehouse_id)
    print(machine_serial_number)
    cursor = conn.cursor()
    cursor.execute(
        "insert into ChocolateBiscuitFactoryIMS2.dbo.Stored_Product (Product_ID,Production_Date,Expiration_Date,Quantity,Warehouse_ID,Machine_Serial_Number) " \
        "values (?,?,?,?,?,?)", id, production_date, expiration_date, quantity, warehouse_id, machine_serial_number)
    conn.commit()
    return jsonify({'status': 'OK'})


@app.route('/warehouse_deletestoredproduct', methods=['POST', 'GET'])
def warehouse_deletestoredproduct():
    return render_template('warehouse_deletestoredproduct.html')


@app.route('/deletestoredproduct', methods=['POST'])
def deletestoredproduct():
    id = request.form['id'][1:-1]
    print(id)
    cursor = conn.cursor()
    cursor.execute("delete from ChocolateBiscuitFactoryIMS2.dbo.Stored_Product where Product_ID=?", id)
    conn.commit()
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    # cursor = conn.cursor()
    # cursor2 = conn.cursor()

    app.run(debug=True, host='0.0.0.0')
