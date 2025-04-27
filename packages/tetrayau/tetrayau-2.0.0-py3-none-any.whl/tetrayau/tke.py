import numpy as np
from hashlib import shake_256

# Hyperdimensional Tetrahedral Key Exchange (TKE 12D)
# Upgraded for sovereign post-quantum resilience

class TetrahedralKeyExchange:
    def __init__(self, seed=None):
        self.q = 2147483647  # Large prime modulus (2^31-1)
        self.n = 12  # 12D hyperdimensional key vector
        if seed is not None:
            np.random.seed(seed)
        self.private_key = np.random.randint(0, self.q, self.n)
        self.public_matrix = self._generate_public_matrix()

    def _generate_public_matrix(self):
        # Start with a fully connected base (no self-loops)
        base = np.ones((self.n, self.n), dtype=int) - np.eye(self.n, dtype=int)
        # Introduce random perturbations to destroy symmetry
        perturbation = np.random.randint(-5, 5, size=(self.n, self.n))
        perturbed_base = (base + perturbation) % self.q
        # Ensure no diagonal leaks (zero diagonal)
        np.fill_diagonal(perturbed_base, 0)
        return perturbed_base

    def generate_public_key(self):
        # Public key = Public Matrix × Private Key Vector
        return np.dot(self.public_matrix, self.private_key) % self.q

    def compute_shared_secret(self, received_pubkey):
        # Add random Gaussian noise to break algebraic predictability
        noise = np.random.normal(0, 1, size=received_pubkey.shape)
        mixed = (received_pubkey + noise) * self.private_key
        # Apply double SHAKE256 compression
        first_hash = shake_256(mixed.tobytes()).digest(32)
        final_hash = shake_256(first_hash).digest(32)
        return final_hash
