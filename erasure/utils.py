import json
import requests
from os import path


def get_abi(contract):
    abi_file_path = f"{path.dirname(__file__)}/abi/"
    with open(f'{abi_file_path}/{contract}.json') as json_file:
        return json.load(json_file)


def initialize_contract(w3, contract_address, contract_name):
    return w3.eth.contract(
        address=contract_address,
        abi=get_abi(contract_name)
    )


def get_gas_price(mode='average'):
    url = "https://ethgasstation.info/json/ethgasAPI.json"
    result = requests.get(url)
    return result.json()[mode]/10
