"""
nlt/decode.py - Nültack decoding module
"""
from .core import Nültack
import base64
import zlib

class NültackDecoder(Nültack):
    def __init__(self, version: int = 1):
        super().__init__(version)
    
    def decode(self, payload: str) -> str:
        """
        Decode Nültack payload to Python source
        """
        try:
            # Base64 decode
            decoded = base64.b64decode(payload.encode('ascii'))
            
            # Extract components
            pad = decoded[:16]
            obfuscated = decoded[16:]
            
            # Deobfuscate
            data = self._apply_xor(obfuscated, pad)
            
            # Verify header
            magic = data[:4]
            if magic != self._magic:
                raise ValueError("Invalid Nültack magic header")
                
            version = int.from_bytes(data[4:6], 'big')
            salt = data[6:22]
            
            if salt != self._salt:
                raise ValueError("Invalid salt value")
                
            # Get actual payload
            b64_encoded = data[22:]
            compressed = base64.b64decode(b64_encoded)
            return zlib.decompress(compressed).decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Decoding failed: {str(e)}")
