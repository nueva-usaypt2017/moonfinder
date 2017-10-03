from circle import CircleFinder
import cv2
import sys
import os

"""
Code takes in a directory of images of the moon and outputs data on moon angular size. pixel to angle conversion coming up
"""

class MoonSize():
	def __init__(self, img_paths):
		self.img_paths = img_paths
		self.n = len(self.img_paths)
		print "self.n: " + str(self.n)
		self.radii = []

	def run(self):
		self.radii = []
		for path in self.img_paths:
			try:
				self.radii.append(CircleFinder(path).get_center_coords()[2])
			except TypeError:
				print "Moon not identified at path " + path
				self.radii.append(None)
		self.radii = [MoonSize.pix_to_ang(radius) for radius in self.radii]
		for i in range(self.n):
			print "Moon No. " + str(i) + " (path " + str(self.img_paths[i]) + ")"
			print "Radius: " + str(self.radii[i])

	def show_circle(self, index):
		finder = CircleFinder(self.img_paths[index])
		finder.get_center_coords()
		finder.show_circle()

	@classmethod
	def pix_to_ang(cls, pixels):
		return pixels

if __name__ == "__main__":
	location = sys.argv[1]
	if os.path.isdir(location):
		paths = [location + "/" + path for path in os.listdir(location)]
	elif os.path.isfile(location):
		paths = [location]
	else:
		raise ValueError("Incorrect file path supplied")

	mnsize = MoonSize(paths)
	mnsize.run()
	mnsize.show_circle(0)