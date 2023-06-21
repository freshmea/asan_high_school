#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello
import time
import cv2
import numpy as np

def main():
	drone = tello.Tello('', 8889, command_timeout=.01)

	current_time = time.time()
	pre_time = current_time

	time.sleep(0.5)
	cv2.namedWindow("OpenCV Window")

	def nothing(x):
		pass

	cv2.createTrackbar("H_min", "OpenCV Window", 0, 179, nothing)
	cv2.createTrackbar("H_max", "OpenCV Window", 9, 179, nothing)
	cv2.createTrackbar("S_min", "OpenCV Window", 128, 255, nothing)
	cv2.createTrackbar("S_max", "OpenCV Window", 255, 255, nothing)
	cv2.createTrackbar("V_min", "OpenCV Window", 128, 255, nothing)
	cv2.createTrackbar("V_max", "OpenCV Window", 255, 255, nothing)

	flag = 0
	try:
		while True:
			frame = drone.read()
			if frame is None or frame.size == 0:
				continue 


			image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			bgr_image = cv2.resize(image, dsize=(480,360) )

			hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

			h_min = cv2.getTrackbarPos("H_min", "OpenCV Window")
			h_max = cv2.getTrackbarPos("H_max", "OpenCV Window")
			s_min = cv2.getTrackbarPos("S_min", "OpenCV Window")
			s_max = cv2.getTrackbarPos("S_max", "OpenCV Window")
			v_min = cv2.getTrackbarPos("V_min", "OpenCV Window")
			v_max = cv2.getTrackbarPos("V_max", "OpenCV Window")


			bin_image = cv2.inRange(hsv_image, (h_min, s_min, v_min), (h_max, s_max, v_max))
			masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=bin_image)

			out_image = masked_image
			num_labels, label_image, stats, center = cv2.connectedComponentsWithStats(bin_image)
			num_labels = num_labels - 1
			stats = np.delete(stats, 0, 0)
			center = np.delete(center, 0, 0)


			if num_labels >= 1:
				max_index = np.argmax(stats[:,4])

				x = stats[max_index][0]
				y = stats[max_index][1]
				w = stats[max_index][2]
				h = stats[max_index][3]
				s = stats[max_index][4]
				mx = int(center[max_index][0])
				my = int(center[max_index][1])
				#print("(x,y)=%d,%d (w,h)=%d,%d s=%d (mx,my)=%d,%d"%(x, y, w, h, s, mx, my) )

				cv2.rectangle(out_image, (x, y), (x+w, y+h), (255, 0, 255))

				#cv2.putText(out_image, "%d,%d"%(mx,my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
				cv2.putText(out_image, "%d"%(s), (x, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))

				if flag == 1:
					a = b = c = d = 0

					dx = 1.0 * (240 - mx)

					d = 0.0 if abs(dx) < 50.0 else dx

					d = -d
					d =  100 if d >  100.0 else d
					d = -100 if d < -100.0 else d

					print('dx=%f'%(dx) )
					drone.send_command('rc %s %s %s %s'%(int(a), int(b), int(c), int(d)) )

			cv2.imshow('OpenCV Window', out_image)
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
			elif key == ord('1'):
				flag = 1
			elif key == ord('2'):
				flag = 0
			current_time = time.time()
			if current_time - pre_time > 5.0 :
				drone.send_command('command')
				pre_time = current_time

	except( KeyboardInterrupt, SystemExit):
		print( "stop" )

	drone.send_command('streamoff')
	del drone

if __name__ == "__main__":
	main()