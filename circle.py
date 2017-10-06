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
            self.found_circle = None

    def get_center_coords(self):
        scale = 0.2

        if self.image_path is None:
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            img = cv2.imread(self.image_path, 0)

        # Increase exposure
        thresh = 200
        img_bw = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
        img_bw = cv2.medianBlur(img_bw, 5)

        cv2.imshow("image", cv2.resize(img_bw, (0, 0), fx=scale, fy=scale))
        cv2.waitKey()
        cv2.destroyAllWindows()

        self.img = img
        img = cv2.medianBlur(img, 5)

        # Find image centroid
        M = cv2.moments(img_bw)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        cv2.circle(img, (cx, cy), 7, (0, 0, 0), -1)
        cv2.imshow("image", cv2.resize(img, (0, 0), fx=scale, fy=scale))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Compute circle radius with number of white pixels in thresholded image
        radius = np.sqrt(np.sum(img_bw) / (np.pi * 255))

        self.found_circle = (cx, cy, radius)

        return self.found_circle  # x, y, radius


    def show_circle(self, circle):
        cv2.circle(self.img, (circle[0], circle[1]), int(circle[2]), (255, 0, 0), 5)

        scale = 0.2
        scaled = cv2.resize(self.img, (0, 0), fx=scale, fy=scale)

        cv2.imshow("image", scaled)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_circles(self, circles):
        for circle in circles:
            cv2.circle(
                self.img, (circle[0], circle[1]), int(circle[2]), (255, 0, 0), 5)

        scale = 0.2
        scaled = cv2.resize(self.img, (0, 0), fx=scale, fy=scale)

        cv2.imshow("image", scaled)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    cf = CircleFinder(sys.argv[1])
    print cf.get_center_coords()
