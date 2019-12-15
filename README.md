# erasure.py
Python client for the erasure protocol

## Setup:
1. Create & activate virtulenv (python 3.6+)
2. Install the library using pypi
    ```
    pip install erasure
    ```

## Usage:
0. Update the [settings](https://github.com/ankitchiplunkar/erasure.py/blob/master/erasure/settings.py) by providing necessary enviornment variables.
1. [Initialize](https://github.com/ankitchiplunkar/erasure.py/blob/master/tests/common.py) a client:
    ```
    erasure_client = ErasureClient(w3, mode, version)
    ```
2. [Create](https://github.com/ankitchiplunkar/erasure.py/blob/master/tests/common.py) a feed:
    ```
    feed = Feed(erasure_client=erasure_client, feed_address=FEED_ADDRESS)
    ```
3. [Submit](https://github.com/ankitchiplunkar/erasure.py/blob/master/tests/test_feed.py) a post:
    ```
    receipt = feed.create_post(raw_data, key=key)
    ```
    **Note**: The encryption keys, and data for this post will be saved in `ERASURE_KEY_STORE/<proof_hash>`
4. [Reveal](https://github.com/ankitchiplunkar/erasure.py/blob/master/tests/test_post.py) a post:
    ```
    key_cid, data_cid = post.reveal()
    ```

## Development:
1. Clone & enter the repo:
    ```
    git clone https://github.com/ankitchiplunkar/erasure.py.git
    ```
2. Install required libraries:
    ```
    pip install -r requirements.txt
    ```
3. Install erasure.py:
    ```
    pip install -e .
    ```

## Testing:
1. Launch a local version of erasure protocol via [ganache](https://github.com/erasureprotocol/erasure-protocol/tree/master/packages/testenv#deploy-contracts-to-local-ganache-server)
2. Install, initlalize and run the ipfs daemon locally `ipfs daemon`
3. Run the tests locally `pytest -vv tests/`
