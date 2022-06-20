import gzip
import lzma as xz
import random
import string
from pathlib import Path
from typing import Dict, List, Tuple, Union

import numpy as np
from PIL import Image


def create_random_str(length: int = 10) -> str:
    """Generate a random file name"""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_image(folder: Path, image_name: str, resolution: Tuple, format: str = "png") -> None:
    """Create a random image in a given directory"""
    folder.mkdir(exist_ok=True, parents=True)

    img = np.random.rand(resolution[0], resolution[1], 3) * 255
    img = Image.fromarray(img.astype("uint8")).convert("RGBA")
    img.save(folder / f"{image_name}.{format}")


def create_image_folder(folder: Path, image_names: Union[int, List], resolution: Tuple, format: str = "png") -> None:
    """Create an example directory filled with random images"""
    if isinstance(image_names, int):
        image_names = [create_random_str() for _ in range(image_names)]

    for name in image_names:
        create_image(folder, name, resolution, format)


def create_random_dict(attributes: List[str]) -> Dict:
    """Create random blob of json"""
    result_dict = {}
    for a in attributes:
        result_dict[a] = create_random_str()
    return result_dict


def save_gzip(file: Path, content: str) -> None:
    """Save string as gz"""
    with gzip.open(file, "wb") as f:
        f.write(content.encode())


def save_xz(file: Path, content: str) -> None:
    """Save string as gz"""
    with open(file, "wb") as f:
        f.write(xz.compress(content.encode()))
