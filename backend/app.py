import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

# Get environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Configure Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@localhost/magazine_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ---------------------- ENTITY MODELS ----------------------

class Magazine(db.Model):
    __tablename__ = 'magazine'
    magazine_id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255))
    year_published = db.Column(db.Integer)
    total_subscribers = db.Column(db.Integer)
    magCost = db.Column(db.Float)
    total_earnings = db.Column(db.Float)

    # Relationships
    volumes = db.relationship('Volume', backref='magazine', cascade='all, delete-orphan')
    articles = db.relationship('Article', backref='magazine', cascade='all, delete-orphan')
    sales = db.relationship('Sale', backref='magazine', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Volume(db.Model):
    __tablename__ = 'volume'
    vol_id = db.Column(db.Integer, primary_key=True)
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.magazine_id', ondelete='CASCADE'), nullable=False)
    vol_num = db.Column(db.Integer)
    year_published = db.Column(db.Integer)
    subscriber_count = db.Column(db.Integer)
    volCost = db.Column(db.Float)

    # Relationships
    issues = db.relationship('Issue', backref='volume', cascade='all, delete-orphan')
    sales = db.relationship('Sale', backref='volume', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Issue(db.Model):
    __tablename__ = 'issue'
    issue_id = db.Column(db.Integer, primary_key=True)
    vol_id = db.Column(db.Integer, db.ForeignKey('volume.vol_id', ondelete='CASCADE'), nullable=False)
    iss_num = db.Column(db.Integer)
    season = db.Column(db.String(50))
    back_copies_sold = db.Column(db.Integer)
    issCost = db.Column(db.Float)

    # Relationships
    articles = db.relationship('Article', backref='issue', cascade='all, delete-orphan')
    sales = db.relationship('Sale', backref='issue', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships
    articles = db.relationship('Article', backref='author', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Article(db.Model):
    __tablename__ = 'article'
    article_title = db.Column(db.String(255), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id', ondelete='CASCADE'), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.issue_id', ondelete='CASCADE'), nullable=False)
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.magazine_id', ondelete='CASCADE'), nullable=False)
    topic = db.Column(db.String(255))

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))

    # Relationships
    sales = db.relationship('Sale', backref='customer', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Discount(db.Model):
    __tablename__ = 'discount'
    discount_id = db.Column(db.Integer, primary_key=True)
    min_volumes = db.Column(db.Integer)
    max_volumes = db.Column(db.Integer)
    discount_percentage = db.Column(db.Float)
    discount_code = db.Column(db.String(50), unique=True)

    # Relationships
    sales = db.relationship('Sale', backref='discount', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Sale(db.Model):
    __tablename__ = 'sale'
    sale_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id', ondelete='CASCADE'), nullable=False)
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.magazine_id', ondelete='CASCADE'))
    vol_id = db.Column(db.Integer, db.ForeignKey('volume.vol_id', ondelete='CASCADE'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.issue_id', ondelete='CASCADE'))
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.discount_id', ondelete='SET NULL'))
    earning = db.Column(db.Float)

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
        'sales': Sale
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
            if 'article_title' not in data:
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
        # Handle Article which has string ID
        if entity == 'articles':
            record = model.query.get(id)
        else:
            record = model.query.get(int(id))
        
        if not record:
            return jsonify({"error": f"{entity[:-1]} not found"}), 404
        
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
        # Handle Article which has string ID
        if entity == 'articles':
            record = model.query.get(id)
        else:
            record = model.query.get(int(id))
        
        if not record:
            return jsonify({"error": f"{entity[:-1]} not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
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

# ➤ DELETE
@app.route('/<entity>/<id>', methods=['DELETE'])
def delete_entity(entity, id):
    model = get_model(entity)
    if not model:
        return jsonify({"error": "Invalid entity"}), 404
    
    try:
        # Handle Article which has string ID
        if entity == 'articles':
            record = model.query.get(id)
        else:
            record = model.query.get(int(id))
        
        if not record:
            return jsonify({"error": f"{entity[:-1]} not found"}), 404
        
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": f"{entity[:-1]} deleted successfully"})
    
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Cannot delete due to foreign key constraints", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ---------------------- RUN APP ----------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)