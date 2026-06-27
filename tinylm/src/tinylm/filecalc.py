import os
from pathlib import Path

def sum_file(path: Path) -> int:
    """Reads a file of integers and returns their sum"""
    return sum(int(line) for line in path.read_text(encoding="utf-8").splitlines())

def multiply_by_mode(value: int) -> int:
    mode = os.getenv("MULTIPLY_MODE", "double")
    if mode == "double":
        return value * 2
    elif mode == "triple":
        return value * 3
    else:
        raise ValueError(f"Unknown MULTIPLY_MODE: {mode}")
    
    