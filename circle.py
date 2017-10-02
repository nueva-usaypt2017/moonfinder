import cv2
import numpy as np
import sys
from copy import copy


class CircleFinder():
    def __init__(self, path):
        if type(path) == str:
            self.image_path = path
        else:
            self.image_path = None
            self.img = path

    def get_center_coords(self):
        if self.image_path is None:
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            img = cv2.imread(self.image_path, 0)
        img = cv2.medianBlur(img, 5)
        self.img = img
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=60, param2=30, minRadius=5,
                                   maxRadius=300)
        if circles is None:
            return None
        circles = np.uint16(np.around(circles))
        max_index = 0
        for ii, i in enumerate(circles[0, :]):
            if i[2] > circles[0, max_index, 2]:  # find largest one
                max_index = ii
        self.found_circle = circles[0, max_index]
        return self.found_circle  # x, y, radius

    def show_circle(self):
        cv2.circle(self.img, (self.found_circle[0], self.found_circle[1]), self.found_circle[2], (255, 0, 0), 5)
        
        scale = 0.2
        self.img = cv2.resize(self.img, (0, 0), fx=scale, fy=scale)
        
        cv2.imshow("image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



if __name__ == '__main__':
    cf = CircleFinder(sys.argv[1])
    print cf.get_center_coords()
