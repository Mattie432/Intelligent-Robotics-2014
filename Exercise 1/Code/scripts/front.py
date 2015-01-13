#! /usr/bin/env python
# -*- coding: utf-8 -*- #


#---- imports ----#
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time


"""
Intelligent Robotics 2014/15
Exercise 1, Part 1 (c)
Alex Bor, Laurence Stokes, Robert Minford, Matthew Flint
"""

	
#-------------- Main Method-------------#
def main():
    try:
		rospy.init_node('simple_mover_node')


		#make pub a global variable
		global pub
		pub = rospy.Publisher('cmd_vel',Twist)

		base_data = Twist()

		end = time.time()
		start = time.time()
		while (end-start) < 20:
			end = time.time()
			print "im heere" + str(end-start)
	
			base_data.linear.x = 0.05
			pub.publish(base_data)

		base_data.linear.x = 0.0
		pub.publish(base_data)

		start = time.time()
		end = time.time()
		while (end-start) < 12:
			end = time.time()
			print "elapsed time " + str(end-start)
			base_data.linear.x = 0.25
			pub.publish(base_data)
		print "ending"
		base_data.linear.x = 0
		pub.publish(base_data)



    except KeyboardInterrupt:
        raise KeyboardInterruptError()
    except SystemExit:
        sys.exit(1)
    

if __name__ == "__main__":
    main()

'''
#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def callback( sensor_data ):
	base_data = Twist()
	#print len(list(sensor_data.ranges))
	
	stop = False
	for value in list(sensor_data.ranges):
		#index = 0
		if value < 0.3:			
			stop = True

	if stop:
		base_data.linear.x = 0;	
	else:		
		base_data.linear.x = 2	

	pub.publish(base_data)
	
if __name__ == '__main__': 
	rospy.init_node('simple_mover_node')
	rospy.Subscriber('base_scan',LaserScan, callback)
	pub = rospy.Publisher('cmd_vel',Twist)
	rospy.spin()
'''

