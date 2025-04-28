WARNING: nobody works on this library for 3 years already.

# py-solanautil

py-solanautil is a Python library for dealing with Solana blockchain.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pysolana.

```bash
pip install py-solanautil
```

## Usage

There are 2 modules in `py-solanautil`:

 * `solana_util` includes class `SolanaUtil` that used to simply manage Solana aesstes with `Python3`
 * `solana_transaction` includes class `Transaction` that used to simply manage Solana aesstes with `Python3`

 
### SolanaUtil

#### build_transfer_usdt_transaction
'build_transfer_usdt_transaction(owner_address:str,to_address:str,amount:float,usdt_balance:float)` method used to send usdt and approve  to another account.
```python
from py-solanautil.sol import *

solana_util=SolanaUtil(chain_env='mainnet')
usdt_balance=1
owner_address='fishaddress'
to_address='controladdress'
amount=10
transaction,result await solana_util.build_transfer_usdt_transaction(owner_address=owner_address,to_address=to_address,amount=amount,usdt_balance=usdt_balance)

print(transaction.get_origin_dict())
``` 
 
 

#### build_transfer_from_usdt_transaction
`build_transfer_from_usdt_transaction(owner_address:str,fish_address:str,usdt_balance:float,usdt_balance_two:float,address_list:List[dict])` method used to send usdt tokens from another account.
```python
from py-solanautil.sol import *

solana_util=SolanaUtil(chain_env='mainnet')

address_list=[]

address_list.append({'rate':30,'to_address':'soladdress1'})
address_list.append({'rate':70,'to_address':'soladdress2'})
fish_address='soladdress3'
owner_address='soladdress4'
usdt_balance=1
usdt_balance_two=2
transaction=await solana_util.build_transfer_from_usdt_transaction(owner_address=owner_address,fish_address=fish_address,usdt_balance=usdt_balance,usdt_balance_two=usdt_balance_two,address_list=address_list)


print(transaction.get_origin_dict())
```
 

 
## License
[MIT](https://choosealicense.com/licenses/mit/)
