from skimage.metrics import mean_squared_error as mse
import cv2
import os
from collections import namedtuple
import sys
from time import time
import threading

Similarity = namedtuple('Similarity', ['imageA', 'imageB', 'similarity'])
similarities = []

class ImageBatch(threading.Thread):
    def __init__(self, images):
        threading.Thread.__init__(self)
        self.images = images

    def run(self):
        print('start thread')
        images = self.images
        images = [(name, cv2.imread(path)) for (name, path) in images]
        images = [(name, cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)) for (name, image) in images]

        # And iterate over all images
        for (i, (nameA, imageA)) in enumerate(images):
            for (y, (nameB, imageB)) in enumerate(images):

                # Skip the same images, those will always be equal
                if i == y:
                    continue

                # Calculate the similarity
                similarities.append(Similarity(nameA, nameB, mse(imageA, imageB)))

source = sys.argv[1]
start = time()

# Get all images and convert them into usable properties
images = [(fp.name, f"{source}/{fp.name}") for fp in os.scandir(source)]

batchsize = 30
batches = [images[i * batchsize:(i+1) * batchsize] for i in range((len(images) + batchsize - 1) // batchsize)]
threads = []

for (i, batch) in enumerate(batches):
    thread = ImageBatch(batch)
    thread.start()
    threads.append(thread)

print(len(threads))

for thread in threads:
    thread.join()

print((time() - start))
