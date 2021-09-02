#!/usr/bin/env python3
#
# Simple digest and return netblocks from goog/cloud.json
#  https://www.gstatic.com/ipranges/goog.json
#  https://www.gstatic.com/ipranges/cloud.json

import ipaddress
import json
import urllib.request
import sys

URLS = {
        "goog": "https://www.gstatic.com/ipranges/goog.json",
        "cloud":"https://www.gstatic.com/ipranges/cloud.json",
        }

def get_file(name):
    """Download a single file, return that as a string.

    Args:
      name: a string, the URL to download.
    Returns:
      a string, which is the content downloaded, or zero length if err.
    """
    res = ""
    with urllib.request.urlopen(name) as f:
        res = f.read().decode('utf-8')

    return res

def decode_json(r):
    """Decode the json content, return a list of ipaddress.IPNetworks.

    Args:
      r: a string of json to decode.

    Returns:
      a set([]) of ipaddress.IPNetwork objects.
    """
    res4 = set([])
    res6 = set([])

    j = json.loads(r)
    for i in j['prefixes']:
        if 'ipv4Prefix' in i:
          n = i['ipv4Prefix']
          res4.add(ipaddress.ip_network(n))
        else:
          n = i['ipv6Prefix']
          res6.add(ipaddress.ip_network(n))
    
    # collapse where possible in this set.
    t = set([])
    for r in res4:
      t = set([i for i in ipaddress.collapse_addresses(list(res4))])
    res4 = t
    for r in res6:
      t = set([i for i in ipaddress.collapse_addresses(list(res6))])
    res6 = t
    res4.update(res6)
    return res4


def main(argv):
    """Slurp up the json files, do set math."""

    sets = {}
    for d in URLS:
        r = get_file(URLS[d])
        if r == "":
            print("failed to get %s" %URLS[d])

        l = decode_json(r)
        sets[d] = l

    print("Goog - Cloud")
    f = sets["goog"] - sets["cloud"]
    for p in f:
        print("%s" % p)

if __name__ == '__main__':
    main(sys.argv)
