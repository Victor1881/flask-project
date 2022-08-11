import json
import uuid
import requests
from decouple import config


class WiseService:
    def __init__(self):
        self.token = config("WISE_KEY")
        self.headers = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {self.token}"}
        self.main_url = config("WISE_URL")
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = f"{self.main_url}/v1/profiles"
        resp = requests.get(url, headers=self.headers)
        data = resp.json()
        profile_id = [o["id"] for o in data if o["type"] == "personal"][0]
        return profile_id

    def create_quote(self, source_currency, target_currency, amount):
        url = f"{self.main_url}/v2/quotes"
        data = {
            "sourceCurrency": source_currency,
            "targetCurrency": target_currency,
            "targetAmount": amount,
            "profile": self.profile_id
        }
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.json()["id"]

    def create_recipient(self, full_name, iban):
        url = f"{self.main_url}/v1/accounts"
        data = {
          "currency": "EUR",
          "type": "iban",
          "profile": self.profile_id,
          "accountHolderName": full_name,
           "details": {
              "legalType": "PRIVATE",
              "iban": iban
            }
        }
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.json()["id"]

    def create_transfer(self, recipient_account_id, quote_id, customer_transaction_id):
        url = f"{self.main_url}/v1/transfers"
        data = {
          "targetAccount": recipient_account_id,
          "quoteUuid": quote_id,
          "customerTransactionId": customer_transaction_id,
         }
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.json()

    def fund_transfer(self, transfer_id):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        data = {"type": "BALANCE"}
        resp = requests.post(url, json=data, headers=self.headers)
        return resp.json()


if __name__ == '__main__':
    wise = WiseService()
    quote_id = wise.create_quote("EUR", "EUR", 20)
    recipient_id = wise.create_recipient("Quandle Dingle", "DE89370400440532013000")
    customer_transaction = str(uuid.uuid4())
    transfer_id = wise.create_transfer(recipient_id, quote_id, customer_transaction)["id"]
    print(wise.fund_transfer(transfer_id))