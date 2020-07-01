from datetime import datetime, timedelta
from jinja2 import Template
from plaid import Client
import os
import re

PLAID_CLIENT_ID = '5dcd8e7d0f92430011ae11cf'
PLAID_PUBLIC_KEY = '6cd2c536928d3af1754097031ed25e'
PLAID_SECRET = os.getenv('PLAID_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
THIS_DIR = os.path.dirname(os.path.realpath(__file__))

PERCENTAGE = 40
LIST = [{'regex': '^City of Austin T PAYMENT', 'description': 'Electric'},
        {'regex': '^TIAACREF-BACL344 WEB PMTS', 'description': 'Rent'},
        {'regex': '^SPECTRUM', 'description': 'Internet'}]


def get_transactions(client_id, public_key, secret, access_token):
    """ Gets today's transactions given the credentials and access_token """
    end_date = datetime.strftime(datetime.today() - timedelta(10), '%Y-%m-%d')
    start_date = datetime.strftime(datetime.today() - timedelta(10), '%Y-%m-%d')

    client = Client(client_id=client_id,
                    secret=secret,
                    public_key=public_key,
                    environment='development',
                    suppress_warnings=True)
    response = client.Transactions.get(access_token,
                                       start_date=start_date,
                                       end_date=end_date)
    results = response['transactions']
    while len(results) < response['total_transactions']:
        response = client.Transactions.get(access_token,
                                           start_date=start_date,
                                           end_date=end_date,
                                           offset=len(results))
        results.extend(response['transactions'])
    return results


def get_splittables():
    transactions = get_transactions(PLAID_CLIENT_ID, PLAID_PUBLIC_KEY, PLAID_SECRET, ACCESS_TOKEN)
    month = datetime.strftime(datetime.today().replace(day=1) - timedelta(1), '%B')

    # Create separate names and descriptions lists for easy indexing
    regex = [x['regex'] for x in LIST]
    descriptions = [x['description'] for x in LIST]

    # Loop through all transactions
    to_split = list()
    total_total_amount = 0
    total_amount_owed = 0
    for transaction in transactions:
        for i, v in enumerate(regex):
            if re.match(v, transaction['name'], re.IGNORECASE):
                # Create new item to be split
                total_amount = float(transaction['amount'])
                amount_owed = total_amount * PERCENTAGE / 100
                date = datetime.strptime(transaction['date'], '%Y-%m-%d')
                total_total_amount += total_amount
                total_amount_owed += amount_owed
                to_split.append({'description': descriptions[i], 'date': date,
                                 'total_amount': '{:,.2f}'.format(total_amount),
                                 'amount_owed': '{:,.2f}'.format(amount_owed)})

    # Generate HTML email body based on to_split list
    if len(to_split) == 0:
        email_body = None
        subject = None
    elif len(to_split) == 1:
        t = Template(open(os.path.join(THIS_DIR, 'templates/expenses-single.html'), 'r').read())
        email_body = t.render(transaction=to_split[0])
        subject = '💸 {} {} Bill'.format(to_split[0]['date'].strftime('%B'), to_split[0]['description'])
    else:
        t = Template(open(os.path.join(THIS_DIR, 'templates/expenses-multi.html'), 'r').read())
        email_body = t.render(transactions=to_split, month=month,
                              total_amount='{:,.2f}'.format(total_total_amount),
                              amount_owed='{:,.2f}'.format(total_amount_owed))
    return email_body
