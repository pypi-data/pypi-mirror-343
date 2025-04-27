from pathlib import Path

tke_code = """\
import numpy as np
from hashlib import shake_256

# Tetrahedral Key Exchange (TKE)
# Inspired by 3D Platonic Tetrahedral rotations in hyperlattice space

class TetrahedralKeyExchange:
    def __init__(self, seed=None):
        self.q = 8388607  # Large prime modulus
        self.n = 4  # Tetrahedron has 4 vertices
        if seed:
            np.random.seed(seed)
        self.private_key = np.random.randint(0, self.q, self.n)
        self.public_matrix = self._generate_public_matrix()

    def _generate_public_matrix(self):
        # Generate a public 4x4 tetrahedral-inspired matrix
        base = np.array([
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [1, 1, 1, 0]
        ])
        rotation = np.random.randint(1, 10)
        return np.mod(np.linalg.matrix_power(base, rotation), self.q)

    def generate_public_key(self):
        # Public key = Public Matrix × Private Vector
        return np.dot(self.public_matrix, self.private_key) % self.q

    def compute_shared_secret(self, received_pubkey):
        return shake_256(np.dot(received_pubkey, self.private_key).tobytes()).digest(32)


# Example usage
if __name__ == "__main__":
    alice = TetrahedralKeyExchange(seed=42)
    bob = TetrahedralKeyExchange(seed=99)

    alice_pub = alice.generate_public_key()
    bob_pub = bob.generate_public_key()

    alice_secret = alice.compute_shared_secret(bob_pub)
    bob_secret = bob.compute_shared_secret(alice_pub)

    print("Alice's Shared Secret:", alice_secret.hex())
    print("Bob's Shared Secret:  ", bob_secret.hex())
    print("Match:", alice_secret == bob_secret)
"""

# Save to src/tke.py
output_path = Path("/mnt/data/TetraCrypt_FullSystem/src/tke.py")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(tke_code)

output_path.name  # show just filename
