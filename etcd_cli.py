#!/usr/bin/python

import requests, json, argparse

ETCD_HOST='172.17.42.1'
ETCD_PROTO='http://'
ETCD_PORT=4001
ETCD_BASE_KEY_URI='/v2/keys'

POST_TYPES = {
    'get': 'get',
    'put': 'put',
    'append': 'append'
}

def base_url():
    return '{}{}:{}{}'.format(ETCD_PROTO, ETCD_HOST, ETCD_PORT, ETCD_BASE_KEY_URI)

def get(args):
    if 'key' not in args:
        raise Exception('A key is required')
    
    r = requests.get('{}/{}'.format(base_url(), args.key))
    if r.status_code == 404:
        return None
 
    return r.json()['node']['value']

def put(args):
    if args.key is None or args.value is None:
        raise Exception('Key and value required')

    r = requests.put('{}/{}'.format(base_url(), args.key), data={'value':args.value})
    return r.json()['node']['value']

def append(args):
    if args.key is None or args.value is None:
        raise Exception('Key and value required')

    current_value = get(args)
    if current_value is None:
        return put(args)

    r = requests.put('{}/{}?prevValue={}'.format(base_url(), args.key, current_value), data={'value':'{},{}'.format(current_value, args.value)})
    return r.json()
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Etcd helper')
    parser.add_argument('type', type=str, choices=['get', 'put', 'append'], help='Get or set a value')
    parser.add_argument('key', type=str, help='Key to get or set')
    parser.add_argument('--value', type=str, dest='value', help='Value to use when setting a key')
    args = parser.parse_args()
    print locals()[POST_TYPES[args.type]](args) 
