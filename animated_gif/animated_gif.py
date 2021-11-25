import glob
from PIL import Image

# filepaths
fp_in = "dataset/images_03_part1/*.jpg"
fp_out = "out_image.gif"

size = (512, 384)

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img, *imgs_resized = [im.resize(size, Image.ANTIALIAS) for im in imgs]
img.save(fp=fp_out, format='GIF', append_images=imgs_resized,
         save_all=True, duration=200, loop=0)
