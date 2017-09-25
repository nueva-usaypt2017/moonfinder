from circle import CircleFinder
from star import StarFinder
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt


class StarDistance():
    def __init__(self, img1, img2):
        self.finder1 = StarFinder(img1)
        self.stars1 = self.finder1.run()
        self.finder2 = StarFinder(img2, self.finder1)
        self.stars2 = self.finder2.run()
        self.img1 = cv2.imread(img1)
        self.img2 = cv2.imread(img2)

    def run(self):
        pts1 = np.float32(self.stars1.values())
        pts2 = np.float32(self.stars2.values())
        print pts2.shape
        print pts1.shape
        M = cv2.getAffineTransform(pts1, pts2)
        rows, cols, ch = self.img1.shape
        dst = cv2.warpAffine(self.img1, M, (cols, rows))
        plt.subplot(121), plt.imshow(self.img2), plt.title('Input')
        plt.subplot(122), plt.imshow(dst), plt.title('Output')
        plt.show()
        moonloc1 = CircleFinder(self.img1).get_center_coords()
        moonloc2 = CircleFinder(dst).get_center_coords()
        return (moonloc1[0] - moonloc2[0], moonloc1[1] - moonloc2[1])


if __name__ == '__main__':
    sd = StarDistance(sys.argv[1], sys.argv[2])
    print sd.run()
