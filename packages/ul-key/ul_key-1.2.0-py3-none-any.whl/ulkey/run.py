from ulkey.core import ULKey

def encode_ul(text: str, seed: str, mode: str = "normal") -> str:
    ul = ULKey(seed, mode)
    return ul.encode(text)

def decode_ul(encoded_text: str, seed: str, mode: str = "normal") -> str:
    ul = ULKey(seed, mode)
    return ul.decode(encoded_text)

