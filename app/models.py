from app import db

class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)