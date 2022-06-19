import random
import string
from pathlib import Path
from typing import List, Tuple

import numpy as np
from PIL import Image


def create_random_name(length: int = 10) -> str:
    """Generate a random file name"""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_image_folder(folder: Path, image_names: List, resolution: Tuple, format: str = "png") -> None:
    """Create an example directory filled with random images"""
    folder.mkdir(exist_ok=True, parents=True)

    for name in image_names:
        img = np.random.rand(resolution[0], resolution[1], 3) * 255
        img = Image.fromarray(img.astype("uint8")).convert("RGBA")
        img.save(folder / f"{name}.{format}")
