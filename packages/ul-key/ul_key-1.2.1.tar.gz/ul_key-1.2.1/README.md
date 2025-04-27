# Install
```shell
pip install ul-key==version
```


## Example
```python
from ulkey import encode_ul, decode_ul

encoded = encode_ul("hello world!", seed="ul-key", mode="dynamic")
decoded = decode_ul(encoded, seed="ul-key", mode="dynamic")

print(encoded)
print(decoded)
```


### Examples console use
```none-key
ulkey-encode "text"
````
_________________

```key
ulkey-encode "Текст" --key "мой_секретный_ключ"
```