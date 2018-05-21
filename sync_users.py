#!/bin/env python
from mailmanclient import Client
import os
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sync member list")

    CORE_URI = os.environ.get('MAILMAN_CORE_URI',
                              'http://mailman-core:8001/3.1')
    CORE_USER = os.environ.get('MAILMAN_REST_USER', 'restadmin')
    CORE_PASS = os.environ.get('MAILMAN_REST_PASSWORD', 'restpass')

    parser.add_argument('list_fqdn')
    parser.add_argument('--members-file', dest='list', default=None)
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

    current_members = [str(m.address) for m in ml.members]
    new_member_list = []
    if args.list:
        if args.list == '-':
            list_file = sys.stdin
        else:
            list_file = open(args.list, 'r')
    else:
        list_file = sys.stdin

    for l in list_file:
        member_email = l.strip()
        print("Received {}".format(member_email))
        new_member_list.append(member_email)
    if args.list and args.list != '-':
        list_file.close()

    for member_email in current_members:
        if member_email not in new_member_list:
            print("Intend to unsubscribe '{0}'".format(member_email))
            try:
                ml.unsubscribe(member_email)
            except:
                print("Can't unsubscribe '{0}'".format(member_email))

    for member_email in new_member_list:
        if member_email not in current_members:
            print("Intend to subscribe '{0}'".format(member_email))
            try:
                ml.subscribe(member_email, pre_verified=True, pre_confirmed=True,
                             pre_approved=True)
            except:
                print("Can't subscribe '{0}'".format(member_email))
