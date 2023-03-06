# python-svg-workshop

Experiments with Python and generating SVG files. Intended to assist with my creative projects.

Intended to be run from comand line.

## Hexaglyph Test

`python hexaglyphtest.py [-h|--help] [-r] [-g] [-b] [--range] [--side] [--size]`

```default
optional arguments:
  -h, --help     show this help message and exit
  -r R           red value (0-255). Random value will be used if not provided. (default: None)
  -g G           green value (0-255). Random value will be used if not provided. (default: None)
  -b B           blue value (0-255). Random value will be used if not provided. (default: None)
  --range RANGE  variance range for color change. Default selects a random integer from 15-31 (base 10). (default: None)
  --side SIDE    hexes per outer edge, minimum 2. Lower values ignored. (default: 2)
  --size SIZE    widest diameter of the hexagon cells, minimum 25. Lower values ignored. default 100 (default: 100)
```
