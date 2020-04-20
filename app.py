from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from datetime import datetime, timedelta, date
from collections import Counter 
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waitlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db=SQLAlchemy(app)
migrate=Migrate(app, db)

class Product(db.Model):	
    __tablename__ = "products"
    product_id=db.Column(db.String(100), primary_key=True)	
    product_name=db.Column(db.String(100))
    created_at=db.Column(db.DateTime, server_default=func.now())
    updated_at=db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    product_incoming_shipments=db.relationship("Shipment", back_populates="product", cascade="all, delete, delete-orphan")
    product_orders=db.relationship("Order", back_populates="product", cascade="all, delete, delete-orphan")

    def get_shipment_delivery_dates(self):
        result = []
        for shipment in self.product_incoming_shipments:
            result.append(shipment.estimate_delivery_date)
        result = sorted(result)
        return result

    def total_available_quantity(self):
        total_avail = 0
        for shipment in self.product_incoming_shipments:
            total_avail = total_avail + shipment.available_quantity
        return total_avail
    
    def total_waitlisted_customers(self):
        cus_list = []
        for order in self.product_orders:
            cus_list.append(order.customer_id)
        return countDistinct(cus_list)
    
    def total_ordered_quantity(self):
        total_ordered = 0
        for order in self.product_orders:
            total_ordered = total_ordered + order.quantity
        return total_ordered

    
class Shipment(db.Model):	
    __tablename__ = "shipments"	
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(100), db.ForeignKey("products.product_id"))
    product = db.relationship('Product', foreign_keys=[product_id])
    product_quantity = db.Column(db.Integer)
    available_quantity=db.Column(db.Integer)
    purchase_limit = db.Column(db.Integer)
    estimate_delivery_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def purchase_limit_values(self):
        result = []
        p_limit = self.purchase_limit + 1
        for x in range (1, p_limit):
            result.append(x)
        return result

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    customer = db.relationship('Customer', foreign_keys=[customer_id])
    product_id = db.Column(db.String(100), db.ForeignKey("products.product_id"))
    product = db.relationship('Product', foreign_keys=[product_id])
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Customer(db.Model):
    __tablename__ = "customers"
    id=db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(),onupdate=func.now())
    customer_orders = db.relationship("Order", back_populates="customer", cascade="all, delete, delete-orphan")

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def add_new_customer(cls,data):
        new_customer = cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
        )
        db.session.add(new_customer)
        db.session.commit()
        return new_customer

    @classmethod
    def show_errors(cls, form_data):
        errors=[]

        if len(form_data['first_name'])<1:
            errors.append("Please enter valid first name.")
        if len(form_data['last_name'])<1:
            errors.append("Please enter valid last name.")
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append("Please enter valid email.")

        return errors

    @classmethod
    def add_to_customers(cls, form_data):
        errors = cls.show_errors(form_data)
        valid = len(errors)==0
        data = cls.add_new_customer(form_data) if valid else errors
        return {
            "status": "good" if valid else "bad",
            "data": data
        }
def countDistinct(arr): 
  
    # counter method gives dictionary of elements in list 
    # with their corresponding frequency. 
    # using keys() method of dictionary data structure 
    # we can count distinct values in array 
    return len(Counter(arr).keys()) 

@app.route("/dashboard")
def product_info():
    product_list=Product.query.all()
    return render_template("dashboard.html", products=product_list)

@app.route("/products/add")
def add_product():
    return render_template("add_product.html")


@app.route("/products/new", methods=["POST"])
def new_product():
    new_product = Product(
        product_id=request.form['product_id'],
        product_name=request.form['product_name']
    )
    db.session.add(new_product)
    db.session.commit()

    date = request.form['estimate_delivery_date']
    delivery_date = datetime.strptime(date, '%Y-%m-%d')

    new_shipment = Shipment(
        product_id=request.form['product_id'],
        product_quantity = request.form['product_quantity'],
        available_quantity = request.form['product_quantity'],
        purchase_limit = request.form['purchase_limit'],
        estimate_delivery_date = delivery_date
    )
    db.session.add(new_shipment)
    db.session.commit()
    return redirect("/dashboard")

@app.route("/products/<product_id>/edit")
def edit_product(product_id):
    product = Product.query.get(product_id)
    shipment_list = Shipment.query.filter_by(product_id=product_id).order_by(Shipment.estimate_delivery_date).all()
    return render_template("edit_product.html", product=product, shipments=shipment_list)

