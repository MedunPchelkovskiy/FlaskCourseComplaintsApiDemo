import requests
from decouple import config

profile_id = None

url = 'https://api.sandbox.transferwise.tech/v3/profiles/{{profileId}}/quotes'
headers = {
    'Authorization': f'Bearer 0f92f2de-5a0f-4369-beb0-87eececb8661',
    'Content-Type': 'application/json'
}
body = {
            'sourceCurrency': 'GBP',
            'targetCurrency': 'USD',
            'sourceAmount': 100,
}


if __name__ == '__main__':
    response = requests.post(url, body, headers=headers)
    print(response.status_code)
    print(response.json())
