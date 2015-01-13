#-------------- Imports -------------#

from geometry_msgs.msg import Pose, PoseArray, Quaternion
from pf_base import PFLocaliserBase
import math
import rospy
from util import rotateQuaternion, getHeading
import random
from time import time


#-------------- PFLocaliser Class Methods-------------#

class PFLocaliser(PFLocaliserBase):

	#constructor
	def __init__(self):

		#Call the superclass constructor
		super(PFLocaliser, self).__init__()

		#Set motion model parameters
		self.ODOM_ROTATION_NOISE = 0
		self.ODOM_TRANSLATION_NOISE = 0
		self.ODOM_DRIFT_NOISE = 0

		#Sensor model readings
		self.NUMBER_PREDICTED_READINGS = 20 
		
    
	def initialise_particle_cloud(self, initialpose):
        #Set particle cloud to initialpose plus noise

		partNumber = 30
		noise = 1

		#create an array of Poses
		posArray = PoseArray()

		#iterate over the number of particles and append to PosArray
		for x in range(0, partNumber): 
			pose = Pose()

			pose.position.x =  random.uniform((initialpose.pose.pose.position.x) - noise, 	initialpose.pose.pose.position.x + noise)
			pose.position.y = random.uniform(initialpose.pose.pose.position.y - noise, 		initialpose.pose.pose.position.y +noise)
			pose.position.z = 0

			pose.orientation = rotateQuaternion(initialpose.pose.pose.orientation, math.radians(random.uniform(0,360)))

			posArray.poses.append(pose)
			
		#print posArray
		return posArray



    
	def update_particle_cloud(self, scan):
		'''method called wenever a new LaserScan message
		   is recieved. Does the particle filtering'''
		
		print("Running update_particle_cloud")

		#list of poses
		sum_weights = 0
		cumulative_sum_list = [] 
		segment_list = []
		sum_count = 0
		y=0

		pcloud = self.particlecloud.poses

		for particle in pcloud:
			particleWeight = self.sensor_model.get_weight(scan, particle)
			sum_weights+= particleWeight

			#print particleWeight

		print sum_weights

		for particle in pcloud:
			particleWeight = self.sensor_model.get_weight(scan, particle)
			segment_list.extend([(particleWeight/(sum_weights))])
			
		#print segment_list


		for x in segment_list:
			sum_count+=x
			cumulative_sum_list.extend([sum_count])	
		    

		#print cumulative_sum_list
		
		#new pose array to replace partical cloud
		newParticleCloud = PoseArray()

		for particle in pcloud:
			rand = random.uniform(0,1)
			segment_count = 0  
			output = 0
			count = 0
			for x in cumulative_sum_list:
				count += 1
				print "I got to position " 
				
				if rand <= x:
					print count
					output = segment_count
					break
				segment_count+=1
			newParticleCloud.poses.append(pcloud[output])
		
		#the weighting of the particle at the segment_list we 			
		#are in. Higher weighted particles have bigger segments
	    #and so are more likely to be output

		
		print segment_list[output]
				

		return newParticleCloud


	def estimate_pose(self):
		'Method to estimate the pose'
		
		
			
		'''Create new estimated pose, given particle cloud
		# E.g. just average the location and orientation values of each of
		# the particles and return this.

		# Better approximations could be made by doing some simple clustering,
		# e.g. taking the average location of half the particles after 
		# throwing away any which are outlier'''

		
		#declare some variables 'yo
		x,y,z,orix,oriy,oriz,oriw,count = 0,0,0,0,0,0,0,0
		
		#iterate over each particle extracting the relevant
		#averages
		for particle in self.particlecloud.poses:
			x += particle.position.x
			y += particle.position.y
			z += particle.position.z
			orix += particle.orientation.x
			oriy += particle.orientation.y
			oriz += particle.orientation.z
			oriw += particle.orientation.w
			
			count+=1

		#create a new pose with the averages of the location and 			#orientation values of the particles
		pose = Pose()
		
		pose.position.x = x/count
		pose.position.y = y/count
		pose.position.z = z/count

		pose.orientation.x = orix/count
		pose.orientation.y = oriy/count
		pose.orientation.z = oriz/count
		pose.orientation.w = oriw/count

		#print(pose)
		return pose


"""
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
"""
