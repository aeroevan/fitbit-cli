#!/usr/bin/env python3
import json
import requests
import argparse
from urllib.parse import parse_qs
from requests_oauthlib import OAuth1

from _credentials import CLIENT_KEY, CLIENT_SECRET

BASE_URL = 'http://api.fitbit.com'
REQUEST_TOKEN_URL = BASE_URL + '/oauth/request_token'
BASE_AUTHORIZATION_URL = 'http://www.fitbit.com/oauth/authorize'
ACCESS_TOKEN_URL = BASE_URL + '/oauth/access_token'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', '-k',
                        help='Resource owner key')
    parser.add_argument('--secret', '-s',
                        help='Resource owner secret')
    args = vars(parser.parse_args())

    do_stuff(args)


def do_stuff(args):
    ro_key, ro_secret = \
        get_resource_owner_stuff()

    if args['key'] and args['secret']:
        ro_key = args['key']
        ro_secret = args['secret']
    else:
        token = get_token(ro_key)
        ro_key, ro_secret = access_token(ro_key, ro_secret, token)
        print(ro_key)
        print(ro_secret)

    steps_json = get_steps(ro_key, ro_secret)
    with open('steps.json', 'w') as outfile:
        json.dump(steps_json, outfile)


def get_resource_owner_stuff():
    oauth = OAuth1(CLIENT_KEY, client_secret=CLIENT_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.text)
    resource_owner_key = credentials['oauth_token'][0]
    resource_owner_secret = credentials['oauth_token_secret'][0]
    return (resource_owner_key, resource_owner_secret)


def get_token(resource_owner_key):
    authorize_url = BASE_AUTHORIZATION_URL + '?oauth_token='
    authorize_url = authorize_url + resource_owner_key
    print('Please go here and authorize, ' + authorize_url)
    verifier = input('Please input the verifier')
    return verifier


def access_token(resource_owner_key, resource_owner_secret,
                 user_token):
    oauth = OAuth1(CLIENT_KEY, client_secret=CLIENT_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=user_token)
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.text)
    print(credentials)
    resource_owner_key = credentials['oauth_token'][0]
    resource_owner_secret = credentials['oauth_token_secret'][0]
    return (resource_owner_key, resource_owner_secret)


def get_steps(resource_owner_key, resource_owner_secret):
    oauth = OAuth1(CLIENT_KEY, client_secret=CLIENT_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret)
    r = requests.get(BASE_URL + '/1/user/-/activities/steps/date/today/1y.json', auth=oauth)
    return r.json()


if __name__ == '__main__':
    main()
