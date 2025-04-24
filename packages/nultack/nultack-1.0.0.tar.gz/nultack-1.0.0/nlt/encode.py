"""
nlt/encode.py - Nültack encoding module
"""
from .core import Nültack
import base64
import zlib

class NültackEncoder(Nültack):
    def __init__(self, version: int = 1):
        super().__init__(version)
    
    def encode(self, source: str, compression_level: int = 6) -> str:
        """
        Encode Python source to Nültack format
        """
        if not self._validate_python(source):
            raise ValueError("Invalid Python syntax")
        
        # Compression and base64
        compressed = zlib.compress(source.encode('utf-8'), compression_level)
        b64_encoded = base64.b64encode(compressed)
        
        # Add metadata
        header = self._magic + self.version.to_bytes(2, 'big') + self._salt
        payload = header + b64_encoded
        
        # Obfuscation
        pad = self._generate_pad()
        obfuscated = self._apply_xor(payload, pad)
        
        # Final encoding
        return base64.b64encode(pad + obfuscated).decode('ascii')
