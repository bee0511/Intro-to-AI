import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def image_resize(image):
  height, width = image.shape[0], image.shape[1]
  width_new = 800
  height_new = 600
  if width / height >= width_new / height_new:
    image_new = cv2.resize(image, (width_new, int(height * width_new / width)))
  else:
    image_new = cv2.resize(image, (int(width * height_new / height), height_new))
  return image_new

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    regions = {}
    current_filename = ""
    with open(dataPath) as f:
      for line in f:
        s = line.split(' ')
        if len(s) == 2:
          current_filename = s[0]
          regions[current_filename] = []
        elif len(s) == 4:
          regions[current_filename].append([int(string) for string in s])
    for (filename, regions) in regions.items():
      image = cv2.imread(f"data/detect/{filename}")
      gray_image = cv2.imread(f"data/detect/{filename}", cv2.IMREAD_GRAYSCALE)
      for region in regions:
        x, y, w, h = region
        crop_image = gray_image[y:y+h, x:x+w]
        crop_image = cv2.resize(crop_image, (19, 19), interpolation=cv2.INTER_NEAREST)
        is_face = clf.classify(crop_image)
        image = cv2.rectangle(image, (x, y), (x+w, y+h), color=(0, 255, 0) if is_face else (0, 0, 255), thickness=3)
      image = image_resize(image)
      cv2.imshow(filename, image)
      cv2.waitKey(0)
    #raise NotImplementedError("To be implemented")
    # End your code (Part 4)
