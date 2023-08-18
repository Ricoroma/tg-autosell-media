import random
import string

import requests

from data.config import *
from data.db import get_settings


class QiwiWallet:

    def __init__(self, phone, api_token):
        self.s = requests.Session()
        self.s.headers['authorization'] = 'Bearer ' + api_token
        self.phone = phone

    def payment_history(self, rows_num=5) -> dict:
        parameters = {'rows': str(
            rows_num), 'nextTxnId': '', 'nextTxnDate': ''}
        h = self.s.get('https://edge.qiwi.com/payment-history/v2/persons/' +
                       self.phone + '/payments', params=parameters)
        return h.json()

    def check(self, comment, amount):
        last_payments = self.payment_history(40)
        try:
            for payment in last_payments['data']:
                qcomment = payment['comment']
                if comment in qcomment:
                    if payment['sum']['amount'] == amount:
                        return True
                    else:
                        return False
            return False
        except:
            return False


def random_order():
    return f"{random.randint(44, 77)}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}" \
           f"{random.randint(371, 984)}{random.choice(string.ascii_letters)}{random.randint(11, 24)}"


def check_qiwi(comment, amount):
    wallet = QiwiWallet(phone=get_settings()[1], api_token=qiwi_token)
    return wallet.check(comment, int(amount))
