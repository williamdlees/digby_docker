# Ping healthchecks.io

import argparse
import requests

# Ping key for this project from healtchecks.io. Change for your project
ping_key = "BOQ1XRHK7u1aaRoofWecgA"


def main():
    parser = argparse.ArgumentParser(description='Send ping to healtchecks.io. Requires healthchecks.py to be configured and in the same directory')
    parser.add_argument('slug', help='slug name in healthchecks.io project')
    parser.add_argument('status', help='success, start, fail or log')
    parser.add_argument('-m', '--message', help='message to send with status', required=False)
    args = parser.parse_args()

    if args.status not in ['success', 'start', 'fail', 'log']:
        print('Status must be success, start, fail or log')
        exit(1)

    message = args.message if args.message else ''

    try:
        if args.status == 'success':
            r = requests.post(f"https://hc-ping.com/{ping_key}/{args.slug}", data=message, headers={'Ping-Body-Limit': '250'})
        else:
            r = requests.post(f"https://hc-ping.com/{ping_key}/{args.slug}/{args.status}", data=message, headers={'Ping-Body-Limit': '250'})
    except requests.RequestException as e:
        print("Ping failed: %s" % e)

    if r.status_code != 200:
        print(f"Ping error: status {r.status_code}: {r.text}")

if __name__ == "__main__":
    main()
