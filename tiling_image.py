from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener


@dataclass
class TilingImage:
    path: Path
    image: Image = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)

    def __post_init__(self):
        register_heif_opener()
        self.image = self.__load_image()
        self.width, self.height = self.__get_image_size()

    def __load_image(self) -> Image:
        return Image.open(self.path.as_posix())

    def __get_image_size(self) -> tuple[int, int]:
        width, height = self.image.size
        return width, height
