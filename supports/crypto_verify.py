import hashlib

PASSWORD = "8276a624bc555994a749f9160b5043875d98d6810dd20008a439e32b07d74a38"


def verify(plain_text):
    if hashlib.sha256(plain_text.encode()).hexdigest() == PASSWORD:
        return True
    return False
