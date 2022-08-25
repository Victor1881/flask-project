from flask_testing import TestCase

from config import create_app
from db import db
from models import Donation
from tests.factories import VipDonatorFactory, DonationFactory
from tests.helper import generate_user_token


class TestDonation(TestCase):
    url = "/create/"

    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_donation_schema(self):
        donation = Donation.query.all()
        assert len(donation) == 0
        user = VipDonatorFactory()
        token = generate_user_token(user)
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json",
                   }
        data = {'amount': None, 'received_money': 0, 'complete': False, 'admin_id': 0}
        resp = self.client.post(self.url, headers=headers, json=data)
        self.assert_400(resp)
        assert resp.json == {}

        donation = Donation.query.all()
        assert len(donation) == 0

    def test_create_donation(self):
        user = VipDonatorFactory()
        token = generate_user_token(user)
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json",
                   }
        data = {
            "amount": "2000"
        }
        resp = self.client.post(self.url, headers=headers, json=data)
        assert resp.status_code == 200
        donation = Donation.query.all()
        assert len(donation) == 1

    def test_get_donation_status(self):
        user = VipDonatorFactory()
        token = generate_user_token(user)
        donation = DonationFactory(admin_id=user.id, complete=False, received_money=0, amount=1000)
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json",
                   }
        resp = self.client.get(self.url, headers=headers, json={"donation_id": donation.id})

        self.assertEqual(resp.json, {"message": f'Donation received {donation.received_money:.0f} from {donation.amount} need {donation.amount - donation.received_money:.0f}'})

    def test_get_donation_status_when_donation_is_completed(self):
        user = VipDonatorFactory()
        token = generate_user_token(user)
        donation = DonationFactory(admin_id=user.id, complete=True, received_money=1000, amount=1000)
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json",
                   }
        resp = self.client.get(self.url, headers=headers, json={"donation_id": donation.id})
        self.assertEqual(resp.json, {"message": "Donation is completed"})

    def test_get_donation_status_with_given_wrong_donation_id__raise_exception(self):
        user = VipDonatorFactory()
        token = generate_user_token(user)
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json",
                   }
        resp = self.client.get(self.url, headers=headers, json={"donation_id": 1})
        self.assert_400(resp)
        self.assertEqual(resp.json, {"message": "No donation found with the given id"})

    def test_get_donation_status_without_given_donation_id__raise_exception(self):
        user = VipDonatorFactory()
        token = generate_user_token(user)
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json",
                   }
        resp = self.client.get(self.url, headers=headers, json={})
        self.assert_400(resp)
        self.assertEqual(resp.json, {"message": "No donation id given"})
