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
    global DataWait
    done =  True


con = ibConnection(PORT=4001)
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
for _ in range(90):
    if done:
        break
    time.sleep(1)

con.disconnect()
con.close()

print contracts
