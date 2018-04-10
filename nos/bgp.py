"""
"Spirit of BGP" implementation.

We implement peering over a redis pub/sub queue and perodically
announce a random set of prefixes to peers. The output of each
message contains the version of the implementation. This is to
clearly show when an upgrade has occured.
"""

import os
import time

import redis


r = redis.StrictRedis(host="localhost", port=6379, db=0)
queue = r.pubsub(ignore_subscribe_messages=True)

asn = os.environ.get('BGP_ASN')
prefixes = os.environ.get('BGP_PREFIXES')
prefixes = prefixes.split(',')
peer_asns = os.environ.get('BGP_PEER_ASNS')
peer_asns = peer_asns.split(',')

for peer in peer_asns:
    queue.subscribe(peer)

VERSION = '1.0.0'

print("ASN {} starting. Running version {}. Configured peers: {}".format(asn, VERSION, ", ".join(peer_asns)))

i = 0
while True:
    message = queue.get_message()
    if message:
        message = message['data'].decode("utf-8")
        print(message)

    if i % 10 == 0:
        print("ASN {} is alive! Running version {}".format(asn, VERSION))

    if i % 30 == 0:
        print("ASN {} sending prefixes to peers. Running version {}".format(asn, VERSION))
        for peer in peer_asns:
            peer_message = "ASN {} prefixes {}. Running version {}".format(asn, ", ".join(prefixes), VERSION)
            r.publish(asn, peer_message)

    i += 1
    time.sleep(0.1)
