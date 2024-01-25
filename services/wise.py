import uuid

import requests
from decouple import config


TARGET_CURRENCY = 'BGN'

class WiseService:
    def __init__(self):
        self.base_url = config('WISE_URL')
        self.headers = {
        'Authorization': f'Bearer {config("WISE_TOKEN")}',
        'Content-type': 'application/json'
        }
        self.profile_id = config('PROFILE_ID')

    def create_quota(self, amount):
        url = f'{self.base_url}/v3/profiles/{self.profile_id}/quotes'
        body = {
            "sourceCurrency": "GBP",
            "targetCurrency": TARGET_CURRENCY,
            "sourceAmount": amount
        }

        response = requests.post(url,  json=body, headers=self.headers)
        return response.json()['id']


# def _get_profile_id(headers):
#     url = 'https://api.sandbox.transferwise.tech/v1/profiles'
#     resp = requests.get(url, headers=headers)
#
#     resp = resp.json()
#     return resp

    def create_recipient_account(self, full_name, iban):
        url = url = f'{self.base_url}/v1/accounts'
        body = {
            "currency": TARGET_CURRENCY,
            "type": "IBAN",
            "profile": self.profile_id,
            "ownedByCustomer": False,
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "iban": iban
            }
        }
        response = requests.post(url, json=body, headers=self.headers, )
        return response.json()['id']

    def create_transfer(self, quote_id, recipient_id, transaction_id):
        url = url = f'{self.base_url}/v1/transfers'
        body = {
          "targetAccount": recipient_id,
          "quoteUuid": quote_id,
          "customerTransactionId": transaction_id,
          "details": {
              # "reference" : "to my friend",
              # "transferPurpose": "verification.transfers.purpose.pay.bills",
              # "transferPurposeSubTransferPurpose": "verification.sub.transfers.purpose.pay.interpretation.service"
              # "sourceOfFunds": "verification.source.of.funds.other"
            }
         }
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()['id']

    def fund_transfer(self, transfer_id):
        url = f'{self.base_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments'
        body = {
            "type": "BALANCE"
        }
        response = requests.post(url, json=body, headers=self.headers)
        return response

    def cancel_transfer(self, transfer_id):
        url = f'{self.base_url}/v1/transfers/{transfer_id}/cancel'

        response = requests.put(url, json={}, headers=self.headers)
        return response



if __name__ == '__main__':
    wise_service = WiseService()
    wise_service.cancel_transfer(52830240)
    # quote_id = wise_service.create_quota(150)
    # recipient_id = wise_service.create_recipient_account('Buba Mara', 'BG80BNBG96611020345678')
    # transaction_id = str(uuid.uuid4())
    # transfer_id = wise_service.create_transfer(quote_id, recipient_id, transaction_id)
    # print(_get_profile_id(headers))
    # print(quote_id)
    # print(recipient_id)
    # print(transfer_id())

