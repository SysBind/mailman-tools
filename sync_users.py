#!/usr/local/bin/python
from mailmanclient import Client
import os
import sys

CORE_URI = os.environ.get('MAILMAN_CORE_URI', 'http://mailman-core:8001/3.1')
CORE_USER = os.environ.get('MAILMAN_REST_USER', 'restadmin')
CORE_PASS = os.environ.get('MAILMAN_REST_PASSWORD', 'restpass')

client = Client(CORE_URI, CORE_USER, CORE_PASS)

ml_fqdn = sys.argv[1]
ml = client.get_list(ml_fqdn)

current_members = [m.address for m in ml.members]
new_member_list = []

for l in sys.stdin:
    member_email = l.strip()
    print("Received {}".format(member_email))
    new_member_list.append(member_email)

for member_email in current_members:
    if member_email not in new_member_list:
        print("Intend to unsubscribe {}".format(member_email))
        ml.unsubscribe(member_email)

for member_email in new_member_list:
    if member_email not in current_members:
        print("Intend to subscribe {}".format(member_email))
        ml.subscribe(member_email, pre_verified=True, pre_confirmed=True, 
                     pre_approved=True)
