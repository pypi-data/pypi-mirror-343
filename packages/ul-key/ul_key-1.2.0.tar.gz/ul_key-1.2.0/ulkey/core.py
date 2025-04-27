import hashlib
import random
import zlib
from utils.utils import mutate_seed

class ULKey:
    def __init__(self, seed: str, mode: str = "normal"):
        self.base_seed = seed
        self.mode = mode
        self.current_seed = seed
        self.rng = self._create_rng(self.current_seed)

    def _create_rng(self, seed: str):
        hash_seed = hashlib.sha256(seed.encode()).hexdigest()
        int_seed = int(hash_seed, 16)
        return random.Random(int_seed)

    def _encode_char(self, char: str) -> str:
        value = ord(char)
        noise = self.rng.randint(100000000, 999999999)
        mixed = value ^ noise
        return hex(mixed)[2:]

    def _decode_char(self, encoded: str) -> str:
        encoded_int = int(encoded, 16)
        noise = self.rng.randint(100000000, 999999999)
        value = encoded_int ^ noise
        return chr(value)

    def encode(self, text: str) -> str:
        blocks = []
        self.current_seed = self.base_seed
        self.rng = self._create_rng(self.current_seed)

        for char in text:
            block = self._encode_char(char)
            blocks.append(block)

            if self.mode == "dynamic":
                self.current_seed = mutate_seed(self.current_seed, block)
                self.rng = self._create_rng(self.current_seed)

        return "|".join(blocks)

    def decode(self, encoded_text: str) -> str:
        chars = []
        self.current_seed = self.base_seed
        self.rng = self._create_rng(self.current_seed)

        for block in encoded_text.split("|"):
            char = self._decode_char(block)
            chars.append(char)

            if self.mode == "dynamic":
                self.current_seed = mutate_seed(self.current_seed, block)
                self.rng = self._create_rng(self.current_seed)

        return "".join(chars)

