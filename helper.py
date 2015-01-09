from uuid import uuid4
from time import time


records_per_page = 2


def get_exp_time_for_code():
    return int(time()+2 * 60)


def get_exp_time_for_access_token():
    return int(time()+10 * 60)


def generate_random_code():
    res = ""
    return res.join(str(uuid4()).split('-'))


if __name__ == "__main__":
    print(generate_random_code())