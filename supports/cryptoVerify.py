import hashlib

PASSWORD = "d210ae60501cc5e4df5e5dbf094af2ae150b4ce03b2ca67c827656d58a0866e1"


def verify(plain_text):
    if hashlib.sha256(plain_text.encode()).hexdigest() == PASSWORD:
        return True
    return False
