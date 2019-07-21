import argparse
import config
import requests


class Client(object):
    def __init__(self, url):
        self._url = url

    def get_experiments_list(self):
        response = requests.get(self._url + 'experiments_list')
        if response.status_code != 200:
            print("Failure")
        else:
            resp = response.json()
            print(resp['message'])

    def create_experiment(self, experiment_id, ip_num):
        response = requests.get(self._url + 'experiments/create/%s/%d' % (experiment_id, ip_num))
        if response.status_code != 200:
            print("Failure")
        else:
            resp = response.json()
            print(resp['message'])

    def release_experiment(self, experiment_id):
        response = requests.get(self._url + 'experiments/release/%s' % experiment_id)
        if response.status_code != 200:
            print("Failure")
        else:
            resp = response.json()
            print(resp['message'])

    def get_ip_list(self, experiment_id):
        response = requests.get(self._url + 'experiments/%s/ips' % experiment_id)
        if response.status_code != 200:
            print("Failure")
        else:
            resp = response.json()
            print(resp['message'])

    def get_available_num(self):
        response = requests.get(self._url + 'available_ip_num')
        if response.status_code != 200:
            print("Failure")
        else:
            resp = response.json()
            print(resp['message'])


def main():
    client = Client(url=config.base_url)
    if args.list_experiment:
        client.get_experiments_list()

    if args.release_experiment is not None:
        client.release_experiment(args.release_experiment)

    if args.create_experiment is not None:
        client.create_experiment(args.create_experiment, args.n)

    if args.ip_list is not None:
        client.get_ip_list(args.ip_list)

    if args.available_num:
        client.get_available_num()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list_experiment", help="list all experiments", action='store_true')
    parser.add_argument("-r", "--release_experiment", help="release an experiment", type=str)
    parser.add_argument("-c", "--create_experiment", help="create an experiment", type=str)
    parser.add_argument("-n", help="create an experiment with `n` ips", type=int)
    parser.add_argument("--ip_list", help="get ip list of the experiment", type=str)
    parser.add_argument("--available_num", help="get the number of available ips", action='store_true')
    args = parser.parse_args()
    if args.create_experiment is not None and args.n is None:
        parser.error("If you want to create an experiment, we need both `-c` and `-n` commands")
    main()
