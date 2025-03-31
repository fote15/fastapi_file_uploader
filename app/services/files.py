import uuid

def generate_random_hash() -> str:
    """Generate a random unique hash every time."""
    return uuid.uuid4().hex

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename and keep only safe ones."""
    return "".join(c if c.isalnum() or c in ("_", "-", ".") else "_" for c in filename)
