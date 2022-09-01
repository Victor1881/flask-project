from sqlalchemy import func

from db import db


class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.String(255), nullable=False)
    recipient_id = db.Column(db.String(255), nullable=False)
    transfer_id = db.Column(db.String(255), nullable=False)
    target_account_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    donation_id = db.Column(db.Integer, db.ForeignKey('donation.id'), nullable=False)
    send = db.Column(db.Boolean, default=False)
    donation = db.relationship('Donation')
    pdf = db.Column(db.String, nullable=False)