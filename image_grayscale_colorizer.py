from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps


@dataclass
class ImageGrayscaleColorizer:
    image: Image
    path: Path
    black_to: str = None
    white_to: str = None

    def __post_init__(self):
        if self.black_to is None:
            self.black_to = "black"
        if self.white_to is None:
            self.white_to = "white"

    def to_colorized_name(self) -> Path:
        new_name = self.path.with_name(
            f"{self.path.stem}_colorized_{self.black_to}_{self.white_to}.jpeg"
        )
        return new_name

    def colorize(self) -> Image:
        greyscale_image = ImageOps.grayscale(self.image)
        return ImageOps.colorize(greyscale_image, black=self.black_to, white=self.white_to)
