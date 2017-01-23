import argparse
import calendar
import json
import os
from datetime import datetime

import get_birthdays
import add_appointments

CONFIG_FILE = 'config.json'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("month", nargs='?', help="Month number to request", type=int)
    return parser.parse_args()


def main():
    args = get_args()
    if not args.month:
        month = 0
        suggested = datetime.now().month
        while month < 1 or month > 12:
            try:
                month = int(input("Which month should be run? [{}]:".format(suggested)))
            except ValueError:
                pass
        args.month = month
    month_name = calendar.month_name[args.month]
    print("Gathering Birthdays for {}".format(month_name))

    with open(os.path.join(os.path.dirname(__file__), CONFIG_FILE)) as f:
        config = json.load(f)

    last = None
    diff = 5
    start_hour = 17
    start_min = 0

    for b in get_birthdays.birthday_iter(args.month):
        dt = b['birthdate']
        if last and last['month'] == dt['month'] and last['day'] == dt['day']:
            last['minutes'] += diff
            if last['minutes'] > 60:
                last['hour'] += 1
                last['minutes'] -= 60
        else:
            last = dict(dt)
            last['hour'] = start_hour
            last['minutes'] = start_min

        appointment = {
            "title": "{} ({})".format(b['name'], b['age']),
            "event_start": datetime(2017, last['month'], last['day'], last['hour'], last['minutes']),
            "description": "{name}\n{address}\nphone: {phone}\nemail: {email}".format(**b),
            "calendarId": config['google']['calendar_id']
        }
        add_appointments.add_event(**appointment)


if __name__ == '__main__':
    main()
