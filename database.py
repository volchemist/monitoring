#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import pandas as pd


cache = []
cache_size = 200


def save_tick_data(tstamp, symbol, field, value):
    observation = (tstamp, symbol, field, value)
    cache.append(observation)
    if len(cache) >= cache_size:
        flush_cache()


def flush_cache():
    try:
        con = lite.connect('../data/prices.sqlite')
        cur = con.cursor()
        cur.executemany("INSERT INTO intraday VALUES(?, ?, ?, ?)", cache)
        con.commit()
        del cache[:]
    except lite.OperationalError:
        print 'database locked. will retry to flush cache later.'
    finally:
        if con:
            con.close()

            
def _convert_time(time):
    try:
        return unicode(time.strftime('%Y-%m-%d'))
    except:
        return u''
            

def get_securities():
    """
    Returns a list of security definitions (each as a tuple of 
    unicode values)
    """
    #df = pd.read_excel('statics.xls', 'securities')
    #df['expiry'] = df['expiry'].map(_convert_time)
    df = pd.read_csv('securities.csv', sep=';', dtype=unicode)
    df = df.fillna(u'')
    return df.to_dict('records')


def get_subscriptions():
    """
    Returns a list of subscription definitions (each as a tuple of 
    unicode values)
    """
    #df = pd.read_excel('statics.xls', 'subscriptions')
    df = pd.read_csv('subscriptions.csv', sep=';', dtype=unicode)
    df = df.fillna(u'')
    return df.to_dict('records')
