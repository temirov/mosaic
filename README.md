# Mosaic

This program allows to stitch a titling image into a large file, forming large canvas of repetitive patterns.

## Extra functionality

### Dimming an image

A dimming of a given strength can be applied to the image using 7 different options:

1. Uniformed
2. Left-to-right
3. Right-to-left
4. Top-to-bottom
5. Bottom-to-top
6. Left bottom corner to right top corner
7. Left top corner to right bottom corner

### Making colorized greyscale

An image can be turned into a greyscale of predefined colors

## Example

```shell
mosaic.py --source "/tmp/tiles/cars.png" --width 2000 --height 1000 --dim 0.3 --dimming_direction left_to_right --log err
```

### Tiling image

![](assets/cars.png)

### Mosaic (stitched image)

![](assets/cars_mosaic_2000_1000.jpeg)

### Mosaic (stitched and dimmed image)

![](assets/cars_mosaic_2000_1000_dimmed_DimmingDirection.LEFT_TO_RIGHT_0.3.jpeg)

### Mosaic (stitched and colorized image)

![](assets/cars_mosaic_2000_1000_colorized_orange_yellow.jpeg)