# in hash_test.py
import hashlib
# The encode() method encodes the string, using the specified encoding. If no encoding is specified, UTF-8 will be used.
encode = 'A'.encode()
print(encode)
# hexdigest turns hash object into a hashed string
print(hashlib.sha256(encode).hexdigest())
# notice how every print statement returns the same hash with th same input
print(hashlib.sha256(encode).hexdigest())
print(hashlib.sha256(encode).hexdigest())
print(hashlib.sha256(encode).hexdigest())