# erasure.py
Python client for the erasure protocol

![Tests](https://travis-ci.com/ankitchiplunkar/erasure.py.svg?branch=master)

Erasure Protocol version: `1.2.0`


## Setup:
1. Create & activate virtulenv (python 3.6+)
2. Install the library using pypi. `pip install erasure`

## Usage:
The client is built to replicate the usage [here](https://github.com/erasureprotocol/erasure-protocol#example-usage-of-erasureclient).

1. Update the [settings](https://github.com/ankitchiplunkar/erasure.py/blob/master/erasure/settings.py) by configuring the appropriate enviornment variables.
2. [Initialize](https://github.com/ankitchiplunkar/erasure.py/blob/master/tests/common.py) a client:
    ```
    erasure_client = ErasureClient(w3, mode, version)
    ```
3. [Create](https://github.com/ankitchiplunkar/erasure.py/blob/master/tests/common.py) a feed:
    ```
    feed = Feed(erasure_client=erasure_client, feed_address=FEED_ADDRESS)
    ```
4. [Submit](https://github.com/ankitchiplunkar/erasure.py/blob/master/tests/test_feed.py) a post:
    ```
    receipt = feed.create_post(raw_data, key=key)
    ```
    **Note**: The encryption keys, and data for this post will be saved in `ERASURE_KEY_STORE/<proof_hash>`
5. [Reveal](https://github.com/ankitchiplunkar/erasure.py/blob/master/tests/test_post.py) a post:
    ```
    key_cid, data_cid = post.reveal()
    ```

## Development:
1. Clone & enter the repo. `git clone https://github.com/ankitchiplunkar/erasure.py.git`
2. Install required libraries. `pip install -r requirements.txt`

## Testing:
1. Launch a local version of erasure protocol via [ganache](https://github.com/erasureprotocol/erasure-protocol/tree/master/packages/testenv#deploy-contracts-to-local-ganache-server)
2. Install, initlalize and run the ipfs daemon locally `ipfs daemon`
3. Run the tests locally `pytest -vv tests/`
