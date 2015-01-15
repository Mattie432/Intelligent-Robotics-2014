# Intelligent-Robotics-2014
Mobile robots are regularly used in many applications:
from aiding disaster recovery efforts in mines and after
earthquakes, to military uses such as roadside bomb detection.
Recently, they have even been employed to explore
the surface of Mars. This paper presents the design and
development of a Mobile Robot inspired by the AAAI Mobile
Robotics Competition, 1996: Call a Meeting, which
stressed navigation and planning. For our solution to
the competition, we present an autonomous Mobile Robot
that (a) searches for and finds an empty room (in terms of
human presence) b) detects a human in a different room c)
directs the human to the empty room. Our setup included
a Pioneer 3-DX mobile robot, a Hokuyo URG-04LX laser
sensor and a Toshiba i3 / 2GB RAM laptop. Notable features
of our solution include a behavioural-based hybrid
control architecture, ACML localization and a laser-based
leg detection system for identifying persons.

## Exercise 1
For the first exercise, your task is to write a ROS node -- or set of nodes -- to enable your robot to explore the lab (or even the foyer outside) without getting stuck.

Your robot should be able to run for as long as possible without getting trapped in any small corners or under desks, chairs, tables, etc. and without just going over the same small area of ground repeatedly. The idea is to explore! You will need to think about how your robot might know it is stuck, and what it can do to get out of such a situation.

[url](Exercise 1)


## Exercise 2
For this exercise, you will write a replacement ROS node for AMCL in python which runs a basic particle filter and localises the robot within the supplied map.

Your task for this exercise is to write a class called PFLocaliser which will extend PFLocaliserBase and provide localisation given a map, laser readings, and an initial pose estimate.


## Exercise 3
If you wish you can build a robot that solves a “call a meeting” task that we have defined the rules for. This task is similar to but not the same as the task of the same name in the AAAI 1996 Mobile Robot Competition. Your robot should operate reliably for the period of the task (about 15 minutes) without any human intervention. Interventions will result in penalty marks for the demonstration portion of the mark. The rest of this document concentrates on the assessment criteria, particularly those for the writeup. The task is to call a meeting by first finding an empty room to have a meeting in, then informing all potential meeting participants (or “conferees”) about the meeting. This can be done by a GUI on the laptop screen, or by canned speech. The task will be carried out in a mock office arena. In demonstration robots will be run individually, for 15 minutes. The whole demo including questions should take 20 mins. Potential meeting participants, or “conferees” will be standing or walking in the light well area. There will be two conferees somewhere in the arena. Once a conferee is informed of the meeting the robot should take them there.

At the beginning of the task the robot is placed at a random point in the corridor. Points will be awarded to each team as follows. Please note that these do not form a component of the demonstration mark, but instead guide you as to what the task priorities are. Thus the score you achieve will not be translated into part of the mark for the demonstration. The mark will depend on a judgement by the module lecturer as to the overall quality of the performance, and other criteria will be equally important in the demonstration mark, such as your design, the mreliability, the speed, and how well you present your work.
