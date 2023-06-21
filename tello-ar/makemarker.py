#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import utils import AR
# ArUcoのライブラリを導入
aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
aruco
def main():
	for i in range(10):
		ar_image = aruco.drawMarker(dictionary, i, 150)
		fileName = "ar" + str(i).zfill(2) + ".png"
		cv2.imwrite(fileName, ar_image)
  
if __name__ == "__main__":
	main()