# sim/ledger.py

import hashlib

class Ledger:
    def __init__(self):
        self.chain = []

    def add_block(self, node_id, state_hash, timestamp):
        block_data = f'{node_id}|{state_hash.hex()}|{timestamp}'.encode()
        block_hash = hashlib.shake_256(block_data).digest(32)
        self.chain.append({
            'node': node_id,
            'hash': block_hash,
            'timestamp': timestamp
        })

    def last_hash(self):
        return self.chain[-1]['hash'] if self.chain else b'\x00' * 32
