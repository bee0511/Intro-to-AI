import os
import cv2
from operator import itemgetter
def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    #raise NotImplementedError("To be implemented")
    """
    Line 28: use enumerate to put flag 1 on face and flag 0 on non-face.
    Line 29: use os.listdir(f"{dataPath}/{face_or_nonface}") to reach files 
    in training set and testing set. 
    Line 30: use cv2.imread(f"{dataPath}/{face_or_nonface}/{filename}", flags=cv2.IMREAD_GRAYSCALE) 
    to load images in the files. 
    Note that we need to read in grayscale or the compiler will raise
    ValueError: too many values to unpack (expected 2), the reason is the default
    will return BGR, which is 3 dimensional array.
    Line 31: use append to add image and flag into dataset.
    Line 32: Sort the dataset, let the first image to be face image.
    """
    dataset = []
    for flag, face_or_nonface in enumerate(["non-face", "face"]):
      for filename in os.listdir(f"{dataPath}/{face_or_nonface}"):
        image = cv2.imread(f"{dataPath}/{face_or_nonface}/{filename}", flags=cv2.IMREAD_GRAYSCALE)
        dataset.append((image, flag))
    dataset = sorted(dataset, key=itemgetter(1), reverse=True) 
    # End your code (Part 1)
    return dataset
