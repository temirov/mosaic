from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from dimming_direction import DimmingDirection
from utils import converters


@dataclass
class ImageDimmer:
    image: Image
    path: Path
    dimming_direction: DimmingDirection
    dimming_strength: float
    image_width: int = field(init=False)
    image_height: int = field(init=False)

    def __post_init__(self):
        self.image_width, self.image_height = self.image.size

    def to_dimmed_name(self) -> Path:
        new_name = self.path.with_name(
            f"{self.path.stem}_dimmed_{self.dimming_direction}_{self.dimming_strength}.jpeg"
        )
        return new_name

    def dim(self) -> Image:
        if self.dimming_direction == DimmingDirection.UNIFORMED:
            dimmed_image = Image.eval(self.image, lambda x: x * self.dimming_strength)
        else:
            dimmed_image = Image.new('RGB', (self.image_width, self.image_height))
            for w in range(0, self.image_width):
                for h in range(0, self.image_height):
                    px = self.image.getpixel((w, h))
                    new_pixel = self.__change_pixel_brightness(px, (w, h))
                    dimmed_image.putpixel((w, h), new_pixel)
        return dimmed_image

    def __brightness_coefficient(self, coordinates: tuple[int, int]) -> float:
        width_point, height_point = coordinates
        if self.dimming_direction == DimmingDirection.UNIFORMED:
            return self.dimming_strength
        if self.dimming_direction == DimmingDirection.LEFT_TO_RIGHT:
            return width_point / converters.string_to_float(self.image_width)
        if self.dimming_direction == DimmingDirection.RIGHT_TO_LEFT:
            return 1 - (width_point / converters.string_to_float(self.image_width))
        if self.dimming_direction == DimmingDirection.TOP_TO_BOTTOM:
            return height_point / converters.string_to_float(self.image_height)
        if self.dimming_direction == DimmingDirection.BOTTOM_TO_TOP:
            return 1 - (height_point / converters.string_to_float(self.image_height))

    def __change_pixel_brightness(self, pixel: tuple[int, ...], coordinates: tuple[int, int]) -> tuple[
        int, ...]:
        result = []
        for color in pixel:
            new_color = int(self.dimming_strength * self.__brightness_coefficient(coordinates) * color)
            result.append(new_color)
        return tuple(result)
