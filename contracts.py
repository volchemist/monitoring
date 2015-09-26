import time
from ib.ext.Contract import Contract
from ib.ext.ContractDetails import ContractDetails
from ib.opt import ibConnection, message


# global variables
done = False
contracts = []


def watcher(msg):
    print msg


def handle_details(msg):
    contracts.append(msg.contractDetails.m_summary)


def handle_details_end(msg):
    global done
    done = True


con = ibConnection(port=4001, clientId=321)
con.registerAll(watcher)
con.register(handle_details, 'ContractDetails')
con.register(handle_details_end, 'ContractDetailsEnd')
con.connect()

contract = Contract()
contract.m_exchange = "CBOE"
contract.m_secType =  "IND"
contract.m_symbol = "VIX"
contract.m_currency = "USD"

con.reqContractDetails(1, contract)
for _ in range(20):
    if done:
        print 'all contracts received'
        break
    time.sleep(1)
if not done:
    print 'time out'
con.disconnect()
con.close()

for c in contracts:
    print c.m_symbol, c.m_secType, c.m_exchange, c.m_currency, c.m_strike, c.m_tradingClass

