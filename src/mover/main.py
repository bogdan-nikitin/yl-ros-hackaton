#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class MoverClass(object):
    def __init__(self):
        rospy.init_node("mover_node")
        self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_cb)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.vel = Twist()
        rospy.spin()

    def ros_publisher(self):
        self.pub.publish(self.vel)


MoverClass()
