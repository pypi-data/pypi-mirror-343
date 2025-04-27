"""
Quantum Isoca-Dodecahedral Encryption (QIDL)
"""

import numpy as np
import time
import os
import hashlib

class QuantumLatticeEncryptor:
    def __init__(self, seed: int = 42):
        self.key = self.generate_isoca_dodecahedral_key(seed)

    @staticmethod
    def generate_isoca_dodecahedral_key(seed: int = 42):
        np.random.seed(seed)
        phi = (1 + np.sqrt(5)) / 2
        angles = np.linspace(0, 2 * np.pi, 20)
        key = np.array([np.cos(phi * angles), np.sin(phi * angles)]).T
        return key

    @staticmethod
    def generate_entropy_salt(length: int = 16) -> str:
        entropy_base = os.urandom(length) + str(time.time()).encode()
        return hashlib.sha256(entropy_base).hexdigest()[:length]

    def encrypt(self, message: str, salt: str = None):
        if salt is None:
            salt = self.generate_entropy_salt()
        message += salt

        encoded = []
        for i, char in enumerate(message):
            char_val = ord(char)
            point = self.key[i % len(self.key)]
            transformed = (char_val * point[0], char_val * point[1])
            encoded.append(transformed)
        return encoded, salt

    def decrypt(self, encoded_message, salt: str = ''):
        decoded = ''
        try:
            for i, (x, y) in enumerate(encoded_message):
                point = self.key[i % len(self.key)]
                denom = point[0] + point[1]
                if denom == 0:
                    raise ZeroDivisionError("Dodecahedral key caused divide-by-zero")
                char_val = round((x + y) / denom)
                decoded += chr(int(char_val) % 256)
        except (ZeroDivisionError, ValueError, IndexError) as e:
            print(f"[!] Decryption error: {e}")
            return None

        if salt and decoded.endswith(salt):
            decoded = decoded[:-len(salt)]
        return decoded
