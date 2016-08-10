import random
import json
import requests
import logging
import pytz
from datetime import datetime


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.DEBUG,
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='logger.log')


def enter_account():
    """
    Verify account name (number)
    """
    account = 0
    while True:
        try:
            account = int(input("Enter your account number: "))
        except ValueError:
            print("Please, enter valid numeric data")
            continue

        # May be use data base or something
        if account <= 0:
            print("Please, enter valid account number.")
            continue
        else:
            break
    return account


def enter_money():
    """
    Verify amount of money, e.g. you can't enter amount that is less than zero
    """
    amount_of_money = 0
    while True:
        try:
            amount_of_money = float(input("Enter the amount of money you want to put to your account: "))
        except ValueError:
            print("Please, enter numeric data")
            continue

        if amount_of_money <= 0:
            print("Please, enter valid amount of money (greater than zero)")
            continue
        else:
            break
    return "{0:.2f}".format(amount_of_money)


def exit_clause():
    while True:
        answer = input('Do you want to continue? [y/n]: ')
        if answer.lower().startswith("y"):
            return 1
        elif answer.lower().startswith("n"):
            exit()


def make_single_process_json(point_id, timestamp, transaction_id, service_id, account, money, fee, params):
    json_data = {
        "single_process":
            {
                "point_id": str(point_id),
                "datetime": str(timestamp),
                "external_transaction_id": str(transaction_id),
                "service_id": str(service_id),
                "service_key": str(account),
                "amount": str(money),
                "fee": str("{0:.2f}".format(fee)),
                "params": params
            }
    }
    return json_data


def make_request(url, data, certificates, verify_cert):
    """
    Wrapper for data request which enables us to us try/catch if something goes wrong
    :param url: our URL
    :param data: json data
    :param certificates: cert.pem file
    :param verify_cert: (cert, key) pem files
    :return: json with output data from response
    """
    user_agent = '1.5.0'
    headers = {'User-Agent': user_agent, 'Content-Type': 'application/json'}
    logging.info("Generated JSON: {0}".format(json.dumps(data, indent=4)))
    try:
        resp = requests.post(
            url,
            json.dumps(data),
            headers=headers,
            verify=verify_cert,
            cert=certificates)
        if resp.status_code == 200:
            json_data = json.loads(resp.text)
            return json_data
        else:
            logging.info("Response body: {0}\nHTTP Code: {1}".format(resp.text, resp.status_code))
            return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def main():
    """
    Basic workflow
    """

    # unsigned int64 -> from 0 to 18,446,744,073,709,551,615
    limit64 = 18446744073709551615

    while True:
        # Initialize and enter required values
        account = enter_account()
        amount_of_money = enter_money()
        service_id = 1001351861392575516
        point_id = 1001469740754200645
        transaction_id = random.randint(0, limit64)
        timestamp = datetime.now(pytz.timezone('Europe/Moscow')).replace(microsecond=0).isoformat()
        # Fill json with our data to make request
        json_data = make_single_process_json(point_id, timestamp, transaction_id, service_id, account, amount_of_money,
                                             fee=0, params={})
        # Setup our SSL certificates (provide the path for the certificates)
        verify = "..."
        cert = (
            '...',
            '...')

        # Finally make the request with all required information
        output_json = make_request("...", json_data, cert, verify)
        if output_json is not None:
            # Output required results
            print("Code of operation is [{0}]\nDescription is [{1}]".format(
                output_json['single_process_answer']['code'],
                output_json['single_process_answer']['description']
            ))
            logging.info("Output JSON: {0}".format(json.dumps(output_json, indent=4)))
            exit_clause()
        else:
            print('Oops, something went wrong, Check logfile for additional information.')
            exit_clause()


if __name__ == '__main__':
    main()

"""
JSON Single-process request

{"single_process":
    {
    "point_id": "777",
    "datetime": "2012-01-01T11:12:13+04:00",
    "external_transaction_id": "34567843216789023456",
    "service_id": "123456",
    "service_key": "9876543210",
    "amount": "15.15",
    "fee": "0.10",
    "params":
        {
        "first_param_name": "first_param_value",
        "second_param_name": "second_param_value"
        }
    }
}

JSON Single-process answer

{"single_process_answer":
    {
    "id": "12345678",
    "point_id": "777",
    "external_transaction_id": "34567843216789023456",
    "code": "0",
    "description": "OK",
    "datetime": "2012-01-01T11:12:13+04:00"
    }
}
"""
