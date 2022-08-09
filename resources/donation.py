from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.donation import DonationManager
from models import UserRole
from units.decorators import permission_required


class CreateDonation(Resource):
    @auth.login_required
    @permission_required(UserRole.user)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        donation = DonationManager.create_donation(data, current_user)
        return donation