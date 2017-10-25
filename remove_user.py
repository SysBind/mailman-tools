#!/usr/local/bin python
from mailmanclient import Client
import os
import sys

CORE_URI=os.environ.get('MAILMAN_CORE_URI','http://mailman-core:8001/3.1')
CORE_USER=os.environ.get('MAILMAN_REST_USER','restadmin')
CORE_PASS=os.environ.get('MAILMAN_REST_PASSWORD','restpass')

client=Client(CORE_URI,CORE_USER,CORE_PASS)

ml_fqdn=sys.argv[1]
member_email=sys.argv[2]

ml=client.get_list(ml_fqdn)
ml.unsubscribe(member_email)

