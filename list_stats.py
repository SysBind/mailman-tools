#!/usr/local/bin python
from mailmanclient import Client
import os
import sys
import argparse
try:
    import json
except ImportError:
    import simplejson as json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Manipulate member settings")

    CORE_URI = os.environ.get('MAILMAN_CORE_URI',
                              'http://mailman-core:8001/3.1')
    CORE_USER = os.environ.get('MAILMAN_REST_USER', 'restadmin')
    CORE_PASS = os.environ.get('MAILMAN_REST_PASSWORD', 'restpass')

    parser.add_argument('--list-fqdn', dest='list_fqdn', action='append',
                        default=None)
    parser.add_argument('--core-uri', dest='core_uri',
                        default=CORE_URI)
    parser.add_argument('--rest-user', dest='core_user',
                        default=CORE_USER)
    parser.add_argument('--rest-password', dest='core_password',
                        default=CORE_PASS)
    args = parser.parse_args()

    # client = Client(CORE_URI, CORE_USER, CORE_PASS)
    client = Client(args.core_uri, args.core_user, args.core_password)

    results = {}
    for ml in client.get_lists():
        list_name = ml.settings['list_name']
        if args.list_fqdn:
            if not (list_name in args.list_fqdn):
                # if list name doesn't match required
                # skip along
                continue
        messages_held = len(ml.held)
        members = len(ml.members)
        subscription_requests = len(ml.requests)
        list_fqdn_name = ml.settings['fqdn_listname']
        last_post = ml.settings['last_post_at']
        last_digest = ml.settings['digest_last_sent_at']

        results[list_name] = {
            'list_fqdn_name': list_fqdn_name,
            'members': members,
            'messages_held': messages_held,
            'subscription_requests': subscription_requests,
            'last_post': last_post,
            'last_digest': last_digest
        }

    print json.dumps(results, indent=2)
