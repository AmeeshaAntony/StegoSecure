import hashlib
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_logs = []  # Store logs before adding them to the chain
        self.create_block(previous_hash="0")  # Genesis block

    def create_block(self, previous_hash):
        """Create a new block and add it to the blockchain."""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'logs': self.pending_logs,  # Add pending logs to the new block
            'previous_hash': previous_hash,
            'hash': "",  # Will be generated
        }
        block['hash'] = self.hash(block)  # Generate block hash
        self.chain.append(block)
        self.pending_logs = []  # Clear pending logs after adding to block
        return block

    def add_log(self, log_entry):
        """Add a log entry to pending logs."""
        self.pending_logs.append(log_entry)

    def hash(self, block):
        """Generate a SHA-256 hash for a block."""
        block_string = f"{block['index']}{block['timestamp']}{block['logs']}{block['previous_hash']}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def get_logs(self):
        logs = []
        for block in self.chain:
            if block['logs']:  # Only add non-empty logs
                logs.extend(block['logs'])
        return logs if logs else ["❌ No logs found."]


    def mine_block(self):
        """Mine a new block and commit pending logs to the blockchain."""
        if not self.pending_logs:
            return "❌ No new logs to commit."

        last_block = self.chain[-1]
        new_block = self.create_block(previous_hash=last_block['hash'])  # Commit pending logs
        return f"✅ New block mined! Block Index: {new_block['index']}, Hash: {new_block['hash']}"

# Create blockchain instance
blockchain = Blockchain()
