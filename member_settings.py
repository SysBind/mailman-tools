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

    parser.add_argument('--list-fqdn', dest='list_fqdn',
                        required=True)
    parser.add_argument('--members', dest='members',
                        action='append', default=None)
    parser.add_argument('--members-file', dest='list', default=None)
    parser.add_argument('--core-uri', dest='core_uri',
                        default=CORE_URI)
    parser.add_argument('--rest-user', dest='core_user',
                        default=CORE_USER)
    parser.add_argument('--rest-password', dest='core_password',
                        default=CORE_PASS)
    args = parser.parse_args()

    # client = Client(CORE_URI, CORE_USER, CORE_PASS)
    client = Client(args.core_uri, args.core_user, args.core_password)

    ml_fqdn = args.list_fqdn
    member_list = args.members
    member_file = None
    if args.list:
        if args.list == '-':
            member_file = sys.stdin
        else:
            member_file = open(args.list, 'r')

        for m in member_file:
            member_list.append(m.strip())
        if args.list and args.list != '-':
            member_file.close()

    results = {}
    ml = client.get_list(ml_fqdn)
    for member_email in member_list:
        member = ml.get_member(member_email)
        results[member_email] = member.settings

    print json.dumps(results, indent=2)
