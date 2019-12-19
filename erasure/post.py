import logging
from erasure.utils import get_file_contents
from erasure.ipfs import upload_bytes_to_ipfs
from erasure.crypto import Symmetric

logger = logging.getLogger(__name__)


class Post():
    """
    Post class to facilitate handling of a post
    """

    def __init__(self, feed, proof_hash_in_hex):
        self.proof_hash_in_hex = proof_hash_in_hex
        self._key_store = feed.erasure_client.get_key_store()

    def _fetch_post_secrets(self):
        directory = f"{self._key_store}/{self.proof_hash_in_hex}"
        self.key = get_file_contents(f"{directory}/key").encode('utf-8')
        self.encrypted_data = get_file_contents(
            f"{directory}/edata").encode('utf-8')
        self.cid = get_file_contents(f"{directory}/cid")

    def reveal(self):
        self._fetch_post_secrets()
        data = Symmetric.decrypt(self.key, self.encrypted_data)
        logger.info(f'Uploading key.')
        key_cid = upload_bytes_to_ipfs(self.key)
        logger.info(f'Uploading data.')
        data_cid = upload_bytes_to_ipfs(data)
        return key_cid, data_cid
