import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
    fig, ax = plt.subplots(1, len(regions))
    for index, (filename, regions) in enumerate(regions.items()):
      image = cv2.imread(f"data/detect/{filename}", cv2.IMREAD_GRAYSCALE)
      ax[index].axis('off')
      ax[index].set_title(filename)
      ax[index].imshow(image, cmap='gray')
      for region in regions:
        x, y, w, h = region
        crop_image = image[y:y+h, x:x+w]
        # cv2.imshow("cropped", crop_image)
        # cv2.waitKey(0)
        crop_image = cv2.resize(crop_image, (19, 19), interpolation=cv2.INTER_CUBIC)
        #cv2.imshow("cropped", crop_image)
        #cv2.waitKey(0)
        #print(crop_image)
        is_face = clf.classify(crop_image)
        ax[index].add_patch(Rectangle((x, y), w, h, linewidth = 1, edgecolor='g' if is_face else 'r', fill = False))
    plt.show()
    #raise NotImplementedError("To be implemented")
    # End your code (Part 4)
