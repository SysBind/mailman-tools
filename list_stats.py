#!/usr/local/bin python
from mailmanclient import Client
import os
# import sys
import urllib2
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

    # parser.add_argument('--members', action='store_true', default=False)
    # parser.add_argument('--owners', action='store_true', default=False)
    # parser.add_argument('--nonmembers', action='store_true', default=False)
    # parser.add_argument('--moderators', action='store_true', default=False)
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
        list_fqdn_name = ml.settings['fqdn_listname']
        if args.list_fqdn:
            if not (list_fqdn_name in args.list_fqdn):
                # if list name doesn't match required
                # skip along
                continue
        try:
            messages_held = len(ml.held)
        except:
            messages_held = -1
        try:
            members = ml.rest_data['member_count']
        except:
            members = -1
        try:
            moderators = len(ml.moderators)
        except:
            moderators = -1
        try:
            owners = len(ml.owners)
        except:
            owners = -1
        try:
            nonmembers = len(ml.nonmembers)
        except:
            nonmembers = -1
        try:
            subscription_requests = len(ml.requests)
        except:
            subscription_requests = -1
        last_post = ml.settings['last_post_at']
        last_digest = ml.settings['digest_last_sent_at']

        results[list_name] = {
            'list_fqdn_name': list_fqdn_name,
            'members': members,
            'owners': owners,
            'moderators': moderators,
            'nonmembers': nonmembers,
            'messages_held': messages_held,
            'subscription_requests': subscription_requests,
            'last_post': last_post,
            'last_digest': last_digest
        }

    print json.dumps(results, indent=2)
