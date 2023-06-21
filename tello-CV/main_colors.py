#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello		
import time			
import cv2			

def main():
	drone = tello.Tello('', 8889, command_timeout=.01)  

	current_time = time.time()	
	pre_time = current_time		

	time.sleep(0.5)		#

	try:
		while True:
			frame = drone.read()
			if frame is None or frame.size == 0:
				continue
			image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			bgr_image = cv2.resize(image, dsize=(480,360) )

			hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

			cv2.imshow('BGR Color', bgr_image)
			cv2.imshow('HSV Color', hsv_image)

			key = cv2.waitKey(1)
			if key == 27:
				break
			elif key == ord('t'):
				drone.takeoff()
			elif key == ord('l'):
				drone.land()
			elif key == ord('w'):
				drone.move_forward(0.3)
			elif key == ord('s'):
				drone.move_backward(0.3)
			elif key == ord('a'):
				drone.move_left(0.3)
			elif key == ord('d'):
				drone.move_right(0.3)
			elif key == ord('q'):
				drone.rotate_ccw(20)
			elif key == ord('e'):
				drone.rotate_cw(20)
			elif key == ord('r'):
				drone.move_up(0.3)
			elif key == ord('f'):
				drone.move_down(0.3)

			current_time = time.time()
			if current_time - pre_time > 5.0 :
				drone.send_command('command')
				pre_time = current_time	

	except( KeyboardInterrupt, SystemExit):
		print( "stop" )
	del drone

if __name__ == "__main__":
	main()