from datetime import datetime, timedelta
from plaid import Client
from .logger import log
import os
import re

PLAID_CLIENT_ID = '5dcd8e7d0f92430011ae11cf'
PLAID_PUBLIC_KEY = '6cd2c536928d3af1754097031ed25e'
PLAID_SECRET = os.getenv('PLAID_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
THIS_DIR = os.path.dirname(os.path.realpath(__file__))

PERCENTAGE = 35
LIST = [{'regex': '^City of Austin T PAYMENT', 'description': 'Electric'},
        {'regex': '^Folio WEB PMTS', 'description': 'Rent'},
        {'regex': '^SPECTRUM', 'description': 'Internet'}]


def get_transactions(client_id, public_key, secret, access_token):
    """ Gets today's transactions given the credentials and access_token """

    last_last_month = datetime.today().replace(day=1) - timedelta(1)
    first_last_month = last_last_month.replace(day=1)

    start_date = datetime.strftime(first_last_month, '%Y-%m-%d')
    end_date = datetime.strftime(last_last_month, '%Y-%m-%d')

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


def expenses():
    """ Get the known splittable expenses """
    log.info('Getting Transactions')
    raise Exception('IDK WHATS HAPPENING')
    transactions = get_transactions(PLAID_CLIENT_ID,
                                    PLAID_PUBLIC_KEY,
                                    PLAID_SECRET,
                                    ACCESS_TOKEN)
    results = {'found': False, 'transactions': [], 'total': 0, 'owed': 0}

    # Create separate names and descriptions lists for easy indexing
    regex = [x['regex'] for x in LIST]
    descriptions = [x['description'] for x in LIST]

    # Loop through all transactions
    for transaction in transactions:
        for i, v in enumerate(regex):
            if re.match(v, transaction['name'], re.IGNORECASE):
                # Create new item to be split
                total_amount = float(transaction['amount'])
                amount_owed = total_amount * PERCENTAGE / 100

                results['found'] = True
                results['total'] += total_amount
                results['owed'] += amount_owed
                results['transactions'].append({'description': descriptions[i],
                                                'amount': '{:,.2f}'.format(total_amount),
                                                'owed': '{:,.2f}'.format(amount_owed)})
    # Round to exactly two decimal places
    results['total'] = '{:,.2f}'.format(results['total'])
    results['owed'] = '{:,.2f}'.format(results['owed'])
    return results
