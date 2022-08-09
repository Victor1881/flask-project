from db import db
from models import Donation


class DonationManager:
    @staticmethod
    def create_donation(donation_data, user):
        donation_data['admin_id'] = user.id
        donation = Donation(**donation_data)
        db.session.add(donation)
        db.session.commit()

    @staticmethod
    def give_money():
        pass
