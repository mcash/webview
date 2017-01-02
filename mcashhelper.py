import requests as r
import uuid


URL = 'https://api.mca.sh'
# URL = 'https://mcashtestbed.appspot.com'
MERCHANT_ID = ''
MERCHANT_USER = ''
SECRET = ''
# TESTBED_TOKEN = ''  # Sign up at https://mcashtestbed.appspot.com/testbed/signup/
SHORTLINK = 'http://mca.sh/s/XXXXXX/'  # You can create a new one at /generate_shortlink


headers = {
    'X-Mcash-Merchant': MERCHANT_ID,
    'X-Mcash-User': MERCHANT_USER,
    'Authorization': 'SECRET ' + SECRET,
}


def create_shortlink(callback_uri):
    url = URL + '/merchant/v1/shortlink/'
    data = {'callback_uri': callback_uri}
    res = r.post(url, json=data, headers=headers)
    sid = res.json().get('id', '')
    return (sid, res) if sid else (None, res)


def create_payment_request(amount, scan_token):
    url = URL + '/merchant/v1/payment_request/'
    data = {
        'amount': amount,
        'customer': scan_token,
        'currency': 'NOK',
        'pos_id': 'webview_demo',
        'pos_tid': str(uuid.uuid4()),
        'allow_credit': True,
        'action': 'sale'
    }
    res = r.post(url, json=data, headers=headers)
    tid = res.json().get('id', '')
    return tid if tid else None

