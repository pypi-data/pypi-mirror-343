"""
   Hello, ini can hehe
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
            # Base64 dcode
            decoded = base64.b64decode(payload.encode('ascii'))
            
            # Extract componen
            pad = decoded[:16]
            obfuscated = decoded[16:]
            
            # Deobf
            data = self._apply_xor(obfuscated, pad)
            
            # Verif dlhead
            magic = data[:4]
            if magic != self._magic:
                raise ValueError("Invalid Nültack magic header")
                
            version = int.from_bytes(data[4:6], 'big')
            salt = data[6:22]
            
            if salt != self._salt:
                raise ValueError("Invalid salt value")
                
            # Actuall payload
            b64_encoded = data[22:]
            compressed = base64.b64decode(b64_encoded)
            return zlib.decompress(compressed).decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Decoding failed: {str(e)}")
