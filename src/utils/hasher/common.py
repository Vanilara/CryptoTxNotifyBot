import base64
from eth_utils.hexadecimal import decode_hex


class Hasher:
    @staticmethod
    def hash_to_base_64(text: str) -> str:
        encoded_text = base64.b64encode(text.encode('utf-8'))
        return encoded_text.decode('utf-8')
    
class EvmHasher:
    @staticmethod
    def decode_int(data) -> float:
        decoded_number = int.from_bytes(decode_hex(data), "big")
        return decoded_number