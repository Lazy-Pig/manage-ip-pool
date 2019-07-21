import json
ORIGINAL_IPS_PATH = 'data/total_ips.json'


def generate_pool():
    results = {}
    prefix = '10.10.'
    for x in range(1, 255):
        for y in range(1, 255):
            ip = prefix + str(x) + '.' + str(y)
            status = dict(is_available=True, experiment=None)
            results[ip] = status
    with open(ORIGINAL_IPS_PATH, 'w') as fp:
        json.dump(results, fp)


if __name__ == "__main__":
    generate_pool()
