"""
nlt/__init__.py - Main package interface
"""
from .encode import NültackEncoder
from .decode import NültackDecoder
from .execute import NültackExecutor

__version__ = "1.0.0"
__all__ = ['encode', 'decode', 'execute']

# Shortcut functions
def encode(source: str) -> str:
    return NültackEncoder().encode(source)

def decode(payload: str) -> str:
    return NültackDecoder().decode(payload)

def execute(payload: str, globals=None, locals=None) -> None:
    return NültackExecutor().execute(payload, globals, locals)
