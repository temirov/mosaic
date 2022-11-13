#!/usr/bin/env python3

import argparse
import logging

from dimming_direction import DimmingDirection
from image_dimmer import ImageDimmer
from image_grayscale_colorizer import ImageGrayscaleColorizer
from image_stitcher import ImageStitcher
from tiling_image import TilingImage
from utils import converters
from utils.logger import Logger
from utils.path_utils import PathUtils


def __parse_args():
    usage = """
        %(prog)s --source <TILING_IMAGE> --width <UNIQUE_ID_OF_A_PERSON> --height <GLOB> --dim <DIMMING_STRENGTH> --log <WARN|INFO|DEBUG>
        """
    parser = argparse.ArgumentParser(description='Face extractor', usage=usage)
    parser.add_argument('--source',
                        help='path to the tiling image',
                        type=converters.string_to_path,
                        dest='source_image',
                        required=True)
    parser.add_argument('--width',
                        help='The width of resulting image',
                        type=converters.string_to_int,
                        dest='width',
                        required=True)
    parser.add_argument('--height',
                        help='The height of resulting image',
                        type=converters.string_to_int,
                        dest='height',
                        required=True)
    parser.add_argument('--white_to',
                        help='A color to replace white color',
                        type=str,
                        dest='white_to',
                        required=False)
    parser.add_argument('--black_to',
                        help='A color to replace black color',
                        type=str,
                        dest='black_to',
                        required=False)
    parser.add_argument('--dim',
                        help='Dimming strength',
                        type=converters.string_to_float,
                        dest='dimming_strength',
                        required=False)
    parser.add_argument('--dimming_direction',
                        help='Dimming direction',
                        type=converters.string_to_dimming_direction,
                        dest='dimming_direction',
                        default=DimmingDirection.UNIFORMED,
                        required=False)
    parser.add_argument('--log',
                        help='Set logging level, the default is WARNING',
                        type=converters.string_to_loglevel,
                        default=logging.WARN,
                        dest='log_level')

    return parser.parse_args()


def main():
    arguments = __parse_args()
    logger = Logger(arguments.log_level)
    path_utils = PathUtils()

    for file in [arguments.source_image]:
        path_utils.raise_when_no_file(file)
    tiling_image = path_utils.as_path(arguments.source_image)
    tiling_image = TilingImage(tiling_image)

    image_stitcher = ImageStitcher(tiling_image, arguments.width, arguments.height)
    mosaic = image_stitcher.stitch()
    mosaic_name = image_stitcher.to_stitched_name()
    mosaic.save(mosaic_name)
    logger.log(f"Mosaic {mosaic_name} has been saved")

    if arguments.white_to or arguments.black_to:
        image_grayscale_colorizer = ImageGrayscaleColorizer(image=mosaic, path=mosaic_name, white_to=arguments.white_to,
                                                            black_to=arguments.black_to)
        colorized_image = image_grayscale_colorizer.colorize()
        colorized_name = image_grayscale_colorizer.to_colorized_name()
        colorized_image.save(colorized_name)
        logger.log(f"Colorized image {colorized_name} has been saved")

    if arguments.dimming_strength:
        if arguments.dimming_strength < 0.0 or arguments.dimming_strength > 1.0:
            raise RuntimeError("Dimming strength must be between 0.0 and 1.0")

        image_dimmer = ImageDimmer(
            image=mosaic,
            path=mosaic_name,
            dimming_strength=arguments.dimming_strength,
            dimming_direction=arguments.dimming_direction
        )
        dimmed_image = image_dimmer.dim()
        dimmed_name = image_dimmer.to_dimmed_name()
        dimmed_image.save(dimmed_name)
        logger.log(f"Dimmed image {dimmed_name} has been saved")


if __name__ == '__main__':
    main()
