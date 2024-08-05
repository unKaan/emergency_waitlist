from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    wait_time = db.Column(db.Integer, nullable=False)