from models import Donate, DonatorsRewards, Donation, TransactionModel, User


def donator_reward(user):
    total = sum((d.amount for d in Donate.query.filter_by(user_id=user.id).all()))
    user_status = user.donator_status
    if 50 <= total < 100:
        user.donator_status = DonatorsRewards.normal
    elif 100 <= total < 500:
        user.donator_status = DonatorsRewards.super
    elif 500 <= total < 1000:
        user.donator_status = DonatorsRewards.elite
    elif 1000 <= total < 2000:
        user.donator_status = DonatorsRewards.vip
    elif 2000 <= total < 5000:
        user.donator_status = DonatorsRewards.legendary
    elif total >= 5000:
        user.donator_status = DonatorsRewards.mythic

    if user_status == user.donator_status:
        return {"message": "No changes"}
    if user.donator_status == DonatorsRewards.novice:
        return "No changes"
    return {"message": f"{user.first_name} {user.last_name} became {user.donator_status.value}"}


def delete(user):
    Donate.query.filter_by(user_id=user.id).delete()
    for x in Donation.query.filter_by(admin_id=user.id).all():
        TransactionModel.query.filter_by(donation_id=x.id).delete()

    Donation.query.filter_by(admin_id=user.id).delete()
    User.query.filter_by(id=user.id).delete()