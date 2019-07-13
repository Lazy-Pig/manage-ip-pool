import json
ORIGINAL_IPS_PATH = 'data/original_ips.json'


def generate_pool():
    ips = []
    prefix = '10.10.'
    for x in range(1, 255):
        for y in range(1, 255):
            ips.append(prefix + str(x) + '.' + str(y))
    with open(ORIGINAL_IPS_PATH, 'w') as fp:
        json.dump(ips, fp)


if __name__ == "__main__":
    generate_pool()
