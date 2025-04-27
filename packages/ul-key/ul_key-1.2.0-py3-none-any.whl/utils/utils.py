import zlib

def mutate_seed(seed: str, block: str) -> str:
    combined = (seed + block).encode('utf-8')
    new_seed = str(zlib.crc32(combined))
    return new_seed

