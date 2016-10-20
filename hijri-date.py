#!/usr/bin/env python3

import os, time, datetime as dt
import urllib.request
import lxml.html

DATE_FILE = "/tmp/hijri_date.txt"

def fetch_hijri_date():
    """fetch the hijri date online"""
    days = {'1': "السبت",
            '2': "الأحد",
            '3': "الإثنين",
            '4': "الثلاثاء",
            '5': "الأربعاء",
            '6': "الخميس",
            '7': "الجمعة"}

    with urllib.request.urlopen('http://www.ummulqura.org.sa/') as response:
        html = response.read()
        html = html.decode('utf-8')
        page = lxml.html.fromstring(html)
        day_name = page.xpath('//*[@id="ContentPlaceHolder1_homepage1_daytable"]')[0].get('background')
        day_name = days[day_name.split('/')[1][0]]
        day_number = page.xpath('//*[@id="ContentPlaceHolder1_homepage1_lblHDay"]')[0].text
        month_name = page.xpath('//*[@id="ContentPlaceHolder1_homepage1_lblHMonthA"]')[0].text
        month_number = page.xpath('//*[@id="ContentPlaceHolder1_homepage1_lblHMonthNumber"]')[0].text
        year = page.xpath('//*[@id="ContentPlaceHolder1_homepage1_lblHYear"]')[0].text
    date = "{} {} {} ({}) {} هـ".format(day_name, day_number, month_name, month_number, year)
    return date

def should_update_p(f):
    """a predicate that becomes True when the file is older than one day"""
    aday = dt.timedelta(hours=24)
    fmtime = os.path.getmtime(f)
    fmtime = dt.datetime.fromtimestamp(fmtime)
    if (dt.datetime.now() - fmtime) > aday:
        return True
    else:
        return False

def set_file_mtime(f):
    """sets the file access and mondification time to the beginning of the current day"""
    n = dt.datetime.now()
    this_day = dt.datetime(year=n.year, month=n.month, day=n.day)
    os.utime(f, times=(this_day.timestamp(), this_day.timestamp()))

def create_date_file(txt):
    """used to create or update the date file"""
    f = open(DATE_FILE, 'w')
    f.write(txt)
    f.close()
    set_file_mtime(f.name)

def read_date_file():
    f = open(DATE_FILE, 'r')
    text = f.readline()
    f.close()
    return text

def hijri_date():
    try:
        if should_update_p(DATE_FILE):
            date = fetch_hijri_date()
            create_date_file(date)
            return date
        else:
            date = read_date_file()
            return date

    except FileNotFoundError:
        date = fetch_hijri_date()
        create_date_file(date)
        return date


now = dt.datetime.now()
e = os.environ['BLOCK_BUTTON']

if e == '1':
    print(hijri_date())
else:
    print(now.strftime("%Y-%m-%d %I:%M %p"))
