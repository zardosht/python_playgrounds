import glob
import os
import pathlib

path_to_images = "./images_03_part1_copy"

paths = pathlib.Path(path_to_images).glob("*")

# for path_str in paths:
#     path = pathlib.Path(path_str)
#     if path.stem[-1] in ["1"]:
#         continue
#     else:
#         os.remove(path)

keep = []
for path_str in paths:
    path = pathlib.Path(path_str)
    filename = path.name
    if filename.endswith("jpg"):
        keep.append(path.stem)

paths = pathlib.Path(path_to_images).glob("*")
for path_str in paths:
    path = pathlib.Path(path_str)
    filename = path.stem
    if not filename in keep: 
        os.remove(path)
    

