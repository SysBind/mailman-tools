#!/bin/env python
import sys
try:
    import json
except ImportError:
    import simplejson as json

data = json.load(sys.stdin)

#  "security": {
#    "owners": 2,
#    "messages_held": 3,
#    "members": 11,
#    "list_fqdn_name": "security@lists.med.stanford.edu",
#    "last_digest": "2010-10-27T23:04:25.346716",
#    "nonmembers": 134,
#    "subscription_requests": 0,
#    "last_post": "2010-10-27T23:04:29.843071",
#    "moderators": 4
#  }

# echo "1 Mailu_queue_len queue=$queued;300;500 WARNING - Can't fetch queue length"
for list_name in data.keys():
    print("0 Mailman_{list_name}_stats members={members}|owners={owners}|messages_held{messages_held}|nonmembers={nonmembers}|subscription_requests={subscription_requests}|moderators={moderators}\n".format(
        list_name=list_name, **data[list_name]))
