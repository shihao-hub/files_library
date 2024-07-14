import cv2
import matplotlib.pyplot as plt
import numpy as np

# img = cv2.imread(r"resources/20210705160801165.jpg")
image = cv2.imread(r"resources/邮箱.png", -1)

if image is None or image.shape[0] == 0 or image.shape[1] == 0:
    print('Error: Image has invalid size')
else:
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
