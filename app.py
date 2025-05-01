import os
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.inspection import inspect
from sqlalchemy import func
from flask_cors import CORS  # import CORS

app = Flask(__name__)
app.secret_key = "spoingus"
CORS(app)                    # enable CORS for the app

# Get environment variables
db_user = os.getenv('DB_USER', "root")
db_password = os.getenv('DB_PASSWORD', "Pleiades2013")

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@localhost/magazinesales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
#-----------------------Login Page-----------------------


@app.route("/Login", methods=["POST", "GET"])
def Login():
    if request.method == "POST":
        
        login_name = request.form["name_input"]
        session["username"] = login_name 
        login_email = request.form["email_input"]
        session["useremail"] = login_email
        session["cart"] = []
        session["cartNum"] = 0 
        
        if Customer.query.filter_by(name=login_name, email=login_email).first():
            customer = Customer.query.filter_by(name=login_name, email=login_email).first().customerID
            session["userID"] = customer
            return redirect("/index")
        else:
            flash("One or more field is invalid or account does not exist.")
            return render_template("Login.html")
    else:
        if "username" in session:
            return redirect(url_for("index"))
        
        return render_template("Login.html")
    
@app.route("/signup", methods=["POST", "GET", "PUT"])
def signup():
    if request.method == "POST":
        name_input = request.form["name_input"]
        email_input = request.form["email_input"]
        phone_input = request.form["phone_number_input"]
        address_input = request.form["address_input"]
        customerID = Customer.toInt(Customer.query.order_by(Customer.customerID.desc()).first()) + 1

        if Customer.query.filter_by(name=name_input, email=email_input).first():
            flash("Account already exists")
            return render_template("customer_information.html")
        else:
            try:
                data = {"customerID": customerID, "name": name_input, "email": email_input,"phone": phone_input, "address": address_input}
                
                create_entity("customers", data)
            except Exception as e:
                flash(f"error {e}")
            if Customer.query.filter_by(name=name_input, email=email_input).first():
                
                return redirect("/Login")
            else:
                return render_template("customer_information.html")

        
    else:    
        return render_template("customer_information.html")

#----------------------Logout----------------------

@app.route("/logout", methods=["POST"])
def logout():
    if "username" in session:
        user = session["username"]
        flash(f"{user} logged out successfully.", "info")
    session.pop("username", None)
    session.pop("useremail", None)
    session.pop("cart", None)
    session.pop("cartNum", None)

    return redirect(url_for("Login"))


#----------------------Index page-----------------------

@app.route("/index", methods=["POST", "GET"])
def index():
    if "username" in session:
        user = session["username"]
        return render_template("index.html", user=user)
    else:
        return redirect("/Login")

#----------------------Customer Log---------------------

@app.route("/customerlog", methods=["POST", "GET"])
def customer_log():
    return render_template("customer_log.html", table=get_all_entities("customers"))

#----------------------Writer page----------------------

@app.route("/writerqueue", methods=["POST", "GET"])
def writer_queue():
    return render_template("writer_queue.html", table=get_all_entities("authors"))

#----------------------Discount page--------------------

@app.route("/discount", methods=["POST", "GET"])
def discount():
    if request.method == "POST":
        session["discountID"] = request.form["id"]
    return render_template("discount.html", table=get_all_entities("discounts"))

@app.route("/discounts", methods=["GET", "POST"])
def discounts():
    if request.method == "POST":
        ID = request.form.get("delete")
        try:
            Discount.query.filter_by(discountID=ID).first().delete()
            db.session.commit()
            flash("Entry deleted")
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting entry: {e}")
    
    return render_template("discount.html")

@app.route("/edits", methods=["GET", "POST"])
def edits():
    if request.method == "POST":
        id = request.form.get("id") 
        min_val= request.form.get("min")
        max_val= request.form.get("max")
        percent= request.form.get("percentage")
        code= request.form.get("code")
        try:
            if id:
                entry = Discount.query.filter_by(discountID=id).first()

                if not entry:
                    flash("discount entry not found")
                    return render_template("discount.html")

                if min_val:
                    entry.minVolumes = int(min_val)
                if max_val:
                    entry.maxVolumes = int(max_val)
                if percent:
                    entry.discountPercentage = int(percent)
                if code:
                    entry.discountCode = code
                
                db.session.commit()
                flash("Entry updated")
                return render_template("discount.html", table=get_all_entities("discounts"))
            else:
                flash("No info provided")
                return render_template("discount.html", table=get_all_entities("discounts"))
        except Exception as e:
            db.session.rollback()
            flash(f"error: {e}")
            return render_template("discount.html") 
    return render_template("discount.html")

#----------------------Issues page----------------------

