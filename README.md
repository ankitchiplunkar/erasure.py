# erasure.py
Python client for the erasure protocol

## Setup
1. Create & activate virtulenv (python 3.6+)
2. Clone & enter the repo `git clone https://github.com/ankitchiplunkar/erasure.py.git`
3. Install required libraries `pip install -r requirements.txt`
4. Install erasure.py `pip install -e .`

## Testing
1. Launch a local version of erasure protocol via ganache
    - https://github.com/erasureprotocol/erasure-protocol/tree/master/packages/testenv#deploy-contracts-to-local-ganache-server
2. Run the tests locally `pytest -vv tests/`
