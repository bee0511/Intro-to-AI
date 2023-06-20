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
    """ 
    Line 29 ~ Line 38: read the file and use regions to store each image's selected region
    Line 39: use plt.subplots to show image, where row is 1 and columns are len(regions)
    Line 40: use enumerate(regions.items()) to iterate all the selected regions.
    Line 41 ~ Line 46: read images and initialize axes.
    Line 47 ~ Line 52: iterate all the regions in the selected image, 
    use classify to check whether the region is face or not, and use add_patch to put green or red
    rectangles on the regions.
    Line 53: show the result.
    """
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
      image = cv2.imread(f"data/detect/{filename}", flags=cv2.IMREAD_UNCHANGED)
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      gray_image = cv2.imread(f"data/detect/{filename}", flags=cv2.IMREAD_GRAYSCALE)
      ax[index].axis('off')
      ax[index].set_title(filename)
      ax[index].imshow(image)
      for region in regions:
        x, y, w, h = region
        crop_image = gray_image[y:y+h, x:x+w]
        crop_image = cv2.resize(crop_image, (19, 19), interpolation=cv2.INTER_CUBIC)
        is_face = clf.classify(crop_image)
        ax[index].add_patch(Rectangle((x, y), w, h, linewidth = 1, edgecolor='g' if is_face else 'r', fill = False))
    plt.show()
    #raise NotImplementedError("To be implemented")
    # End your code (Part 4)

