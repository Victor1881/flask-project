from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.donate import DonateManager
from managers.donation import DonationManager
from models import UserRole
from schemas.donation import DonateSchemaRequest
from units.decorators import permission_required, validate_schema


class CreateDonation(Resource):
    @auth.login_required
    @permission_required(UserRole.user)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        donation = DonationManager.create_donation(data, current_user)
        return donation

    @auth.login_required
    def get(self):
        data = request.get_json()
        message = DonationManager.donation_status(data)
        return message


class Donate(Resource):
    @auth.login_required
    @validate_schema(DonateSchemaRequest)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        message = DonateManager.donate(data, current_user)
        return message

    @auth.login_required
    def get(self):
        data = request.get_json()
        donators = DonateManager.get_donators(data)
        return [x for x in donators]


