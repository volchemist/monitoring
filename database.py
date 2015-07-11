#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as lite


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
    finally:
        if con:
            con.close()


def get_securities():
    data = None
    try:
        con = lite.connect('../data/statics.sqlite')
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM securities')
        data = cur.fetchall()
    finally:
        if con:
            con.close()
    return data


def get_subscriptions():
    data = None
    try:
        con = lite.connect('../data/statics.sqlite')
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM subscriptions WHERE symbol NOT IN (SELECT symbol FROM securities WHERE expiry < datetime())')
        data = cur.fetchall()
    finally:
        if con:
            con.close()
    return data

