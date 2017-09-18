from circle import CircleFinder
import cv2
import sys

img = cv2.imread(sys.argv[1],0)
cf = CircleFinder(sys.argv[1])
circle_coords = cf.get_center_coords()
cv2.circle(img,(circle_coords[0],circle_coords[1]),circle_coords[2],(0,255,0),2)
cv2.circle(img,(circle_coords[0],circle_coords[1]),3,(255,0,0),2)

while True:
	cv2.imshow('stardistance',img)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cv2.destroyAllWindows()
