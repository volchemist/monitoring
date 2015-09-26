import time
from ib.ext.Contract import Contract
from ib.ext.ContractDetails import ContractDetails
from ib.opt import ibConnection, message


# global variables
done = False
contracts = []
FIELDS = ('m_symbol', 'm_secType', 'm_exchange',
          'm_currency', 'm_strike', 'm_tradingClass',
          'm_expiry', 'm_right', 'm_conId')


def handle_details(msg):
    contracts.append(msg.contractDetails.m_summary)


def handle_details_end(msg):
    global done
    done = True


def print_contract(c):
    print tuple(getattr(c, f) for f in FIELDS)


con = ibConnection(port=4001, clientId=321)
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

print FIELDS
for c in contracts:
    print_contract(c)

