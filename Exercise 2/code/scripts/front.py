#! /usr/bin/env python
# -*- coding: utf-8 -*- #


#---- imports ----#
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


"""
Intelligent Robotics 2014/15
Exercise 1, Part 1 (c)
Alex Bor, Laurence Stokes, Robert Minford, Matthew Flint
"""


#------Main Method definitions------#

def callback( sensor_data ):
	'Callback method that executes on retrieving sensor data from the Pioneer'
	base_data = Twist()

	middle =  len(list(sensor_data.ranges))/2

	print list(sensor_data.ranges).index(middle) 
	
	
	
	#publish the data back to the Robot to execute
	pub.publish(base_data)

	
#-------------- Main Method-------------#
def main():
    try:
		rospy.init_node('simple_mover_node')
		rospy.Subscriber('base_scan',LaserScan, callback)

		#make pub a global variable
		global pub 
		pub = rospy.Publisher('cmd_vel',Twist)

		rospy.spin()
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

