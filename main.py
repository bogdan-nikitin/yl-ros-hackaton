#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class TurtleMoverClass(object):
    def __init__(self):
        rospy.init_node("wild_west_node")
        self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_cb)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.vel = Twist()
        rospy.spin()
    
    def ros_publisher(self):
        self.pub.publish(self.vel)

TurtleMoverClass()
