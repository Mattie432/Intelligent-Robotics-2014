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
            #movebase_client(23.114, 9.253,-0.369, 0.929)
            roamPoint = roamPoint + 1
        if(foundPerson == False and roamPoint == 2):
            #movebase_client(27.4,12.4,0.918, -0.397)
            roamPoint = roamPoint + 1
        if(foundPerson == False and roamPoint == 3):
            #movebase_client(23.114, 9.253,0.935, 0.354)
            roamPoint = roamPoint + 1
        if(foundPerson == False and roamPoint == 4):
            #movebase_client(19.4,2.9,0.36,0.93)
            roamPoint = roamPoint + 1
        if(foundPerson == False and roamPoint == 5):
            #movebase_client(23.114, 9.253,0.935, 0.354)
            roamPoint = roamPoint + 1
        if(foundPerson == False and roamPoint == 6):
            movebase_client(8.001, 23.693,-0.369, 0.929)
        if(foundPerson == False and roamPoint == 7):
            movebase_client(11.7,27.1,0.918, -0.397)
        if(foundPerson == False and roamPoint == 8):
            movebase_client(8.001, 23.693,-0.369, 0.929)
        if(foundPerson == False and roamPoint == 9):
            movebase_client(2.5,18.4,0.36,0.93)
        if(foundPerson == False and roamPoint == 10):
            movebase_client(8.001, 23.693,-0.369, 0.929)
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
        roamLegsDetected = roamLegsDetected + len(item.poses)

    #check every 1000 cycles
    if(legCount % 100000 == 0):
        print "calc avg = "
        avg = float(roamLegsDetected)/legCount
        roamLegsDetected = 0
        legCount = 0
        print avg

        if(avg > 1.0):
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
                if(localPoint < 6 and localPoint > 0):
                    movebase_client(23.114, 9.253,-0.369, 0.929)
                elif(localpoint > 5 and localPoint < 11):
                    movebase_client(8.001, 23.693,-0.369, 0.929)
                    
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
    if(roamPoint == 10):
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
        detectedLegs = detectedLegs + len(item.poses)

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
    if(avg > 1.0):
        return askForInput(15)
    else:
        return False

def searchRooms():
    global chosenRoomX;
    global chosenRoomY;
    global chosenRoomOz;
    global chosenRoomOy;

    global topRoomX
    global topRoomY
    global topRoomOz 
    global topRoomOy
    global bottomRoomX
    global bottomRoomY
    global bottomRoomO
    global bottomRoomOy
    #Drive to the bottom room
    result = movebase_client(bottomRoomX, bottomRoomY,bottomRoomOz,bottomRoomOy)
    #check if room empty
    personInRoom = checkRoom()
    if (personInRoom == False):
        chosenRoomX = bottomRoomX
        chosenRoomY = bottomRoomY
        chosenRoomOz = bottomRoomOz
        chosenRoomOy = bottomRoomOy
        print("this  is the chosen room - bottom room")
        speak("Found an empty Room")
        movebase_client(20.974, 10.563, -0.311, 0.950)
        return True        
    movebase_client(20.974, 10.563, -0.311, 0.950)


    #drive to the top room
    result = movebase_client(topRoomX, topRoomY, topRoomOz,topRoomOy)
    #check if empty
    personInRoom = checkRoom()
    if (personInRoom == False):
        chosenRoomX = topRoomX
        chosenRoomY = topRoomY
        chosenRoomOz = topRoomOz
        chosenRoomOy = topRoomOy
        print("this  is the chosen room - top room")
        speak("Found an empty room")
        movebase_client(15.400, 16.362, 0.400, 0.916)
        return True
    movebase_client(15.400, 16.362, 0.400, 0.916)

    return False


if __name__ == '__main__':
    try:
        global client
        global roamLegsDetected
        roamLegsDetected = 0
        global legCount
        legCount = 0
        global roamPoint
        roamPoint = -1
        rospy.init_node('simple_nav_goal')
        

        #X & Y Coordinates of the rooms
        global bottomRoomX
        global bottomRoomY
        global bottomRoomO
        global bottomRoomOy
        bottomRoomX = 18.522
        bottomRoomY = 10.547
        bottomRoomOz =  0.93
        bottomRoomOy =  0.36

        global topRoomX
        global topRoomY
        global topRoomOz 
        global topRoomOy
        topRoomX = 15.7
        topRoomY = 16.3
        topRoomOz = 0.99 
        topRoomOy = -0.06

        global chosenRoomX;
        global chosenRoomY;
        global chosenRoomOz;
        global chosenRoomOy;
        foundPerson = False
        
        #TESTING
        #chosenRoomX = topRoomX
        #chosenRoomY = topRoomY
        #chosenRoomOz = topRoomOz
        #chosenRoomOy = topRoomOy
        #roam()
        #print "Finished roam"
        #roam()
        #rospy.spin()

        #navigate to the two co66ordinates to localize
        result = movebase_client(22.972, 9.280,0.939, 0.344)
        result = movebase_client(27.322, 12.271, 0.930, -0.368)
        
        foundEmptyRoom = False
        while(foundEmptyRoom == False):
            print "looping empty room check"
            foundEmptyRoom = searchRooms()

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
