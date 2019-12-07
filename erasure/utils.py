import json
from os import path


def get_abi(contract):
    abi_file_path = f"{path.dirname(__file__)}/abi/"
    with open(f'{abi_file_path}/{contract}.json') as json_file:
        return json.load(json_file)


def initialize_contract(w3, version, contract_dict, contract_name):
    return w3.eth.contract(
        address=contract_dict[version][contract_name],
        abi=get_abi(contract_name)
    )