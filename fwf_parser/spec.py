from dataclasses import dataclass
from typing import List

@dataclass
class Spec:
    input_encoding: str
    offsets: List[int]
    line_width: int
    output_encoding: str
