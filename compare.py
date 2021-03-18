# Dependencies
import os, sys, threading, cv2
from skimage.metrics import mean_squared_error as mse
from PIL import Image
import numpy as np

# Parameters and settings for the script
source = sys.argv[1]
threshold = 2000
batchsize = 5
image_size = (150, 100)

def image(path):
    """
    Function to load an image and convert it to a OpenCV grayscale image.

    Parameters:
        path: path to image

    Returns:
        cv2.Image
    """
    # Load the image, resize it, and convert to grayscale 
    img = Image.open(path).resize(image_size, Image.ANTIALIAS)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    # Expose the image
    return img

# Get all images and convert them into usable properties
images = ((fp.name, f"{source}/{fp.name}") for fp in os.scandir(source))
images = [(name, image(path)) for (name, path) in images]

class ImageBatch(threading.Thread):
    """
    Class for creating a thread that processes a batch of images and decides
    to remove images based on their similarity with other images.
    """

    def __init__(self, images):
        threading.Thread.__init__(self)
        self.images = images

    def run(self):
        # And iterate over all images
        for (i, (nameA, imageA)) in enumerate(self.images):
            for (y, (nameB, imageB)) in enumerate(images):

                # Skip the same images, those will always be equal
                if nameA == nameB:
                    continue

                # Remove the image if its too similar
                if mse(imageA, imageB) < threshold:

                    # Remove the file if it exists
                    fp = f"{source}/{nameB}"
                    if os.path.isfile(fp):
                        print('remove', nameA, nameB)
                        os.remove(fp)

# Collection of threads and batches to put in threads
threads = []
batches = (images[i * batchsize:(i+1) * batchsize] for i in range((len(images) + batchsize - 1) // batchsize))

for batch in batches:
    thread = ImageBatch(batch)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
