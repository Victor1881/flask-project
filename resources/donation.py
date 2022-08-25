from flask import request
from flask_restful import Resource
from flask_api import status
from managers.auth import auth
from managers.donate import DonateManager
from managers.donation import DonationManager
from managers.users import UserManager
from models import DonatorsRewards
from schemas.donation import DonateSchemaRequest
from units.decorators import permission_required, validate_schema


class CreateDonation(Resource):
    @auth.login_required
    @permission_required(DonatorsRewards.vip, DonatorsRewards.legendary, DonatorsRewards.mythic)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        donation = DonationManager.create_donation(data, current_user)
        return status.HTTP_201_CREATED

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


class Reward(Resource):
    @auth.login_required
    def put(self, id):
        message = UserManager.reward(id)
        return message


class DeleteUser(Resource):
    @auth.login_required
    def delete(self, id):
        UserManager.delete_user(id)

