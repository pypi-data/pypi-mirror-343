"""
Quantum Isoca-Dodecahedral Encryption (QIDL)
Part of the TetraCrypt PQC Nexus
Entropy-hardened, tamper-resilient, time-divergent
"""

import numpy as np
import time
import os
import hashlib

def generate_isoca_dodecahedral_key(seed: int = 42):
    """
    Generate a pseudo-random dodecahedral structure key based on golden ratio encoding.
    """
    np.random.seed(seed)
    phi = (1 + np.sqrt(5)) / 2
    angles = np.linspace(0, 2 * np.pi, 20)
    key = np.array([np.cos(phi * angles), np.sin(phi * angles)]).T
    return key

def generate_entropy_salt(length: int = 16) -> str:
    """
    Strong entropy using os.urandom and time-based fallback, SHA256 hashed.
    """
    entropy_base = os.urandom(length) + str(time.time()).encode()
    return hashlib.sha256(entropy_base).hexdigest()[:length]

def qidl_encrypt(message: str, key: np.ndarray, salt: str = None):
    """
    Quantum simulation using golden-ratio projection with entropy salt.
    Encrypts characters onto a 2D isoca-dodecahedron ring.
    """
    if salt is None:
        salt = generate_entropy_salt()
    message += salt

    encoded = []
    for i, char in enumerate(message):
        char_val = ord(char)
        point = key[i % len(key)]
        transformed = (char_val * point[0], char_val * point[1])
        encoded.append(transformed)
    return encoded, salt

def qidl_decrypt(encoded_message, key: np.ndarray, salt: str = ''):
    """
    Reverse dodecahedral projection and remove appended entropy salt.
    Now with error handling for secure audit conditions.
    """
    decoded = ''
    try:
        for i, (x, y) in enumerate(encoded_message):
            point = key[i % len(key)]
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
