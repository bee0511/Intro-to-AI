import os
import cv2

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
    dataset = []
    for flag, face_or_nonface in enumerate(["face", "non-face"]):
      for filename in os.listdir(f"{dataPath}/{face_or_nonface}"):
        image = cv2.imread(f"{dataPath}/{face_or_nonface}/{filename}", -1)
        dataset.append((image, flag))
    
    # End your code (Part 1)
    return dataset