@app.route("/issues", methods=["POST", "GET"])
def issues():
    return render_template("issues.html", table=get_all_entities("issues"))

#----------------------Sales page-----------------------

@app.route("/sales_tab", methods=["POST", "GET"])
def sales():
    
    
    return render_template("sales.html", table=get_all_entities("sales"))

#----------------------Shopping page--------------------

@app.route("/shoppingwindow", methods=["POST", "GET"])
def shopping_window():
    return render_template("shopping_window.html")    


@app.route("/checkout", methods=["POST", "GET"])
def checkout():
     
    if request.method == "POST":
        volume_input = request.form["volume_input"]
        issue_input = int(request.form["issue_input"])
        magazine_input = request.form["magazine_input"]
        

        if session["cartNum"] >= 3:
            flash("Cart is full please checkout")
            return redirect(url_for("shopping_window"))
        if not( issue_input == 1 or  magazine_input == "oops" or not volume_input):
            if session["cartNum"] < 1:
                choice = {"magazine": magazine_input, "volumeID": volume_input, "issueNum": issue_input}
                session["cart"].append(choice) 
                session["cartNum"] += 1
            elif session["cartNum"] < 2:
                choice2 = {"magazine": magazine_input, "volumeID": volume_input, "issueNum": issue_input}
                session["cart"].append(choice2)
                session["cartNum"] += 1
            elif session["cartNum"] < 3:
                choice3 = {"magazine": magazine_input, "volumeID": volume_input, "issueNum": issue_input}
                session["cart"].append(choice3)
                session["cartNum"] += 1

            flash(f"Added to Cart! Cart total: {session["cartNum"]}")
            return redirect(url_for("shopping_window"))
        else:

            flash("One or more fields are blank")
            return redirect(url_for("shopping_window"))
    
    if request.method == "GET":
        create_sale(session["cart"])
        session["cart"] = []
        
        return render_template("thank_you.html")
    return render_template("thank_you.html")



