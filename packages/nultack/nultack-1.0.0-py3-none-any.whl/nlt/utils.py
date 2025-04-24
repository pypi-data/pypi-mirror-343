"""
nlt/utils.py - Modul Utilitas Tambahan untuk Nültack

Fitur:
1. String Obfuscation
2. Auto-Execution Detection
3. Payload Validation
4. Advanced Encoding Schemes
"""

import re
import hashlib
from typing import Union, Optional

# ======================== STRING OBFUSCATION ========================
def obfuscate_string(s: str, method: str = "xor") -> str:
    """
    Mengaburkan string dengan metode tertentu.
    
    Args:
        s: String yang akan diobfuscate
        method: Metode obfuscation (xor, reverse, base64)
    
    Returns:
        String terobfuscasi
    """
    if method == "xor":
        xor_key = 0x55
        return ''.join(chr(ord(c) ^ xor_key) for c in s)
    elif method == "reverse":
        return s[::-1]
    elif method == "base64":
        import base64
        return base64.b64encode(s.encode()).decode()
    return s

def deobfuscate_string(s: str, method: str = "xor") -> str:
    """
    Membalikkan proses obfuscation string.
    """
    if method == "xor":
        return obfuscate_string(s, "xor")  # XOR reversible
    elif method == "reverse":
        return s[::-1]
    elif method == "base64":
        import base64
        return base64.b64decode(s.encode()).decode()
    return s

# ======================== PAYLOAD VALIDATION ========================
def is_valid_nültack(payload: str) -> bool:
    """
    Memeriksa apakah payload adalah Nültack yang valid.
    """
    try:
        import base64
        decoded = base64.b64decode(payload.encode())
        return len(decoded) > 20  # Minimal panjang payload
    except:
        return False

def get_payload_info(payload: str) -> dict:
    """
    Mendapatkan informasi versi dan metadata dari payload.
    """
    from nlt import Nültack
    try:
        nlt = Nültack()
        decoded = nlt.decode(payload)
        return {
            "version": nlt.version,
            "length": len(decoded),
            "is_executable": is_python_code(decoded)
        }
    except:
        return {"error": "Invalid Nültack payload"}

# ======================== CODE ANALYSIS ========================
def is_python_code(s: str) -> bool:
    """
    Memeriksa apakah string merupakan kode Python yang valid.
    """
    try:
        compile(s, "<nlt_check>", "exec")
        return True
    except SyntaxError:
        return False

def detect_auto_execution() -> bool:
    """
    Mendeteksi apakah kode sedang dijalankan secara otomatis.
    Berguna untuk mencegah eksekusi tidak sah.
    """
    import __main__
    return not hasattr(__main__, '__file__')

# ======================== ADVANCED ENCODING ========================
def hash_based_encoding(s: str, secret: str = "Nültack") -> str:
    """
    Encoding berbasis hash untuk lapisan keamanan tambahan.
    """
    h = hashlib.sha256(secret.encode()).digest()
    encoded = bytearray()
    for i, c in enumerate(s.encode()):
        encoded.append(c ^ h[i % len(h)])
    return bytes(encoded).hex()

def hash_based_decoding(hex_str: str, secret: str = "Nültack") -> str:
    """
    Decoding untuk hash_based_encoding.
    """
    h = hashlib.sha256(secret.encode()).digest()
    encoded = bytes.fromhex(hex_str)
    decoded = bytearray()
    for i, c in enumerate(encoded):
        decoded.append(c ^ h[i % len(h)])
    return decoded.decode()

# ======================== SECURITY UTILS ========================
def generate_license_key(length: int = 32) -> str:
    """
    Membuat license key acak untuk validasi.
    """
    import secrets
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def verify_license_key(key: str, pattern: str = r"^NLT-[A-Z0-9]{28}$") -> bool:
    """
    Memverifikasi format license key.
    """
    return re.match(pattern, key) is not None
