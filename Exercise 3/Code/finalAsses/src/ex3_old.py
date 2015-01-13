#!/usr/bin/env python

import roslib
import sys
import os
from math import *
import termios
from select import select
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, PoseArray, Quaternion
import actionlib
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def roam():
    global legDetec
    global foundPerson
    foundPerson = False
    global legCount
    global roamPoint
    legCount = 0
    roamPoint = 1
    legDetec = rospy.Subscriber("leg_detector_topic", PoseArray, roamLegDetector)

    #while looking for a person goto 4 corners of area
    while(foundPerson == False):
        if(foundPerson == False and roamPoint == 1):
            movebase_client(27.4,12.4,0.918, -0.397)
        if(foundPerson == False and roamPoint == 2):
            movebase_client(19.4,2.9,0.36,0.93)
        if(foundPerson == False and roamPoint == 3):
            movebase_client(11.7,27.1,0.918, -0.397)
        if(foundPerson == False and roamPoint == 4):
            movebase_client(2.5,18.4,0.36,0.93)
        if(roamPoint == -2):
            break

    legDetec.unregister()
    print "Ended roam loop"

    #return to empty room
    global chosenRoomX;
    global chosenRoomY;
    global chosenRoomOz;
    global chosenRoomOy;
    movebase_client(chosenRoomX,chosenRoomY,chosenRoomOz,chosenRoomOy)
    
    speak("Enjoy your meeting")
    
    

def cancelGoal():
    global client
    client.cancel_goal()
    print "Cancelled goal"


def roamLegDetector(item):
    global legCount
    global legDetec
    global roamLegsDetected
    legCount = legCount + 1

    if(len(item.poses) > 0):
        #Possibly detected a leg
        print "Seen a potential leg"
        roamLegsDetected = roamLegsDetected + 1

    #check every 1000 cycles
    if(legCount % 200000 == 0):
        print "calc avg = "
        avg = float(roamLegsDetected)/legCount
        roamLegsDetected = 0
        legCount = 0
        print avg

        if(avg > 0.0):
            print "Checking if seen a person.."
            global roamPoint
            localPoint = roamPoint
            roamPoint = -1

            legDetec.unregister()
            cancelGoal()
            
            result = False
            result = askForInput(5)
            print "Result from input = "
            print result
            if(result):
                global foundPerson
                foundPerson = True
                #legDetec.unregister()
                #cancelGoal()
                print "found person"
                roamPoint = -2
            else:
                print "resending goal"
                legCount = 0
                legDetec = rospy.Subscriber("leg_detector_topic", PoseArray, roamLegDetector)
                global prevMoveX
                global prevMoveY
                global prevMoveOz
                global prevMoveOy
                roamPoint = localPoint
                cancelGoal()
                #movebase_client(prevMoveX, prevMoveY,prevMoveOz,preMoveOy)




def movebase_client(x, y,oz,oy):
    global prevMoveX
    global prevMoveY
    global prevMoveOz
    global prevMoveOy
    prevMoveX = x
    prevMoveY = y
    prevMoveOz = oz
    prevMoveOy = oy

    global client
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    rospy.loginfo('got server')
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = oz
    goal.target_pose.pose.orientation.w = oy
    client.send_goal(goal)
    rospy.loginfo('sent goal')
    rospy.loginfo(goal)
    client.wait_for_result()
    
    print "Increase roamPoint"    
    global roamPoint
    if(roamPoint == 4):
        roamPoint = 1
    else:
        roamPoint = roamPoint + 1

    return client.get_result()



def speak(text):
    return os.system("espeak -ven+f3 -k5 -s150 " + '"' + text + '"' + " 2>/dev/null" )

def roomLegDetection(item):
    global detectedLegs
    global roomLegCount

    roomLegCount = roomLegCount + 1
    if(len(item.poses) > 0):
        detectedLegs = detectedLegs + 1

def askForInput(timeout):
    speak("I think someone is there")
    print "Press the ENTER key to be taken to a meeting room."
    sys.stdout.flush()
    sys.stdin.flush()

    termios.tcflush(sys.stdin, termios.TCIFLUSH)

    rlist = False
    rlist, wlist, xlist = select([sys.stdin],[],[],timeout)
    if rlist:
        print "Hello human!"
        return True
    else:
        print "Timed out..."
        return False
    
def checkRoom():
    print "Checking the room for occupants"
    global roomLegCount
    global roomDetec
    global detectedLegs
    roomLegCount = 0
    global foundPerson
    detectedLegs = 0
    roomDetec = rospy.Subscriber("leg_detector_topic", PoseArray, roomLegDetection)
    
    while(roomLegCount < 100000):
        print roomLegCount
    
    roomDetec.unregister()
    
    avg = float(detectedLegs)/roomLegCount
    print "Detected legs, num of scans, avg"
    print detectedLegs
    print roomLegCount
    print avg
    if(avg > 0.8):
        return askForInput(10)
    else:
        return False
    
if __name__ == '__main__':
    try:
        global client
        global roamLegsDetected
        roamLegsDetected = 0
        global legCount
        legCount = 0
        rospy.init_node('simple_nav_goal')
        

        #X & Y Coordinates of the rooms
        topRoomX = 19.5
        topRoomY = 10.7
        topRoomOz =  1.00
        topRoomOy =  0.02

        bottomRoomX = 15.7
        bottomRoomY = 16.3
        bottomRoomOz = 0.99 
        bottomRoomOy = -0.06

        global chosenRoomX;
        global chosenRoomY;
        global chosenRoomOz;
        global chosenRoomOy;
        foundPerson = False
        
        #TESTING
        chosenRoomX = topRoomX
        chosenRoomY = topRoomY
        chosenRoomOz = topRoomOz
        chosenRoomOy = topRoomOy
        roam()
        print "Finished roam"
        roam()
        rospy.spin()

        #navigate to the two co66ordinates to localize
        #result = movebase_client(23.1, 9.6,0.16,0.98)
        #result = movebase_client(20.4, 4.4, 0.49, 0.86)
        
        #Drive to the top room
        #result = movebase_client(topRoomX, topRoomY, topRoomOz,topRoomOy)

        emptyRoom = checkRoom()
        if (emptyRoom == False):
            #drive to the bottom room
            result = movebase_client(bottomRoomX, bottomRoomY,bottomRoomOz,bottomRoomOy)
            chosenRoomX = bottomRoomX
            chosenRoomY = bottomRoomY
            chosenRoomOz = bottomRoomOz
            chosenRoomOy = bottomRoomOy
            print("this  is the chosen room 2")
            speak("Found an empty romovebase_clientom")
        else:
            chosenRoomX = topRoomX
            chosenRoomY = topRoomY
            chosenRoomOz = topRoomOz
            chosenRoomOy = topRoomOy
            print("this  is the chosen room 1")
            speak("Found an empty room")
        
        #roam about looking for people
        print "1st roam"
        roam()
        print "2nd roam"
        roam()
        print "3rd roam"
        roam()
        print "4th roam"
        roam()


    except rospy.ROSInterruptException:
        print "interrupted"
