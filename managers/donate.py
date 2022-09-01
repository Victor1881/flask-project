import os
import uuid

from werkzeug.exceptions import FailedDependency, BadRequest
from werkzeug.utils import secure_filename

from models import TransactionModel, Donate
from services.wise import WiseService
from units.helper.db import add
from units.helper.donate_helper import valid_donation, top_donators

wise = WiseService()


class DonateManager:
    @staticmethod
    def donate(data, user):
        data['user_id'] = user.id
        donation = valid_donation(data['donation_id'])
        if donation.complete:
            raise FailedDependency("The money have been collected")
        DonateManager.issue_transaction(data["amount"], f"{user.first_name} {user.last_name}",
                                        user.iban, data['donation_id'], user)
        add(Donate, data)
        donation.received_money += int(data['amount'])
        if donation.received_money >= donation.amount:
            donation.complete = True
        return {"message": "Thank you for your donation"}

    @staticmethod
    def issue_transaction(amount, full_name, iban, donation_id, user):
        quote_id = wise.create_quote("EUR", "EUR", amount)
        recipient_id = wise.create_recipient(full_name, iban)
        customer_transaction = str(uuid.uuid4())
        transfer_id = wise.create_transfer(recipient_id, quote_id, customer_transaction)["id"]
        wise.get_pdf_transfer(transfer_id, user.email, amount)
        data = {
            "quote_id": quote_id,
            "recipient_id": recipient_id,
            "transfer_id": transfer_id,
            "target_account_id": customer_transaction,
            "amount": amount,
            "donation_id": donation_id,
            "pdf": 'C:\\Users\\Victor Dimitrov\\Flaskprojects\\donation_project\\invoice.pdf',
        }
        donation = valid_donation(donation_id)
        if donation.admin_id == user.id:
            wise.cancel_transfer(transfer_id)
            raise BadRequest("Donation creator can't donate money to his own donation")

        if int(amount) > 2500:
            wise.cancel_transfer(transfer_id)
            raise BadRequest("Amount is more than the limit of 2500")
        add(TransactionModel, data)
        os.startfile(data['pdf'])
        transaction = [x for x in TransactionModel.query.filter_by(donation_id=donation_id).all() if not x.send][0]
        wise.fund_transfer(transaction.transfer_id)
        transaction.send = True

    @staticmethod
    def get_donators(data):
        try:
            valid_donation(data['donation_id'])
            donators = top_donators(data)
        except KeyError:
            raise BadRequest('No donation id given')

        return donators