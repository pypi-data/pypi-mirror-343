import click
from ulkey.core import ULKey

# Функции для кодировки и декодировки
def encode_ul(text: str, key: str = "хаос_и_разложение"):
    ulkey = ULKey(key)
    return ulkey.encode(text)

def decode_ul(encoded_text: str, key: str = "хаос_и_разложение"):
    ulkey = ULKey(key)
    return ulkey.decode(encoded_text)

# CLI команды
@click.command()
@click.argument("text")
@click.option("--key", default="хаос_и_разложение", help="Секретный ключ для кодировки")
def encode_cli(text, key):
    """CLI команда для кодировки текста"""
    encoded_text = encode_ul(text, key)
    print(f"Закодировано: {encoded_text}")

@click.command()
@click.argument("encoded_text")
@click.option("--key", default="хаос_и_разложение", help="Секретный ключ для декодировки")
def decode_cli(encoded_text, key):
    """CLI команда для декодировки текста"""
    decoded_text = decode_ul(encoded_text, key)
    print(f"Декодировано: {decoded_text}")
