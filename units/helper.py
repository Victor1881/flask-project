from werkzeug.exceptions import BadRequest

from db import db
from models import Donation


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