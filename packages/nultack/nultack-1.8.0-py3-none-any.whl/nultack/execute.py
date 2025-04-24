"""
nlt/execute.py - Nültack execution module
"""
from .decode import NültackDecoder
from typing import Optional, Dict, Any

class NültackExecutor(NültackDecoder):
    def __init__(self, version: int = 1):
        super().__init__(version)
    
    def execute(self, 
               payload: str,
               globals: Optional[Dict[str, Any]] = None,
               locals: Optional[Dict[str, Any]] = None) -> None:
        """
        Execute Nültack payload
        """
        if globals is None:
            globals = {}
        if locals is None:
            locals = {}
            
        source = self.decode(payload)
        code = compile(source, '<nlt_exec>', 'exec')
        exec(code, globals, locals)
