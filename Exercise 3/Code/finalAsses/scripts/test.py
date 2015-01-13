#! /usr/bin/env python
# -*- coding: utf-8 -*- #


#---- imports ----#
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


"""
Intelligent Robotics 2014/15
Exercise 1, Part 2, 'Let's go for a walk'
Alex Bor, Laurence Stokes, Robert Minford, Matthew Flint
"""


#------Main Method definitions------#

def median(lst):
	'Method to find the arithmetic median of a list passed in as the explicit parameter'
	sortedList = sorted(lst)
	lstLen = len(lst)

	index = (lstLen-1) // 2

	if (lstLen % 2):
		return sortedList[index]
	else:
		return (sortedList[index] + sortedList[index + 1])/2.0


def callback( sensor_data ):
	'Callback method that executes on retrieving sensor data from the Pioneer'

	base_data = Twist()
	#print len(list(sensor_data.ranges))
	
	stop = False
	index = 0

	#Segments to break the periphal environment into
	farRight = [] 
	right = []
	middle = []
	middleLeft = []
	middleRight = []
	left = []
	farLeft =[]
	
	#iterating over all the values in the sensor data
	for value in list(sensor_data.ranges):	

		if value < 0.3:			
			stop = True
		
		if index < 100:
			farRight.append(value)
		elif index < 200:
			right.append(value)


		elif index < 233:
			
			middleLeft.append(value)
		elif index < 267:
			
			middle.append(value)
		elif index < 300:
			
			middleRight.append(value)

		elif index < 400:
			left.append(value)
		else:
			farLeft.append(value)
	 
	
		index = index+1		

	#print median(list1), median(list2), median(list3)
	
	#if(median(list1) < 1 and median(list2) < 1 and median(list3) < 1):
		#base_data.andular.z = 0.5

	if median(middle) < 1:
		base_data.angular.z = -0.5	
	elif median(farRight) < 1:
		base_data.angular.z = 0.5	
	
	elif median(right) < 1:		
		base_data.angular.z = 0.5
	elif median(middleRight) < 1:		
		base_data.angular.z = 0.5

	

	elif median(middleLeft) <1	:
		base_data.angular.z = - 0.5

	elif median(left) < 1:
		base_data.angular.z = -0.5
	elif median(farLeft) < 1:
		base_data.angular.z = -0.5
	if stop:
		base_data.linear.x = 0;	
	else:		
		base_data.linear.x = 0.3	

	
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
