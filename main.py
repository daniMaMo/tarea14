# ! ./venv/bin/python3.8
# -*- coding: utf-8 -*-
"""
Download world happiness time series from hedonometer project.
See https://hedonometer.org/timeseries/en_all/?from=2020-08-24&to=2022-02-23
Created on Tue Feb 24 15:35:23 2022

@author: Feliú Sagols
CDMX
"""

import re
import matplotlib.pyplot as plt
import requests
# import psycopg2
import datetime
# import pandas as pd
import loggers
import csv

TIMESERIES_DATABASE = "ts_db"

global LOGGER


# def last_available_date():
#     """
#     Returns the newest record base_date in happiness table
#     """
#     conn = psycopg2.connect("dbname=%s user=fsagols host=localhost" %
#                             TIMESERIES_DATABASE)
#     cur = conn.cursor()
#     cur.execute("""
#         select date_
#         from happiness
#         order by date_ desc
#         limit 1;
#         """)
#     date_ = cur.fetchone()[0]
#     conn.close()
#     return date_


# def get_happiness_ts(last_date, last_days):
#     """
#     Returns the happiness time series.
#
#     Parameters
#     ----------
#     last_date : datetime.pyi
#         Last base_date in the time period to download.
#     last_days:
#         Number of days previous to the last base_date to download.
#
#     Examples
#     --------
#     >>> get_happiness_ts(datetime.datetime(2022, 2, 26), 700)
#
#     Returns
#     -------
#         A dataframe with the time series.
#     """
#     conn = psycopg2.connect("dbname=%s user=fsagols host=localhost" %
#                             TIMESERIES_DATABASE)
#     cur = conn.cursor()
#     cur.execute(
#         """
#         select date_, happiness
#         from happiness
#         where date_ <= %(last_date)s
#         order by date_ desc limit %(last_days)s;
#         """, {
#             'last_date': last_date,
#             'last_days': last_days
#         })
#     answer = cur.fetchall()
#     answer.reverse()
#     answer = [[a[0], a[1]] for a in answer]
#     df = pd.DataFrame(data=answer, columns=['base_date', 'happiness'])
#     df.set_index('base_date', inplace=True)
#     return df


def download_happiness(start_date, records):
    """
    Download happiness records from the url below. Happiness records are stored
    into happiness database table.

    Parameters
    ----------
    start_date : datetime.pyi
        Initial downloading base_date.
    records : int
        Maximum number of records after start_date to download.
    """
    LOGGER.debug("Downloading happiness time series.")
    data_json = requests.get(
        'https://hedonometer.org/api/v1/happiness/?format=json&timeseries__'
        f'title=en_all&date__gte='
        f'{start_date.strftime("%Y-%m-%d")}&limit={records}')
    data = data_json.json()
    data = [[
        datetime.datetime.strptime(d['date'], "%Y-%m-%d"), d['frequency'],
        float(d['happiness'])
    ] for d in data['objects']]
    # conn = psycopg2.connect("dbname=%s user=fsagols host=localhost" %
    #                         TIMESERIES_DATABASE)
    LOGGER.info("Storing happiness time series.")
    # cur = conn.cursor()
    # cur.executemany(
    #     """
    #     insert into happiness
    #     values (%s, %s, %s)
    #     on conflict (date_)
    #     do nothing;
    #     """, data)
    # conn.commit()
    # conn.close()
    # print('\n'.join(str(d) for d in data))
    # print('\n'.join(str(d[0]) for d in data))
    # print('\n'.join(str(d[1]) for d in data))
    # print('\n'.join(str(d[2]) for d in data))
    # print(data)
    return data

if __name__ == "__main__":
    LOGGER = loggers.define_logger("happiness.log")
    date = datetime.datetime(2022, 1, 1)
    DATA = download_happiness(date, 5000)


# with open('happiness.csv', mode='w') as csv_file:
#    fieldnames = ['date', 'frequency', 'rate']
#    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#
#    writer.writeheader()
#    for d in DATA:
#        writer.writerow({'date': str(d[0]), 'frequency': str(d[1]), 'rate': str(d[2])})


# def retrieve_happiness(*lists):
#    """
#    This function return dates between dates interested, also we can specify the step of this list
#    :param lists: list of that contains in the two dates and an optional integer
#    :return: A list of lists, where each one list dates between dates entered
#
#    Example:
#    >>> retrieve_happiness(['2022-01-01', '2022-05-24', 3], ['2022-01-15', '2022-01-20'])
#    """

#    dates_of_all_list = []
#    for l in lists:
#        l[0] = datetime.datetime.strptime(l[0], "%Y-%m-%d")
#        l[1] = datetime.datetime.strptime(l[1], "%Y-%m-%d")
#        interval_dates = [str(date) for date in DATA_DATES if l[0] <= date <= l[1]]
#
#        if len(l) > 2:
#            x = slice(0, len(interval_dates), l[2])
#        else:
#            x = slice(0, len(interval_dates))
#
#        dates = interval_dates[x]
#        dates_of_all_list.append(dates)
#    return dates_of_all_list

DATE = download_happiness(datetime.datetime(2022, 1, 1), 500)
DATES = [str(d[0]) for d in DATE]
DATES_FORMAT = [re.match('\d{4}-\d{2}-\d{2}', d).group(0) for d in DATES]
RATES = [str(d[2]) for d in DATE]
print(DATES_FORMAT)
print(RATES)
x = DATES_FORMAT
y = RATES

plt.plot(x,y,marker="o")
plt.xticks(rotation=10)
plt.title('world happiness time series', fontweight ="bold")
plt.show()

