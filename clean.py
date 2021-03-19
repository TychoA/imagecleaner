# Script for iterating over a given directory, and removing images that are similar
# to images inside it.
#
# Author: Tycho Atsma <tycho.atsma@gmail.com>

# Dependencies
import os, sys, threading, cv2, argparse
from skimage.metrics import mean_squared_error as mse
from PIL import Image
import numpy as np

def image(path):
    """
    Function to load an image and convert it to a OpenCV grayscale image.

    Parameters:
        path: path to image

    Returns:
        cv2.Image
    """
    # Load the image, resize it, and convert to grayscale 
    img = Image.open(path).resize((150, 100), Image.ANTIALIAS)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    # Expose the image
    return img

def blur(image):
    """
    Function to calculate the level of blur in an opencv image.

    Parameters:
        image: opencv image

    Returns:
        float
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()

def remove(path):
    """
    Function to remove a file.

    Parameters:
        path: path of the image
    """
    if os.path.isfile(path):
        os.remove(path)
        removed.append(path)
        print(f"Removed {path}")

class ImageBatch(threading.Thread):
    """
    Class for creating a thread that processes a batch of images and decides
    to remove images based on their similarity with other images.
    """

    def __init__(self, batch):
        """
        Constructor

        Parameters:
            batch: list of images to compare to all other images.
        """
        threading.Thread.__init__(self)
        self.batch = batch

    def run(self):
        """
        Method to execute when the thread has started
        """
        for (i, (pathA, imageA)) in enumerate(self.batch):
            for (y, (pathB, imageB)) in enumerate(images):

                # Skip the same images, those will always be equal
                if pathA == pathB:
                    continue

                # Skip if one of them has already been removed
                if pathA in removed or pathB in removed:
                    continue

                # Remove an image if its too blurry or too similar
                if blur(imageA) < blur_threshold:
                    remove(pathA)
                elif blur(imageB) < blur_threshold:
                    remove(pathB)
                if mse(imageA, imageB) < similarity_threshold:
                    remove(pathB)


# Run as main
if __name__ == "__main__":

    # Set up the cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the directory of images that need to be processed")
    parser.add_argument("--similarity", help="Similarity threshold (MSE) below which images are removed (default: 2000)", type=int, default=2000)
    parser.add_argument("--blur", help="Blur threshold (Laplacian) below which images are removed (default: 150)", type=float, default=150.0)
    parser.add_argument("--batchsize", help="Number of images to process per batch. Less means more images are processed in parallel. Use with caution, this increases the memory and cpu usage significantly (default: 5).", type=int, default=5)

    # And parse the input
    args = parser.parse_args()
    target = args.path
    batchsize = args.batchsize
    similarity_threshold = args.similarity
    blur_threshold = args.blur

    # Get all images and convert them into usable properties
    images = [(entry.path, image(entry.path)) for entry in os.scandir(target)]
    removed = []

    # Collection of threads and batches to put in threads
    batches = (images[i * batchsize:(i+1) * batchsize] for i in range((len(images) + batchsize - 1) // batchsize))
    threads = []

    for batch in batches:
        thread = ImageBatch(batch)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

