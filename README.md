# imagecompare
Python CLI tool to calculate image similarities of all images in a given directory.

Project that inspired this tool is related to photogrammetry. In the field of photogrammetry, you have to take many images of an object.
Many of these images tend to have a large overlap, and thus become redudant in the modelling step. This script saves you the hassle of having to
manually inspect all images and removing those that are too similar to others.

It can also be used to clean up a directory, e.g. removing duplicates.

Usage:
```
python3 compare.py path_to_image_directory
````

Goals:
- add blur detection