@app.route("/products/update", methods=["POST"])
def update_product_info():
    
    orig_product_id = request.form['original_product_id']

    product = Product.query.get(orig_product_id)
    shipments = Shipment.query.filter_by(product_id=orig_product_id).all()
    orders = Order.query.filter_by(product_id=orig_product_id).all()

    if len(request.form['product_id'])>0:
        product.product_id=request.form['product_id']
        product.product_name=request.form['product_name']
        product.updated_at=datetime.now()

        for shipment in shipments:
            shipment.updated_at=datetime.now()
            shipment.product_id=request.form['product_id']

        for order in orders:
            order.product_id=request.form['product_id']
            order.updated_at=datetime.now()
        
        db.session.commit()
    return redirect('/products/{}/edit'.format(request.form['product_id']))

@app.route("/products/<product_id>/delete")
def delete_product(product_id):

    orders = Order.query.filter_by(product_id=product_id).all()

    if orders:

        flash("There are already orders placed for this product. Please cancel customer orders before deleting.")
        return redirect('/products/{}/edit'.format(product_id))
    
    else: 

        product_being_deleted=Product.query.get(product_id)

        db.session.delete(product_being_deleted)
        db.session.commit()
        return redirect("/dashboard")

@app.route("/shipments/<shipment_id>/edit")
def edit_shipment(shipment_id):
    shipment = Shipment.query.get(shipment_id)
    return render_template("edit_shipment.html", shipment=shipment)

@app.route("/shipments/update", methods=["POST"])
def update_shipment_info():

    orig_shipment_id = request.form['original_shipment_id']

    shipment = Shipment.query.get(orig_shipment_id)

    ordered_quantity = shipment.product_quantity - shipment.available_quantity

    updated_quantity = int(request.form['product_quantity'])

    difference_bwtn = shipment.product_quantity - shipment.available_quantity

    new_date = request.form['estimate_delivery_date']

    def isBlank(myString):
        if myString and myString.strip():
            return False
        return True


    if isBlank(new_date) == False:

        new_delivery_date = datetime.strptime(new_date, '%Y-%m-%d')

        print(new_delivery_date)

        print(request.form['estimate_delivery_date'])

        print(" im a big monkey!!!!!")

        if updated_quantity < difference_bwtn:
            flash("There are {} products ordered from this shipment. Please cancel customer orders before editing the quantity.".format(ordered_quantity))
    
        else:

            if updated_quantity >= shipment.product_quantity:

                updated_greater_amount = updated_quantity - shipment.product_quantity
                shipment.product_quantity= updated_quantity
                shipment.available_quantity=shipment.available_quantity + updated_greater_amount
                shipment.purchase_limit=request.form['purchase_limit']
                shipment.estimate_delivery_date= new_delivery_date
                shipment.updated_at=datetime.now()
                db.session.commit()
        
            else:

                updated_lesser_amount = shipment.product_quantity - updated_quantity
                shipment.product_quantity= updated_quantity
                shipment.available_quantity=shipment.available_quantity - updated_lesser_amount
                shipment.purchase_limit=request.form['purchase_limit']
                shipment.estimate_delivery_date= new_delivery_date
                shipment.updated_at=datetime.now()
                db.session.commit()
    else:

        new_delivery_date = shipment.estimate_delivery_date

        if updated_quantity < difference_bwtn:
            flash("There are {} products ordered from this shipment. Please cancel customer orders before editing the quantity.".format(ordered_quantity))
    
        else:

            if updated_quantity >= shipment.product_quantity:

                updated_greater_amount = updated_quantity - shipment.product_quantity
                shipment.product_quantity= updated_quantity
                shipment.available_quantity=shipment.available_quantity + updated_greater_amount
                shipment.purchase_limit=request.form['purchase_limit']
                shipment.estimate_delivery_date= new_delivery_date
                shipment.updated_at=datetime.now()
                db.session.commit()
        
            else:

                updated_lesser_amount = shipment.product_quantity - updated_quantity
                shipment.product_quantity= updated_quantity
                shipment.available_quantity=shipment.available_quantity - updated_lesser_amount
                shipment.purchase_limit=request.form['purchase_limit']
                shipment.estimate_delivery_date= new_delivery_date
                shipment.updated_at=datetime.now()
                db.session.commit()
    
    return redirect('/shipments/{}/edit'.format(orig_shipment_id))

