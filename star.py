import cv2
import time
# import numpy as np
import sys


class StarFinder():

    recent_xy = ()  # As far as I can tell, having a class variable is the only way to
    #  get the xy val for a click out of the event handler or whatever

    def __init__(self, img_path, prev_starfinder=None):
        self.image = cv2.imread(img_path, 0)
        self.compare = prev_starfinder
        if self.compare:
            self.compare.compare = None  # Not sure if this is necessary but it's probably best
        #  img_path is the image path to find stars in. The optional
        #  argument prev_starfinder is another Starfinder instance.
        #  Once stars have been found in one image, pass the
        #  Starfinder instance to the new starfinder instance so
        #  that the program can give the user instructions for which
        #  star to click.
        self.star_locs = {}
        #  star_locs is a dict of IDs and tuples showing star locs. Format is (ID, x, y).
        #  ID val is for continuity between image searches.

    def display_n_find(self):
        print "Click on star as prompted, then press y to enter star"
        print "Enter n to indicate star is not visible"
        print "If this is the first star image, enter x to close"
        time.sleep(0.25)
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", StarFinder.click_loc)

        scale = 0.2

        if self.compare:
            for ky in self.compare.star_locs.keys():
                cv2.namedWindow("comparison")
                im = cv2.resize(self.compare.image, (0, 0), fx=scale, fy=scale)
                cv2.circle(im, (int(self.compare.star_locs[ky][0] * scale),
                                 int(self.compare.star_locs[ky][1] * scale)), 20, (255, 0, 0), 2)
                cv2.imshow("comparison", im)
                cv2.imshow("image", cv2.resize(
                    self.image, (0, 0), fx=scale, fy=scale))

                key = cv2.waitKey(0) & 0xFF

                if key == ord("y"):
                    true_loc = self.find_star(self.recent_xy, scale)
                    print "Point at " + str(true_loc) + " added."
                    self.star_locs[ky] = (true_loc[0], true_loc[1])

                elif key == ord("n"):
                    pass
                cv2.destroyAllWindows()

        else:
            while True:
                cv2.imshow("image", cv2.resize(
                    self.image, (0, 0), fx=scale, fy=scale))
                key = cv2.waitKey(0) & 0xFF

                if key == ord("y"):
                    true_loc = self.find_star(self.recent_xy, scale)
                    print "Point at " + str(true_loc) + " added."
#                    cv2.circle(self.image, (int(true_loc[0] * scale), int(true_loc[1] * scale)), 20, (255, 0, 0), 2)
#                    cv2.imshow("image", self.image)
                    self.star_locs[hash(time.time()) % 10 ** 8] = (true_loc[0], true_loc[1])

                elif key == ord("x"):
                    break

    def find_star(self, search_point, scale):
        r = 30  # Half the side length of the search square
        print "find_star running"
        search_point = (
            int(search_point[0] / scale), int(search_point[1] / scale))
        crop_img = self.image[search_point[1] - r: search_point[1] + r,
                              search_point[0] - r: search_point[0] + r]
        #  from stackoverflow:
        #  NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        x, y = cv2.minMaxLoc(crop_img)[3]
        x = search_point[0] + x - r
        y = search_point[1] + y - r
        print x, y
        return (x, y)

    def run(self):
        self.display_n_find()
        return self.star_locs
        #  Note: remember the format is (ID, x, y). This is important for comparing two results

    @classmethod
    def click_loc(cls, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print "Image clicked at point:"
            print (x, y)
            StarFinder.recent_xy = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            pass


def main():
    finder = StarFinder(sys.argv[1])
    print finder.run()
    finder2 = StarFinder(sys.argv[1], prev_starfinder=finder)
    print finder2.run()


if __name__ == '__main__':
    main()
