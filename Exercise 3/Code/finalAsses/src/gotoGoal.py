#!/usr/bin/env python

import roslib

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib




def movebase_client(x, y):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    rospy.loginfo('got server')
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "odom"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 0.5
    client.send_goal(goal)
    rospy.loginfo('sent goal')
    rospy.loginfo(goal)
    client.wait_for_result()
    return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('simple_nav_goal')
        result = movebase_client(2, 2)
        print result
    except rospy.ROSInterruptException:
        print "interrupted"
