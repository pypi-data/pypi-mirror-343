"""
Recursive Tesseract Hashing (RTH)
Hyperdimensional SHAKE256-based hash function operating on nested tensor blocks.
"""

import hashlib
import numpy as np

def recursive_tesseract_hash(data: bytes, depth: int = 4) -> bytes:
    """
    Applies SHAKE256 recursively to simulate hyperdimensional compression layers.

    Args:
        data (bytes): Input binary data
        depth (int): Number of recursive SHAKE256 rounds (each representing a tesseract fold)

    Returns:
        bytes: Final hash output
    """
    h = data
    for i in range(depth):
        shake = hashlib.shake_256()
        shake.update(h)
        h = shake.digest(64)
    return h

def hyperdimensional_entropy_tensor(seed: bytes, dimensions=(4, 4, 4, 4)) -> np.ndarray:
    """
    Generates a hyperdimensional tensor lattice from seed hash.

    Args:
        seed (bytes): Initial seed hash.
        dimensions (tuple): Shape of the tesseract lattice.

    Returns:
        np.ndarray: Populated hyperdimensional tensor.
    """
    tensor = np.frombuffer(seed * 16, dtype=np.uint8)[:np.prod(dimensions)]
    return tensor.reshape(dimensions)
