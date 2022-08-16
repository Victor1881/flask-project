from werkzeug.exceptions import BadRequest

from db import db
from models import Donation
from services.wise import WiseService
from units.helper import valid_donation

wise = WiseService()


class DonationManager:
    @staticmethod
    def create_donation(donation_data, user):
        donation_data['admin_id'] = user.id
        donation = Donation(**donation_data)
        db.session.add(donation)
        db.session.commit()

    @staticmethod
    def donation_status(data):
        try:
            valid_donation(data['donation_id'])
            donation = Donation.query.filter_by(id=data['donation_id']).first()
            if donation.complete:
                return 'Donation is completed'
            return f'Donation received {donation.received_money:.0f} from {donation.amount} need {donation.amount - donation.received_money:.0f}'
        except KeyError:
            raise BadRequest('No donation id given')




