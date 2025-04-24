import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.inspection import inspect
from sqlalchemy import func
from flask_cors import CORS  # import CORS

app = Flask(__name__)        #  initialize Flask app
CORS(app)                    # enable CORS for the app

# Get environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Configure Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@localhost/magazinesales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

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

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Article(db.Model):
    __tablename__ = 'article'
    articleTitle = db.Column(db.String(100), primary_key=True)
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

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Sale(db.Model):
    __tablename__ = 'sales'
    saleID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey('customer.customerID', ondelete='CASCADE'), nullable=False)
    discountID = db.Column(db.Integer, db.ForeignKey('discount.discountID', ondelete='SET NULL'), server_default='0', nullable=True)
    issID = db.Column(db.Integer, db.ForeignKey('issue.issueID', ondelete='CASCADE'), nullable=False)
    issID2 = db.Column(db.Integer, server_default='0')
    issID3 = db.Column(db.Integer, server_default='0')
    earning = db.Column(db.Numeric(10, 2), nullable=False)

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
def create_entity(entity):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        if entity == 'articles' and 'articleTitle' not in data:
            return jsonify({"error": "Article title is required"}), 400

        new_entry = model(**data)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify(new_entry.as_dict()), 201

    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/<entity>', methods=['GET'])
def get_all_entities(entity):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404

    try:
        records = model.query.all()
        return jsonify([record.as_dict() for record in records])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<entity>/<id>', methods=['GET'])
def get_entity(entity, id):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404

    try:
        primary_key = get_primary_key(model)
        if not primary_key:
            return jsonify({"error": "Could not determine primary key"}), 500

        if getattr(model, primary_key).type.python_type is int:
            record = model.query.get(int(id))
        else:
            record = model.query.get(id)

        if not record:
            return jsonify({"error": f"{entity.capitalize()} not found"}), 404
        return jsonify(record.as_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<entity>/<id>', methods=['PUT'])
def update_entity(entity, id):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        primary_key = get_primary_key(model)
        if not primary_key:
            return jsonify({"error": "Could not determine primary key"}), 500

        if getattr(model, primary_key).type.python_type is int:
            record = model.query.get(int(id))
        else:
            record = model.query.get(id)

        if not record:
            return jsonify({"error": f"{entity.capitalize()} not found"}), 404

        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)

        db.session.commit()
        return jsonify(record.as_dict())

    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/<entity>/<id>', methods=['DELETE'])
def delete_entity(entity, id):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404

    try:
        primary_key = get_primary_key(model)
        if not primary_key:
            return jsonify({"error": "Could not determine primary key"}), 500

        if getattr(model, primary_key).type.python_type is int:
            record = model.query.get(int(id))
        else:
            record = model.query.get(id)

        if not record:
            return jsonify({"error": f"{entity.capitalize()} not found"}), 404

        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": f"{entity.capitalize()} deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/sales', methods=['POST'])
def create_sale():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided for sale"}), 400

        customer_id = data.get('customerID')
        iss_id = data.get('issID')
        iss_id2 = data.get('issID2', 0)
        iss_id3 = data.get('issID3', 0)

        if not customer_id or not iss_id:
            return jsonify({"error": "customerID and at least one issID are required"}), 400

        # Verify customer and issue existence
        customer = Customer.query.get(customer_id)
        issue1 = Issue.query.get(iss_id)
        issue2 = Issue.query.get(iss_id2) if iss_id2 != 0 else None
        issue3 = Issue.query.get(iss_id3) if iss_id3 != 0 else None

        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        if not issue1:
            return jsonify({"error": "Issue with the given issID not found"}), 404
        if iss_id2 != 0 and not issue2:
            return jsonify({"error": "Issue with the given issID2 not found"}), 404
        if iss_id3 != 0 and not issue3:
            return jsonify({"error": "Issue with the given issID3 not found"}), 404

        total_volumes = 1 + (1 if issue2 else 0) + (1 if issue3 else 0)

        # Fetch applicable discounts, ordered by minVolumes in descending order
        discounts = Discount.query.order_by(Discount.minVolumes.desc()).all()

        discount_to_apply = None
        for discount in discounts:
            if discount.minVolumes <= total_volumes <= discount.maxVolumes:
                discount_to_apply = discount
                break

        total_earning = issue1.issueCost + (issue2.issueCost if issue2 else 0) + (issue3.issueCost if issue3 else 0)

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
            customerID=customer_id,
            issID=iss_id,
            issID2=iss_id2 if iss_id2 != 0 else None,  # Store only non-zero issue IDs, or None
            issID3=iss_id3 if iss_id3 != 0 else None,  # Store only non-zero issue IDs, or None
            earning=total_earning,
            discountID=discount_id
        )

        db.session.add(new_sale)
        db.session.commit()
        return jsonify(new_sale.as_dict()), 201

    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error during sale creation", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ---------------------- RUN APP ----------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)