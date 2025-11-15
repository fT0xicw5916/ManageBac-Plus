import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from hashlib import sha256
from cryptography.hazmat.backends import default_backend
import base64


def encrypt(key, data):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(sha256(key.encode("utf-8")).digest()), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(data.encode("utf-8")) + encryptor.finalize()

    return base64.b64encode(iv + encrypted).decode("utf-8")


def decrypt(key, data):
    byte = base64.b64decode(data)
    iv = byte[:16]
    encrypted = byte[16:]

    cipher = Cipher(algorithms.AES(sha256(key.encode("utf-8")).digest()), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted = decryptor.update(encrypted) + decryptor.finalize()

    return decrypted.decode("utf-8")
