# Mosaic

This program allows to stitch a titling image into a large file, forming large canvas of repetitive patterns.

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