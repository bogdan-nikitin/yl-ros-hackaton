#!/usr/bin/env python
#-*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class TurtleMoverClass(object):

    def __init__(self):
        rospy.init_node("wild_west_python_node")
        self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_cb)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.velocity = Twist()
        rospy.spin()

    def scan_front(self, msg):
        print(msg.ranges[0])
        self.r_ray = msg.ranges[10]
        self.l_ray = msg.ranges[350]
        self.dist_to_wall = msg.ranges[0]
        self.mover()

    def scan_side(self, msg):
        print(msg.ranges[0])
        self.r_ray = msg.ranges[280]
        self.l_ray = msg.ranges[260]
        self.dist_to_wall = msg.ranges[270]
        self.turner()

    def ros_publisher(self):
        self.pub.publish(self.velocity)

    def mover(self):
        if self.dist_to_wall == float('inf'):
            pass
        elif self.dist_to_wall < 0.37:
            self.velocity.linear.x = 0
            rospy.loginfo("OMG I'LL HIT THE WALL")
        else:
            self.velocity.linear.x = 0.1
            rospy.loginfo("GO")
        self.ros_publisher()

TurtleMoverClass()
