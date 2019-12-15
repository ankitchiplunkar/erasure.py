import json
from os import path, makedirs


def get_abi(contract):
    abi_file_path = f"{path.dirname(__file__)}/abi/"
    with open(f'{abi_file_path}/{contract}.json') as json_file:
        return json.load(json_file)


def initialize_contract(w3, contract_address, contract_name):
    return w3.eth.contract(
        address=contract_address,
        abi=get_abi(contract_name)
    )


def write_file(directory, file_name, data):
    if not path.exists(directory):
        makedirs(directory)
    if isinstance(data, bytes):
        with open(f"{directory}/{file_name}", 'xb') as f:
            f.write(data)
    else:
        with open(f"{directory}/{file_name}", 'x') as f:
            f.write(data)


def get_file_contents(file_path):
    with open(file_path, 'r') as f:
        return f.read()
