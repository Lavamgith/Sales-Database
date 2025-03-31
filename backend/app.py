from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Configure Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:my_sql_lm_1995@localhost/magazine_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ---------------------- ENTITY MODELS ----------------------

class Magazine(db.Model):
    magazine_id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255))
    year_published = db.Column(db.Integer)
    total_subscribers = db.Column(db.Integer)
    magCost = db.Column(db.Float)
    total_earnings = db.Column(db.Float)

    # Relationship with Volume, cascade deletes volumes when magazine is deleted
    volumes = db.relationship('Volume', backref='magazine', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Volume(db.Model):
    vol_id = db.Column(db.Integer, primary_key=True)
    magazine_id = db.Column(db.Integer, db.ForeignKey('magazine.magazine_id'), nullable=False)
    vol_num = db.Column(db.Integer)
    year_published = db.Column(db.Integer)
    subscriber_count = db.Column(db.Integer)
    volCost = db.Column(db.Float)

    # Relationship with Issue, cascade deletes issues when volume is deleted
    issues = db.relationship('Issue', backref='volume', cascade='all, delete-orphan')

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Issue(db.Model):
    issue_id = db.Column(db.Integer, primary_key=True)
    vol_id = db.Column(db.Integer, db.ForeignKey('volume.vol_id'), nullable=False)
    issue_number = db.Column(db.Integer)
    issueCost = db.Column(db.Float)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    address = db.Column(db.String(255))

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    biography = db.Column(db.Text)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'), nullable=False)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Sale(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.issue_id'), nullable=False)
    sale_price = db.Column(db.Float)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Discount(db.Model):
    discount_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    percentage = db.Column(db.Float)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

# ---------------------- CRUD ROUTES ----------------------

# ➤ POST (CREATE)
@app.route('/<entity>', methods=['POST'])
def create_entity(entity):
    models = {"magazines": Magazine, "volumes": Volume, "issues": Issue, "customers": Customer, "authors": Author, "articles": Article, "sales": Sale, "discounts": Discount}
    if entity not in models:
        return jsonify({"error": "Invalid entity"}), 400
    
    data = request.get_json()
    new_entry = models[entity](**data)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.as_dict()), 201

# ➤ GET (READ)
@app.route('/<entity>', methods=['GET'])
def get_entities(entity):
    models = {"magazines": Magazine, "volumes": Volume, "issues": Issue, "customers": Customer, "authors": Author, "articles": Article, "sales": Sale, "discounts": Discount}
    if entity not in models:
        return jsonify({"error": "Invalid entity"}), 400
    
    records = models[entity].query.all()
    return jsonify([record.as_dict() for record in records])

# ➤ PUT (UPDATE)
@app.route('/<entity>/<int:id>', methods=['PUT'])
def update_entity(entity, id):
    models = {"magazines": Magazine, "volumes": Volume, "issues": Issue, "customers": Customer, "authors": Author, "articles": Article, "sales": Sale, "discounts": Discount}
    if entity not in models:
        return jsonify({"error": "Invalid entity"}), 400
    
    record = models[entity].query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(record, key, value)
    db.session.commit()
    return jsonify(record.as_dict())

# ➤ DELETE
@app.route('/<entity>/<int:id>', methods=['DELETE'])
def delete_entity(entity, id):
    models = {"magazines": Magazine, "volumes": Volume, "issues": Issue, "customers": Customer, "authors": Author, "articles": Article, "sales": Sale, "discounts": Discount}
    if entity not in models:
        return jsonify({"error": "Invalid entity"}), 400
    
    record = models[entity].query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": f"{entity[:-1]} deleted successfully!"})

# ---------------------- RUN APP ----------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

