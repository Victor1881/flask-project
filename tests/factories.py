import factory

from db import db
from models import User, UserRole, DonatorsRewards, Donation, Donate


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class UserFactory(BaseFactory):
    class Meta:
        model = User
    id = factory.sequence(lambda n: n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    iban = factory.Faker('iban')
    role = UserRole.user
    donator_status = DonatorsRewards.novice


class VipDonatorFactory(BaseFactory):
    class Meta:
        model = User
    id = factory.sequence(lambda n: n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    iban = factory.Faker('iban')
    role = UserRole.user
    donator_status = DonatorsRewards.vip


class DonationFactory(BaseFactory):
    class Meta:
        model = Donation
    id = factory.sequence(lambda n: n)
    amount = factory.Faker('amount')
    received_money = factory.Faker('received_money')
    complete = factory.Faker('complete')
    admin_id = factory.Faker('admin_id')


class DonateFactory(BaseFactory):
    class Meta:
        model = Donate
    id = factory.sequence(lambda n: n)
    amount = factory.Faker('amount')
    donation_id = factory.Faker('donation_id')
    user_id = factory.Faker('user_id')
    total = factory.Faker('total')
    biggest_amount = factory.Faker('biggest_amount')
