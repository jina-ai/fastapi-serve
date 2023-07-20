import sys
import time

import requests


def check_service(url):
    try:
        r = requests.get(url, timeout=2)  # added a timeout
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.RequestException as e:
        print(e)
    return None


def measure_downtime(url, sleep_interval=1):
    downtime_start = None
    total_downtime = 0
    old_version = None
    while True:
        response = check_service(url)
        if response is None:
            print('Downtime')
            if downtime_start is None:
                downtime_start = time.time()
        else:
            if downtime_start is not None:
                downtime_end = time.time()
                total_downtime += downtime_end - downtime_start
                print(
                    f'Downtime ended. Total downtime so far: {total_downtime} seconds.'
                )
                downtime_start = None

            if old_version is None:
                old_version = response['version']
            elif old_version != response['version']:
                print(f'Version updated from {old_version} to {response["version"]}')
                old_version = response['version']
            else:
                print(
                    f'Service status: {response["status"]}, Version: {response["version"]}, Revision: {response["revision"]}'
                )
        time.sleep(sleep_interval)


endpoint = sys.argv[1]
measure_downtime(f'{endpoint}/health')
