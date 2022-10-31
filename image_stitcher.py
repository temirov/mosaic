from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from tiling_image import TilingImage


@dataclass
class ImageStitcher:
    tiling_image: TilingImage
    result_width: int
    result_height: int

    def __post_init__(self):
        Image.MAX_IMAGE_PIXELS = None

    def to_stitched_name(self) -> Path:
        new_name = self.tiling_image.path.with_name(
            f"{self.tiling_image.path.stem}_mosaic_{self.result_width}_{self.result_height}.jpeg")
        return new_name

    def stitch(self) -> Image:
        stitched_image = Image.new('RGB', (self.result_width, self.result_height))
        for i in range(0, self.result_width, self.tiling_image.width):
            for j in range(0, self.result_height, self.tiling_image.height):
                # paste the image at location i, j:
                stitched_image.paste(self.tiling_image.image, (i, j))
        return stitched_image
