#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello
import time
import cv2

def main():
	cascPath = 'haarcascade_frontalface_alt.xml'
	faceCascade = cv2.CascadeClassifier(cascPath)
	drone = tello.Tello('', 8889, command_timeout=.01)  

	current_time = time.time()
	pre_time = current_time	
	time.sleep(0.5)	
	cnt_frame = 0
	pre_faces = []
	flag = 0
	cv2.waitKey(0)
	try:
		while True:
			frame = drone.read()
			if frame is None or frame.size == 0:
				continue

			image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			small_image = cv2.resize(image, dsize=(480,360) )
			cv_image = small_image
			if cnt_frame >= 5:
				gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)
				gray = cv2.equalizeHist( gray )
				faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))
				pre_faces = faces
				cnt_frame = 0
			if len(pre_faces) == 0:
				pass
			else:
				for (x, y, w, h) in pre_faces:
					cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
				x = pre_faces[0][0]
				y = pre_faces[0][1]
				w = pre_faces[0][2]
				h = pre_faces[0][3]
				cx = int( x + w/2 )
				cy = int( y + h/2 )
				if flag == 1:
					a = b = c = d = 0
					dx = 0.4 * (240 - cx)
					dy = 0.4 * (180 - cy)
					dw = 0.8 * (100 - w)
					dx = -dx
					print('dx=%f  dy=%f  dw=%f'%(dx, dy, dw) )
					d = 0.0 if abs(dx) < 20.0 else dx
					d =  100 if d >  100.0 else d
					d = -100 if d < -100.0 else d
					b = 0.0 if abs(dw) < 10.0 else dw
					b =  100 if b >  100.0 else b
					b = -100 if b < -100.0 else b
					c = 0.0 if abs(dy) < 30.0 else dy
					c =  100 if c >  100.0 else c
					c = -100 if c < -100.0 else c
					drone.send_command('rc %s %s %s %s'%(int(a), int(b), int(c), int(d)) )
			cnt_frame += 1
			cv2.imshow('OpenCV Window', cv_image)
			key = cv2.waitKey(1)
			if key == 27:
				break
			elif key == ord('t'):
				drone.takeoff()
			elif key == ord('l'):
				flag = 0
				drone.send_command('rc 0 0 0 0')
				drone.land()
				time.sleep(3)
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
				drone.send_command('rc 0 0 0 0')
			current_time = time.time()
			if current_time - pre_time > 5.0 :
				drone.send_command('command')
				pre_time = current_time

	except( KeyboardInterrupt, SystemExit):
		print( "SIGINTを検知" )

	drone.send_command('streamoff')
	del drone

if __name__ == "__main__":
	main()