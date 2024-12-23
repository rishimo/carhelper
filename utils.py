import hashlib


def create_hash(*args: str) -> str:
    """Create a deterministic hash from multiple strings"""
    combined = "".join(str(arg) for arg in args)
    return hashlib.sha256(combined.encode()).hexdigest()[:32]
