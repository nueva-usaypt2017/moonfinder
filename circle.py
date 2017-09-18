import cv2
import numpy as np
import sys

class CircleFinder():
	def __init__(self, image_path):
		self.image_path = image_path
	def get_center_coords(self):
		img = cv2.imread(self.image_path,0)
		img = cv2.medianBlur(img,5)
		cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
		circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=60,param2=30,minRadius=5,maxRadius=300)
		if circles is None:
			return None
		circles = np.uint16(np.around(circles))
		max_index = 0
		for ii, i in enumerate(circles[0,:]):
			if i[2] > circles[0,max_index,2]: #find largest one
				max_index = ii
		return circles[0,max_index,1] # x, y, radius

if __name__ == '__main__':
	cf = CircleFinder(sys.argv[1])
	print cf.get_center_coords()