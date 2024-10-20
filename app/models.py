from app import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    subject = db.Column(db.String(128), nullable=False)
    message = db.Column(db.Text, nullable=False)
