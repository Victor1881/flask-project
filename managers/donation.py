from werkzeug.exceptions import BadRequest

from db import db
from models import Donation
from services.wise import WiseService
from units.helper.db import add
from units.helper.donate_helper import valid_donation

wise = WiseService()


class DonationManager:
    @staticmethod
    def create_donation(donation_data, user):
        donation_data['admin_id'] = user.id
        add(Donation, donation_data)

    @staticmethod
    def donation_status(data):
        try:
            valid_donation(data['donation_id'])
            donation = Donation.query.filter_by(id=data['donation_id']).first()
            if donation.complete:
                return {"message": 'Donation is completed'}
            return {"message": f'Donation received {donation.received_money:.0f} from {donation.amount} need {donation.amount - donation.received_money:.0f}'}
        except KeyError:
            raise BadRequest('No donation id given')




