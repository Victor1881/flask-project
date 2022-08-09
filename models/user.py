from db import db
from models.enum import UserRole


class BaseUser(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    iban = db.Column(db.String(22), nullable=False)


class User(BaseUser):
    __tablename__ = 'users'

    role = db.Column(db.Enum(UserRole), default=UserRole.user, nullable=False)
    donation_id = db.relationship("Donation", backref="donation", lazy='dynamic')


''' create donation нова таблица където само админ може да създава в нея '''