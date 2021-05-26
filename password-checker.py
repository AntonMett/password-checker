import requests
import hashlib
import sys


with open('password.txt', 'r',) as text:
    content = text.read()


def request_api_data(query_char):
    url = f'https://api.pwnedpasswords.com/range/{query_char}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check api.')
    return res


def get_password_leak_count(hashes, hash_to_check):
    hashes = (line.split(':')for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, remaining_char = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leak_count(response, remaining_char)


def main(password):

    count = pwned_api_check(password)
    if count:
        print(
            f'PASSWORD {password} was found {count} times, You should change it!')
    else:
        print(f'PASSWORD: {password} is CLEAR!')
    return 'DONE'


if __name__ == '__main__':
    sys.exit(main(content))
