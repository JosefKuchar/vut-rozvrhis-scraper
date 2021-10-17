#!/usr/bin/env python3
# Josef Kuchař - josefkuchar.com
# Usage: ./parser.py URL OUT_FILE
# E.g.:  ./parser.py https://minerva3.fit.vutbr.cz/rozvrhis/ZS2021/zkousky/1BIT calendar.ics

import pandas as pd
import uuid
from icalendar import Calendar, Event, vDatetime
from datetime import datetime
import requests
import argparse
import sys


def generate_calendar(table):
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '//JosefKuchar/vut-rozvrhis-parser//NONSGML v1.0//EN')

    for index, row in table.iterrows():
        name = row[0].split(',')
        for i in range(1, len(row)):
            row[i] = row[i].replace(u'\xa0', u' ')
            datetime_ranges = row[i].split(';')

            for datetime_range in datetime_ranges:
                try:
                    parts = datetime_range.split(',')
                    startend = parts[1].split(' - ')
                    start = parts[0] + ' ' + startend[0]
                    end = parts[0] + ' ' + startend[1]

                    DATE_FORMAT = "%d. %m. %Y %H:%M"

                    event = Event()
                    event.add('uid', uuid.uuid1())
                    event.add('dtstamp', vDatetime(datetime.now()))
                    event.add('dtstart', vDatetime(
                        datetime.strptime(start, DATE_FORMAT)))
                    event.add('dtend', vDatetime(
                        datetime.strptime(end, DATE_FORMAT)))
                    event.add(
                        'summary', '{} - {}'.format(name[0], table.columns.values[i]))
                    cal.add_component(event)
                except:
                    print("Can't get start and and datetime, skipping...")
    return cal


def preprocess(data):
    data = data.replace('<br>', ',')
    data = data.replace('<hr class="invisible">', ';')
    data = data.replace('<sup>', ':')
    data = data.replace('</sup>', '')

    return data


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description='VUT Rozvrhy IS parser')
    parser.add_argument('url', metavar='URL', type=str,
                        help='Url, e.g.: https://minerva3.fit.vutbr.cz/rozvrhis/ZS2021/zkousky/1BIT')
    parser.add_argument('out', metavar='OUT_FILE', type=str,
                        help='Output filename, e.g.: calendar.ics')
    args = parser.parse_args()

    # Download website as string
    try:
        text = requests.get(args.url).text
    except Exception as e:
        print('Download error!')
        print(e)
        sys.exit()

    # Preprocess for parsing
    text = preprocess(text)

    # Parse table
    try:
        tables = pd.read_html(text, encoding='utf-8')
    except Exception as e:
        print('Table parsing error!')
        print(e)
        sys.exit()

    if (len(tables) == 0):
        print('No tables found!')
        sys.exit()

    # Generate calendar
    calendar = generate_calendar(tables[0])

    # Save calendar to file
    try:
        f = open(args.out, 'wb')
        f.write(calendar.to_ical())
        f.close()
    except Exception as e:
        print('Error writing calendar to file!')
        print(e)
