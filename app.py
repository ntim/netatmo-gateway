import requests
import flask
import os
import sys
import json

app = flask.Flask(__name__)

REDACTED_FIELDS = ['_id',
                   'cipher_id',
                   'date_setup',
                   'last_upgrade',
                   'last_setup',
                   'user',
                   'data_type',
                   'reachable',
                   'place',
                   'last_status_store',
                   'type']


def authenticate():
    try:
        payload = {'grant_type': 'password',
                   'username': os.environ.get('USERNAME'),
                   'password': os.environ.get('PASSWORD'),
                   'client_id': os.environ.get('CLIENT_ID'),
                   'client_secret': os.environ.get('CLIENT_SECRET'),
                   'scope': 'read_station'
                   }
        response = requests.post(
            'https://api.netatmo.com/oauth2/token', data=payload)
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token
    except requests.exceptions.HTTPError as error:
        app.logger.error('POST https://api.netatmo.com/oauth2/token: ' + json.dumps(payload))
        app.logger.error(error.response.status_code, error.response.text)
    except:
        app.logger.error('POST https://api.netatmo.com/oauth2/token: ' + json.dumps(payload))
        app.logger.error('Unexpected error:', sys.exc_info()[0])
    return None


def redact_sensitive_data(obj):
    # Remove fields
    for field in REDACTED_FIELDS:
        obj.pop(field, None)
    # For the remainder of the items
    for item in obj.items():
        # If the item is an object
        if isinstance(item[1], dict):
            # Descend
            obj[item[0]] = redact_sensitive_data(item[1])
        # If the item is a list
        if isinstance(item[1], list):
            # Iterate over all list items
            for listidx, listitem in enumerate(item[1]):
                if isinstance(listitem, dict):
                    obj[item[0]][listidx] = redact_sensitive_data(listitem)
    return obj


def get_stations_data():
    params = {
        'access_token': authenticate(),
        'device_id': os.environ.get('DEVICE_ID')
    }
    try:
        response = requests.post(
            'https://api.netatmo.com/api/getstationsdata', params=params)
        response.raise_for_status()
        devices = response.json()['body']
        return redact_sensitive_data(devices)
    except requests.exceptions.HTTPError as error:
        app.logger.error('POST https://api.netatmo.com/api/getstationsdata: ' + json.dumps(params))
        app.logger.error(error.response.status_code, error.response.text)
    except:
        app.logger.error('POST https://api.netatmo.com/api/getstationsdata: ' + json.dumps(params))
        app.logger.error('Unexpected error:', sys.exc_info()[0])
    return None

@app.route('/')
def main():
    return flask.jsonify(get_stations_data())
