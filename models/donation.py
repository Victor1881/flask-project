from db import db


class Donation(db.Model):
    __tablename__ = 'donation'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    received_money = db.Column(db.Float, default=0, nullable=False)
    complete = db.Column(db.Boolean, default=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin = db.relationship('User')