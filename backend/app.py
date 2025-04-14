import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

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

    # Relationships
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

    # Relationships
    issues = db.relationship('Issue', backref='volume', cascade='all, delete-orphan')
    # Remove this line:
    # sales = db.relationship('Sale', backref='volume', cascade='all, delete-orphan')

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

    # Relationships
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

    # Relationships
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

    # Relationships
    sales = db.relationship('Sale', backref='customer', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Sale(db.Model):
    __tablename__ = 'sales'
    saleID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey('customer.customerID', ondelete='CASCADE'), nullable=False)
    discountID = db.Column(db.Integer, db.ForeignKey('discount.discountID', ondelete='SET NULL'), server_default='0', nullable=True) # Changed nullable=False to nullable=True
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

    # Relationships
    sales = db.relationship('Sale', backref='discount', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

# ---------------------- CRUD ROUTES ----------------------

# Helper function to get model by entity name
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

# ➤ POST (CREATE)
@app.route('/<entity>', methods=['POST'])
def create_entity(entity):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Special handling for Article since it has a string primary key
        if entity == 'articles':
            if 'articleTitle' not in data:
                return jsonify({"error": "Article title is required"}), 400
        
        # Adjusting for Magazine attributes
        if entity == 'magazines':
            new_entry = model(
                magazineTitle=data.get('magazineTitle'),
                yearPublished=data.get('yearPublished'),
                magazineCost=data.get('magazineCost'),
                totalSubscribers=data.get('totalSubscribers'),
                totalEarnings=data.get('totalEarnings'),
                website=data.get('website'),
                magazineID=data.get('magazineID'),
                adminID=data.get('adminID'),
                adminID2=data.get('adminID2')
            )
        elif entity == 'admins':
            new_entry = model(
                adminID=data.get('adminID'),
                phoneNumber=data.get('phoneNumber'),
                name=data.get('name'),
                email=data.get('email'),
                role=data.get('role')
            )
        elif entity == 'volumes':
            new_entry = model(
                volID=data.get('volID'),
                magID=data.get('magID'),
                volNum=data.get('volNum'),
                yearPublished=data.get('yearPublished'),
                volumeCost=data.get('volumeCost'),
                subscriberCount=data.get('subscriberCount')
            )
        elif entity == 'issues':
            new_entry = model(
                issueID=data.get('issueID'),
                volID=data.get('volID'),
                issNum=data.get('issNum'),
                season=data.get('season'),
                issueCost=data.get('issueCost'),
                backCopiesSold=data.get('backCopiesSold')
            )
        elif entity == 'articles':
            new_entry = model(
                articleTitle=data.get('articleTitle'),
                authorID=data.get('authorID'),
                magID2=data.get('magID2'),
                volID2=data.get('volID2'),
                issueID=data.get('issueID'),
                topic=data.get('topic')
            )
        elif entity == 'authors':
            new_entry = model(
                authorID=data.get('authorID'),
                name=data.get('name'),
                email=data.get('email')
            )
        elif entity == 'customers':
            new_entry = model(
                customerID=data.get('customerID'),
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                address=data.get('address')
            )
        elif entity == 'sales':
            new_entry = model(
                saleID=data.get('saleID'),
                customerID=data.get('customerID'),
                discountID=data.get('discountID'),
                issID=data.get('issID'),
                issID2=data.get('issID2'),
                issID3=data.get('issID3'),
                earning=data.get('earning')
            )
        elif entity == 'discounts':
            new_entry = model(
                discountID=data.get('discountID'),
                minVolumes=data.get('minVolumes'),
                maxVolumes=data.get('maxVolumes'),
                discountPercentage=data.get('discountPercentage'),
                discountCode=data.get('discountCode')
            )
        else:
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

# ➤ GET (READ)
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
        # Adjusting for primary key names
        if entity == 'admins':
            record = model.query.get(int(id))
        elif entity == 'magazines':
            record = model.query.get(int(id))
        elif entity == 'volumes':
            record = model.query.get(int(id))
        elif entity == 'issues':
            record = model.query.get(int(id))
        elif entity == 'articles':
            record = model.query.get(id)
        elif entity == 'authors':
            record = model.query.get(int(id))
        elif entity == 'customers':
            record = model.query.get(int(id))
        elif entity == 'sales':
            record = model.query.get(int(id))
        elif entity == 'discounts':
            record = model.query.get(int(id))
        else:
            record = model.query.get(int(id))
        
        if not record:
            return jsonify({"error": f"{entity.capitalize()} not found"}), 404
        return jsonify(record.as_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ➤ PUT (UPDATE)
@app.route('/<entity>/<id>', methods=['PUT'])
def update_entity(entity, id):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Adjusting for primary key names
        if entity == 'admins':
            record = model.query.get(int(id))
        elif entity == 'magazines':
            record = model.query.get(int(id))
        elif entity == 'volumes':
            record = model.query.get(int(id))
        elif entity == 'issues':
            record = model.query.get(int(id))
        elif entity == 'articles':
            record = model.query.get(id)
        elif entity == 'authors':
            record = model.query.get(int(id))
        elif entity == 'customers':
            record = model.query.get(int(id))
        elif entity == 'sales':
            record = model.query.get(int(id))
        elif entity == 'discounts':
            record = model.query.get(int(id))
        else:
            record = model.query.get(int(id))
        
        if not record:
            return jsonify({"error": f"{entity.capitalize()} not found"}), 404
        
        for key, value in data.items():
            setattr(record, key, value)
        db.session.commit()
        return jsonify(record.as_dict())
    
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ➤ DELETE
@app.route('/<entity>/<id>', methods=['DELETE'])
def delete_entity(entity, id):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404
    
    try:
        # Adjusting for primary key names
        if entity == 'admins':
            record = model.query.get(int(id))
        elif entity == 'magazines':
            record = model.query.get(int(id))
        elif entity == 'volumes':
            record = model.query.get(int(id))
        elif entity == 'issues':
            record = model.query.get(int(id))
        elif entity == 'articles':
            record = model.query.get(id)
        elif entity == 'authors':
            record = model.query.get(int(id))
        elif entity == 'customers':
            record = model.query.get(int(id))
        elif entity == 'sales':
            record = model.query.get(int(id))
        elif entity == 'discounts':
            record = model.query.get(int(id))
        else:
            record = model.query.get(int(id))
        
        if not record:
            return jsonify({"error": f"{entity.capitalize()} not found"}), 404
        
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": f"{entity.capitalize()} deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ---------------------- RUN APP ----------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)