# ---------------------- ENTITY MODELS ----------------------
# (Your existing model definitions remain the same)
class Admin(db.Model):
    __tablename__ = 'admin'
    adminID = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(40), nullable=False)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Magazine(db.Model):
    __tablename__ = 'magazine'
    magazineTitle = db.Column(db.String(100), nullable=False)
    yearPublished = db.Column(db.Integer, nullable=False)
    magazineCost = db.Column(db.Numeric(5, 2), nullable=False)
    totalSubscribers = db.Column(db.Integer, nullable=False)
    totalEarnings = db.Column(db.Numeric(10, 2), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    magazineID = db.Column(db.Integer, primary_key=True)
    adminID = db.Column(db.Integer, db.ForeignKey('admin.adminID', ondelete='CASCADE'), nullable=False)
    adminID2 = db.Column(db.Integer, db.ForeignKey('admin.adminID', ondelete='CASCADE'), nullable=False)

    admin = db.relationship('Admin', foreign_keys=[adminID])
    admin2 = db.relationship('Admin', foreign_keys=[adminID2])

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Volume(db.Model):
    __tablename__ = 'volume'
    volID = db.Column(db.Integer, primary_key=True)
    magID = db.Column(db.Integer, db.ForeignKey('magazine.magazineID', ondelete='CASCADE'), nullable=False)
    volNum = db.Column(db.Integer, nullable=False)
    yearPublished = db.Column(db.Integer, nullable=False)
    volumeCost = db.Column(db.Numeric(5, 2), nullable=False)
    subscriberCount = db.Column(db.Integer, nullable=False)

    issues = db.relationship('Issue', backref='volume', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Issue(db.Model):
    __tablename__ = 'issue'
    issueID = db.Column(db.Integer, primary_key=True)
    volID = db.Column(db.Integer, db.ForeignKey('volume.volID', ondelete='CASCADE'), nullable=False)
    issNum = db.Column(db.Integer, nullable=False)
    season = db.Column(db.String(6), nullable=False)
    issueCost = db.Column(db.Numeric(5, 2), nullable=False)
    backCopiesSold = db.Column(db.Integer, nullable=False)

    articles = db.relationship('Article', backref='issue', cascade='all, delete-orphan')
    sales = db.relationship('Sale', backref='issue', cascade='all, delete-orphan')


   

    def toInt(self):
        num = self.issID
        return num
    
    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Article(db.Model):
    __tablename__ = 'article'
    articleTitle = db.Column(db.String(100), primary_key=True,)
    authorID = db.Column(db.Integer, db.ForeignKey('author.authorID', ondelete='CASCADE'), nullable=False)
    magID2 = db.Column(db.Integer, db.ForeignKey('magazine.magazineID', ondelete='CASCADE'), nullable=False)
    volID2 = db.Column(db.Integer, db.ForeignKey('volume.volID', ondelete='CASCADE'), nullable=False)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID', ondelete='CASCADE'), nullable=False)
    topic = db.Column(db.String(50), nullable=False)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Author(db.Model):
    __tablename__ = 'author'
    authorID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    articles = db.relationship('Article', backref='author', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Customer(db.Model):
    __tablename__ = 'customer'
    customerID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(75), nullable=False)

    sales = db.relationship('Sale', backref='customer', cascade='all, delete-orphan')

    def __init__(self, customerID, name, email, phone, address):
        self.customerID = customerID
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def toInt(self):
        num = self.customerID
        return num

    #def as_dict(self):
        #return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Sale(db.Model):
    __tablename__ = 'sales'
    saleID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey('customer.customerID', ondelete='CASCADE'), nullable=False)
    discountID = db.Column(db.Integer, db.ForeignKey('discount.discountID', ondelete='SET NULL'), server_default='0', nullable=True)
    issID = db.Column(db.Integer, db.ForeignKey('issue.issueID', ondelete='CASCADE'), nullable=False)
    #issID2 = db.Column(db.Integer, db.ForeignKey('issue.issueID', ondelete='CASCADE'), nullable=True, server_default='0')
    #issID3 = db.Column(db.Integer, db.ForeignKey('issue.issueID', ondelete='CASCADE'), nullable=True, server_default='0')
    earning = db.Column(db.Numeric(10, 2), nullable=False)


    def __init__(self,saleID, customerID, issID, earning, discountID):
        self.saleID=saleID
        self.customerID= customerID
        self.issID= issID
        self.earning= earning
        self.discountID= discountID

    def toInt(self):
        num = self.saleID
        return num
    
    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Discount(db.Model):
    __tablename__ = 'discount'
    discountID = db.Column(db.Integer, primary_key=True, server_default='0')
    minVolumes = db.Column(db.Integer, nullable=False)
    maxVolumes = db.Column(db.Integer, nullable=False)
    discountPercentage = db.Column(db.Integer, nullable=False)
    discountCode = db.Column(db.String(10))

    sales = db.relationship('Sale', backref='discount', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

# ---------------------- CRUD ROUTES ----------------------

def get_model(entity):
    models = {
        'magazines': Magazine,
        'volumes': Volume,
        'issues': Issue,
        'authors': Author,
        'articles': Article,
        'customers': Customer,
        'discounts': Discount,
        'sales': Sale,
        'admins': Admin
    }
    return models.get(entity)

def get_primary_key(model):
    inspector = inspect(model)
    primary_key_attributes = [pk.name for pk in inspector.primary_key]
    if primary_key_attributes:
        return primary_key_attributes[0]
    return None

@app.route('/<entity>', methods=['POST'])
def create_entity(entity, data):
    model = get_model(entity)
    if not model:
        flash("error: Invalid entity")
        return None

    try:
        
        if not data:
            flash("error: No data provided")
            return None

        if entity == 'articles' and 'articleTitle' not in data:
            flash("error: Article title is required")
            return None

        new_entry = model(**data)
        db.session.add(new_entry)
        db.session.commit()
        flash("Account created successfully")
        return None

    except exc.IntegrityError as e:
        db.session.rollback()
        flash(f"error: Database integrity error \ndetails: {e}")
        return None
    except Exception as e:
        db.session.rollback()
        flash(f"error {e}")
        return 

@app.route('/<entity>', methods=['GET'])
def get_all_entities(entity):
    model = get_model(entity)
    if not model:
        flash("error: Invalid entity")
        return None

    try:
        records = model.query.all()
        return records
    except Exception as e:
        flash(f"error: {e}")
        return None

@app.route('/<entity>/<id>', methods=['GET'])
def get_entity(entity, id):
    model = get_model(entity)
    if not model:
        flash("error: Invalid entity")
        return

    try:
        primary_key = get_primary_key(model)
        if not primary_key:
            flash("error: Could not determine primary key")
            return

        if getattr(model, primary_key).type.python_type is int:
            record = model.query.get(int(id))
        else:
            record = model.query.get(id)

        if not record:
            flash(f"error: {entity.capitalize()} not found")
            return 
        flash(record.as_dict())
        return
    except Exception as e:
        flash(f"error: {e}")
        return

@app.route('/<entity>/<id>', methods=['PUT'])
def update_entity(entity, id):
    model = get_model(entity)
    if not model:
        flash("error: Invalid entity")
        return 

    try:
        data = request.get_json()
        if not data:
            flash("error: No data provided")
            return

        primary_key = get_primary_key(model)
        if not primary_key:
            flash("error: Could not determine primary key")
            return 

        if getattr(model, primary_key).type.python_type is int:
            record = model.query.get(int(id))
        else:
            record = model.query.get(id)

        if not record:
            flash(f"error: {entity.capitalize()} not found")
            return 

        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)

        db.session.commit()
        flash(record.as_dict())
        return 

    except exc.IntegrityError as e:
        db.session.rollback()
        flash(f"error: Database integrity error \ndetails: {e}")
        return 
    except Exception as e:
        db.session.rollback()
        flash(f"error: {e}")
        return 

@app.route('/<entity>/<id>', methods=["GET", 'DELETE'])
def delete_entity(entity, id):
    model = get_model(entity)
    if not model:
        flash("error: Invalid entity")
        return 

    try:
        primary_key = get_primary_key(model)
        if not primary_key:
            flash("error: Could not determine primary key")
            return 

        if getattr(model, primary_key).type.python_type is int:
            record = model.query.get(int(id))
        else:
            record = model.query.get(id)

        if not record:
            flash(f"error: {entity.capitalize()} not found")
            return 

        db.session.delete(record)
        db.session.commit()
        flash(f"message: {entity.capitalize()} deleted successfully")
        return 
    except Exception as e:
        db.session.rollback()
        flash(f"error: {e}")
        return 

@app.route('/sales', methods=['POST'])
def create_sale(data):
    try:
        
        if not data:
            flash("error: No data provided for sale")
            return 
        
        customer_id = session['userID']
        iss1 = data[0]
        if session['cartNum'] >= 2:
            iss2 = data[1]
        else:
            iss2 = 0    
        if session["cartNum"] >= 3:    
            iss3 = data[2]
        else:
            iss3 = 0
        if session["cartNum"] >= 4:
            full = data[3]
        

        if not customer_id or not iss1:
            flash("error: customerID and at least one issue is required")
            return

        # Verify customer and issue existence
        customer = Customer.query.get(customer_id)
        issue1 = Issue.query.filter_by(volID=iss1["volumeID"], issNum=iss1["issueNum"])
        if iss2 !=0:
            issue2 = Issue.query.filter_by(volID=iss2["volumeID"], issNum=iss2["issueNum"]) if iss2 !=0  else None
        if iss3 !=0:    
            issue3 = Issue.query.filter_by(volID=iss3["volumeID"], issNum=iss3["issueNum"]) if iss3 !=0 else None

        if not customer:
            flash("error: Customer not found")
            return 
        if not issue1:
            flash("error: Issue with the given issID not found")
            return 
        if  iss2 !=0 and not issue2:
            flash("error: The second Issue could not be found")
            return 
        if  iss3 !=0 and not issue3:
            flash("error: The third Issue could not be found")
            return 

        total_volumes = 1 
        if iss2 !=0:
            if iss2["volumeID"] != iss1["volumeID"] or iss3["volumeID"]:
                total_volumes += 1
                if iss3 !=0:
                    if iss3["volumeID"] != iss1["volumeID"] or iss2["volumeID"]:
                        total_volumes += 1    

        # Fetch applicable discounts, ordered by minVolumes in descending order
        discounts = Discount.query.order_by(Discount.minVolumes.desc()).all()

        discount_to_apply = None
        for discount in discounts:
            if discount.minVolumes <= total_volumes <= discount.maxVolumes:
                discount_to_apply = discount
                break

        total_earning = 10 + (10 if iss2!=0 else 0) + (10 if iss3!=0 else 0)

        # Apply discount if applicable
        if discount_to_apply:
            from decimal import Decimal
            discount_percentage_decimal = Decimal(discount_to_apply.discountPercentage) / Decimal('100.00')
            discount_amount = total_earning * discount_percentage_decimal
            total_earning -= discount_amount

        # Ensure valid discount ID (0 if no discount is applied)
        discount_id = discount_to_apply.discountID if discount_to_apply else 0

        # Create the sale record
        new_sale = Sale(
            saleID=Sale.toInt(Sale.query.order_by(Sale.saleID.desc()).first()) + 1,
            customerID=customer_id,
            issID= int(iss1["volumeID"]) * 4 - (4 - iss1["issueNum"]),
            #issID2=iss2 if iss2 else None,  # Store only non-zero issue IDs, or None
            #issID3=iss3 if iss3 else None,  # Store only non-zero issue IDs, or None
            earning=total_earning,
            discountID=discount_id
        )
        db.session.add(new_sale)
        db.session.commit()
        flash("Success!")
        flash(f"Your total was ${total_earning + discount_amount}, and you saved ${discount_amount}")
        session["cartNum"] = 0
        session.pop("cart")
        return

    except exc.IntegrityError as e:
        db.session.rollback()
        flash(f"error: Database integrity error during sale creation, details {e}")
        return
    except Exception as e:
        db.session.rollback()
        flash(f"error: {e}")
        return 
    
# ---------------------- RUN APP -----------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)