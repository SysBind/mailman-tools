#!/bin/env python
from mailmanclient import Client
import os
import sys
import argparse
import time
import datetime

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
    new_member_names = {}
    if args.list:
        if args.list == '-':
            list_file = sys.stdin
        else:
            list_file = open(args.list, 'r')
    else:
        list_file = sys.stdin

    for l in list_file:
        member_email = l.split('<')[1].split('>')[0].strip()
        member_name =  l.split('<')[0].strip()
        new_member_list.append(member_email)
        new_member_names[member_email] = member_name
    if args.list and args.list != '-':
        list_file.close()

    for member_email in current_members:
        if member_email not in new_member_list:
            try:
                ml.unsubscribe(member_email)
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                print("["+st+"] Removed %s" % (member_email))
            except:
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                print("["+st+"] Exception %s" % (member_email))

    for member_email in new_member_list:
        if member_email not in current_members:
            try: 
                try:
                    user = client.get_user(member_email)
                except:
                    member_name = new_member_names[member_email]
                    user = client.create_user(email=member_email, display_name=member_name, password=None)		

                ml.subscribe(member_email, display_name=member_name, pre_verified=True, pre_confirmed=True, pre_approved=True)
                current_members.append(member_email)
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                print("["+st+"] Added %s" % (member_email))
            except:
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                print("["+st+"] Invalid %s" % (member_email))
