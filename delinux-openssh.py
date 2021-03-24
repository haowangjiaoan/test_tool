#!/usr/bin/env python

import getopt
import requests
import json
import sys
import hashlib


def post_json(url, data):
    resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    return resp.json()


def get_json(url, params=None):
    resp = requests.get(url, params=params)
    return resp.json()


def gen_sk(ip):
    ret = get_json("http://%s:9000/sys/DeviceInfo" % ip)
    # print(ret)
    uuid = ret['data']['Hardware']['UUID']
    return hashlib.md5(("deepglint%s" % uuid).encode(encoding='UTF-8')).hexdigest()


def main(argv):
    ip = ""
    on = 0
    help_msg = "python delinux-openssh.py -i xx.xx.xx.xx -o true"
    try:
        opts, args = getopt.getopt(argv, "hi:o:")
        print(opts, args)
    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)
    if len(opts) == 0:
        print(help_msg)
        sys.exit(1)
    for opt, arg in opts:
        if opt == "-h":
            print(help_msg)
            sys.exit(1)
        if opt == '-i':
            ip = arg
        if opt == '-o':
            if arg == "true":
                on = 1
    sk = gen_sk(ip)
    # sk = "123"
    # print(sk)
    print(post_json("http://%s:9000/sys/SSH" % ip, {'On': on, 'SecretKey': sk}))

