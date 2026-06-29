import logging

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

logger = logging.getLogger(__name__)

# ==========================================
# ARGON2 CONFIGURATION
# ==========================================
# These parameters dictate how much CPU/Memory Argon2 uses.
# Time cost = iterations. Memory cost = KB (65536 = 64MB). Parallelism = threads.
# These are safe defaults for modern servers. If on a low-memory VPS, lower memory_cost.
_ph = PasswordHasher(
    time_cost=3,  # Number of iterations
    memory_cost=65536,  # 64 MiB memory usage
    parallelism=4,  # Number of parallel threads
    hash_len=32,  # Hash output length
    salt_len=16,  # Salt length
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against an Argon2 hash.
    Returns True on match, False on mismatch or error.
    """
    try:
        _ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
    except Exception as e:
        # Log unexpected argon2 errors, but fail safely
        logger.exception("Unexpected error verifying password: %s", e)
        return False


def get_password_hash(password: str) -> str:
    """Hashes a plain text password using Argon2id."""
    return _ph.hash(password)


def need_to_rehash(hashed_password: str) -> bool:
    """
    Security feature: Argon2 parameters might change in the future.
    Call this on successful login. If True, re-hash the password and save it.
    """
    return _ph.check_needs_rehash(hashed_password)
