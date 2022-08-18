from db import db


def add(table_name, d):
    data = table_name(**d)
    db.session.add(data)
    db.session.flush()
    return data
