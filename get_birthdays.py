import json
import os

import requests

URL = 'https://www.lds.org/mls/mbr/services/report/birthday-list/unit/9296?lang=eng&month={}&months={}'
CONFIG_FILE = 'config.json'


def get_birthdays(month):
    with open(os.path.join(os.path.dirname(__file__), CONFIG_FILE)) as f:
        config = json.load(f)
    s = requests.Session()
    s.get(URL.format(month, 1))
    r = s.post('https://ident.lds.org/sso/UI/Login', {
        'IDToken1': config['lds']['username'],
        'IDToken2': config['lds']['password']
    })
    try:
        results = r.json()
    except ValueError as e:
        s.get('https://www.lds.org/mls/mbr/?nb=true&lang=eng')
        results = s.get(URL.format(month, 1)).json()
    finally:
        return results[0]['birthdays']


def get_data(birthdays):
    for person in birthdays:
        yield {
            'name': person['name'],
            'email': person['email'],
            'age': int(person['age']) + 1,
            'address': person['address'].replace("<br />", "\n"),
            'birthdate': {
                'year': int(person['birthDate'][:4]),
                'month': int(person['birthDate'][4:6]),
                'day': int(person['birthDate'][6:8])
            },
            'phone': person['phone']
        }


def birthday_iter(month):
    birthdays = get_birthdays(month)
    for b in get_data(birthdays):
        yield b


def main():
    birthdays = get_birthdays(1)
    for b in get_data(birthdays):
        print(b)


if __name__ == '__main__':
    main()
