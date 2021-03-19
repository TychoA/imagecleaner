# imagecleaner
Python CLI tool to clean a directory of images based on certain image properties.

At the time of writing, the tool removes images of which a very similar counterpart exists and those that are too blurry. The strictness of these actions can be configured using the `--similarity` and `--blur` parameters.

A project that inspired this tool is related to photogrammetry. In the field of photogrammetry, you have to take many images of an object.
Many of these images tend to have a large overlap or are too blurry and become redudant in the modelling step. This script saves you the hassle of manually inspecting all images.

It can also be used to clean up a directory, e.g. removing duplicates.

Usage:
```
python3 clean.py path_to_image_directory

python3 clean.py --help
````
