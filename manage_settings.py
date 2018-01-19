#!/bin/env python
from mailmanclient import Client
import os
import sys
import argparse
try:
    import json
except ImportError:
    import simplejson as json


def dump(ml):
    print json.dumps(dict(ml.settings), indent=2)


def set_value(ml, setting, value):
    ml.settings[setting] = value
    ml.settings.save()


def update_settings(ml, updated_settings):
    for setting in updated_settings:
        ml.settings[setting] = updated_settings[setting]
    ml.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sync member list")

    CORE_URI = os.environ.get('MAILMAN_CORE_URI',
                              'http://mailman-core:8001/3.1')
    CORE_USER = os.environ.get('MAILMAN_REST_USER', 'restadmin')
    CORE_PASS = os.environ.get('MAILMAN_REST_PASSWORD', 'restpass')

    parser.add_argument('list_fqdn')
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument('--dump', action='store_true', default=False)
    action_group.add_argument('--set', help='set single setting in a form: <setting_name>=<setting_value>')
    action_group.add_argument('--update', help='update settings with contents of the file provided')

    parser.add_argument('--core-uri', dest='core_uri',
                        default=CORE_URI)
    parser.add_argument('--rest-user', dest='core_user',
                        default=CORE_USER)
    parser.add_argument('--rest-password', dest='core_password',
                        default=CORE_PASS)
    args = parser.parse_args()

    client = Client(args.core_uri, args.core_user, args.core_password)

    ml_fqdn = args.list_fqdn

    ml = client.get_list(ml_fqdn)

    if args.dump:
        dump(ml)
    elif args.set:
        (setting, value) = args.set.split('=', 1)
        set_value(ml, setting, value)
    elif args.update:
        if args.update == '-':
            f = sys.stdin
        else:
            f = open(args.update, 'r')
        updated_settings = json.loads(f.read())
        update_settings(ml, updated_settings)
        if args.update != '-':
            f.close()
