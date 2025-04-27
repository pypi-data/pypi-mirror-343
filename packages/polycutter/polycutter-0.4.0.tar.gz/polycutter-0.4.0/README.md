
# polycutter

lossless media cut tool

## usage

this tool can be used to losslessly cut segments out of videos and stitch them together.

simple example usage (a lot more fancy features are supported, pass `-h`)

```sh
poetry run polycutter -v debug cut -i /path/to/input.mp4 -o /path/to/output.mp4 --segments "00:08-00:45,04:43-05:18"
```
