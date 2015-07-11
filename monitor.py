#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep
import datetime
import database

symbol_by_tickid = {}

def print_msg(msg):
    print msg

def process_tick_data(msg):
    if msg.field in [1, 2, 4]:
        tstamp = datetime.datetime.now()
        symbol = symbol_by_tickid[msg.tickerId]
        field = { 1 : 'bid', 2 : 'ask', 4 : 'last' }[msg.field]
        value = msg.price
        database.save_tick_data(tstamp, symbol, field, value)


def create_contract(contract_tuple):
    new_contract = Contract()
    new_contract.m_symbol = str(contract_tuple['ib_symbol'])
    new_contract.m_secType = str(contract_tuple['ib_type'])
    new_contract.m_exchange = str(contract_tuple['ib_exchange'])
    new_contract.m_currency = str(contract_tuple['ib_currency'])
    new_contract.m_expiry = str(contract_tuple['ib_expiry']) if contract_tuple['ib_expiry'] else ''
    new_contract.m_strike = float(contract_tuple['ib_strike'])
    new_contract.m_right = str(contract_tuple['ib_right']) if contract_tuple['ib_right'] else ''
    contr_tup = [new_contract.m_symbol, new_contract.m_secType, new_contract.m_exchange, new_contract.m_currency, new_contract.m_expiry, new_contract.m_strike, new_contract.m_right]
    return new_contract


if __name__ == '__main__':

    # determine which securities to subscribe to
    securities = database.get_securities()
    subscription_data = database.get_subscriptions()

    try:
        # connect to IB and register message handler
        con = ibConnection(port=4001)
	print 'connection to IB established'
        con.register(process_tick_data, message.tickPrice)
	print 'event handler registered'
        con.connect()
        sleep(3)

        # request market data for each security
        tickId = 1
        for sub in subscription_data:
            new_contract = create_contract(sub)
            con.reqMktData(tickId, new_contract, '', False)
            symbol_by_tickid[tickId] = sub['symbol']
            tickId += 1
	print 'market data requested for %d symbols' % len(subscription_data)
        
        # keep thread alive while tick data is coming in
        while True:
            sleep(5)

    except KeyboardInterrupt:
        print 'Terminating due to user request'

    finally:
        # flush database cache
        database.flush_cache()
        # disconnect from IB
        con.cancelMktData(tickId)
        sleep(1)
        con.disconnect()
        sleep(1)
