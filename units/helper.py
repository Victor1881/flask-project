from werkzeug.exceptions import BadRequest

from db import db
from models import Donation, Donate, User, DonatorsRewards


def add(table_name, d):
    data = table_name(**d)
    db.session.add(data)
    db.session.flush()
    return data


def valid_donation(id_d):
    donation = Donation.query.filter_by(id=id_d).first()
    if not donation:
        raise BadRequest("No donation found with the given id")
    return donation


def top_donators(data):
    donators, checked_users = [], []
    biggest_amount, total = 0, 0
    for x in Donate.query.filter_by(donation_id=data["donation_id"]).all():
        if x.user_id in checked_users:
            continue
        user_id = x.user_id
        checked_users.append(x.user_id)
        for y in Donate.query.filter_by(donation_id=data["donation_id"]).all():
            if user_id == y.user_id:
                total += y.amount
                if y.amount > biggest_amount:
                    biggest_amount = y.amount

        for c in Donate.query.filter_by(user_id=x.user_id, donation_id=data['donation_id']).all():
            c.biggest_amount = biggest_amount
            c.total = total

        donators.append(x)
        biggest_amount, total = 0, 0

    donators = sorted(donators, key=lambda x: x.total, reverse=True)[:3]
    newlist = []
    for x in donators:
        user = User.query.filter_by(id=x.user_id).first()
        newlist.append(
            f'{user.first_name} {user.last_name} has donated total {x.total} with biggest donation {x.biggest_amount}')

    return newlist


def donator_reward(user):
    total = sum((d.amount for d in Donate.query.filter_by(user_id=user.id).all()))
    if 50 < total <= 100:
        user.donator_status = DonatorsRewards.normal
    elif 100 < total <= 500:
        user.donator_status = DonatorsRewards.super
    elif 500 < total <= 1000:
        user.donator_status = DonatorsRewards.elite
    elif 1000 < total <= 2000:
        user.donator_status = DonatorsRewards.vip
    elif 2000 < total <= 5000:
        user.donator_status = DonatorsRewards.legendary
    elif total > 5000:
        user.donator_status = DonatorsRewards.mythic