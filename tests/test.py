from flask_testing import TestCase

from config import create_app
from db import db
from tests.factories import UserFactory, DonationFactory, DonateFactory, VipDonatorFactory
from tests.helper import generate_user_token

ENDPOINTS = (
        ("/create/", "GET"),
        ("/create/", "POST"),
)


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def iterate_endpoints(self, endpoints_data, status_code_method, expected_resp, headers=None, payload=None):
        if not headers:
            headers = {}
        if not payload:
            payload = {}

        resp = None
        for url, method in endpoints_data:
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            elif method == "POST":
                resp = self.client.post(url, headers=headers)

        status_code_method(resp)
        self.assertEqual(resp.json, expected_resp)

    def test_login_required(self):

        self.iterate_endpoints(ENDPOINTS, self.assert_401, {"message": "Missing token"})

    def test_invalid_token_raises(self):
        header = {"Authorization": "Bearer dsadac"}
        self.iterate_endpoints(ENDPOINTS, self.assert_401, {"message": "Invalid token"}, header)

    def test_missing_permissions_for_vip__legendary__mythic_user(self):
        endpoint = (
            ("/create/", "POST"),
        )

        user = UserFactory()
        token = generate_user_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        resp = None
        for url, method in endpoint:
            if method == "POST":
                resp = self.client.post(url, headers=headers)
            self.assert_403(resp)
            self.assertEqual(resp.json, {"message": "Permission denied"})

    def test_reward_user(self):
        user = UserFactory()
        donation = DonationFactory(admin_id=user.id, complete=False, received_money=500, amount=1000)
        DonateFactory(user_id=user.id, donation_id=donation.id, amount=500, biggest_amount=500, total=500)
        url = f"/user/{user.id}/reward/"
        token = generate_user_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        resp = self.client.put(url, headers=headers)
        self.assertEqual(resp.json, {"message": f"{user.first_name} {user.last_name} became {user.donator_status.value}"})

    def test_reward_user__return_no_changes(self):
        user = VipDonatorFactory()
        donation = DonationFactory(admin_id=user.id, complete=False, received_money=1000, amount=10000)
        DonateFactory(user_id=user.id, donation_id=donation.id, amount=1000, biggest_amount=1000, total=1000)
        url = f"/user/{user.id}/reward/"
        token = generate_user_token(user)
        headers = {"Authorization": f"Bearer {token}"}
        resp = self.client.put(url, headers=headers)
        self.assertEqual(resp.json, {"message": f"No changes"})