@app.route("/shipments/<shipment_id>/delete")
def delete_shipment(shipment_id):

    shipment = Shipment.query.get(shipment_id)

    ordered_quantity = shipment.product_quantity - shipment.available_quantity    

    if ordered_quantity > 0:

        flash("There are already orders placed for this shipment. Please cancel customer orders before deleting.")
        return redirect('/shipments/{}/edit'.format(shipment_id))
    
    else: 

        db.session.delete(shipment)
        db.session.commit()
        return redirect("/dashboard")


@app.route("/shipments/<product_id>/add")
def add_shipment(product_id):
    product=Product.query.get(product_id)
    return render_template("add_shipment.html", product=product)

@app.route("/shipments/new", methods=["POST"])
def new_shipment():
    date = request.form['estimate_delivery_date']
    delivery_date = datetime.strptime(date, '%Y-%m-%d')

    new_shipment = Shipment(
        product_id=request.form['product_id'],
        product_quantity = request.form['product_quantity'],
        available_quantity = request.form['product_quantity'],
        purchase_limit = request.form['purchase_limit'],
        estimate_delivery_date = delivery_date
    )
    db.session.add(new_shipment)
    db.session.commit()
    return redirect('/dashboard')

@app.route("/waitlist/<product_id>/manage")
def manage_waitlist(product_id):
    product = Product.query.get(product_id)
    return render_template("manage_waitlist.html", product=product)


@app.route("/waitlist/<product_id>/join")
def customer_form(product_id):
    product=Product.query.get(product_id)
    shipment_list=Shipment.query.filter_by(product_id=product_id).order_by(Shipment.estimate_delivery_date).all()
    print(shipment_list)
    for shipment in shipment_list:
        if shipment.available_quantity>0:
            session['cur_shipment'] = {
            "shipment_id": shipment.id
            }
            shipment=Shipment.query.get(shipment.id)
            break
    if shipment.available_quantity<=0:
        flash('The waitlist is full. Please check back later.')
    print(shipment)
    print(shipment.available_quantity)
    return render_template("join_waitlist.html", product=product, shipments=shipment_list, shipment=shipment)

@app.route("/waitlist/<shipment_id>/join", methods=["POST"])
def join_waitlist(shipment_id):
    shipment = Shipment.query.get(shipment_id)
    if shipment.available_quantity>=int(request.form['quantity']):

        form_email = request.form['email']
        returning_customer = Customer.query.filter(Customer.email==form_email).first()

        if returning_customer:

            form_first_name = request.form['first_name']
            same_name_customer = Customer.query.filter(Customer.email==form_email, Customer.first_name==form_first_name).first()

            if same_name_customer:
     
                print(returning_customer)
                session['cur_customer'] = {
                    "cur_customer_id": returning_customer.id
                }

                this_product = request.form['product_id']

                previous_order = Order.query.filter(Order.product_id==this_product, Order.customer_id==returning_customer.id).first()

                if previous_order:
                    print(previous_order)
                    flash("Only 1 order is permitted per customer.")

                else:

                    shipment.available_quantity = shipment.available_quantity - int(request.form['quantity'])

                    print(shipment.available_quantity)

                    new_order = Order(
                        customer_id = returning_customer.id,
                        product_id = request.form['product_id'],
                        quantity=int(request.form['quantity'])
                    )
                    db.session.add(new_order)
                    db.session.commit()
                    flash('Thank you for your order, you have been added to the waitlist.')
            
            else:

                flash('This email address is already in use. Please be advised, the form is case sensitive. Update your information and try again.')

        else:

            result = Customer.add_to_customers(request.form)
        
            if result['status']=="good":
        
                customer=result['data']
                print(customer)
                session['cur_customer'] = {
                    "customer_id": customer.id
                }

                shipment.available_quantity = shipment.available_quantity - int(request.form['quantity'])

                print(shipment.available_quantity)

                new_order = Order(
                    customer_id = customer.id,
                    product_id = request.form['product_id'],
                    quantity=request.form['quantity']
                )
                db.session.add(new_order)
                db.session.commit()
                flash('Thank you for your order, you have been added to the waitlist.')

            else:
                errors=result['data']
                for error in errors:
                    flash(error)
    else:
        if shipment.available_quantity>0:
            flash('Only {} item(s) are left in the next shipment, please lower your order quantity to join the waitlist.'.format(shipment.available_quantity))
    return redirect('/waitlist/{}/join'.format(request.form['product_id']))
if __name__ == "__main__":
    app.run(debug=True)