#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

from constants import *
from compare import *


class MoverClass(object):
    def __init__(self):
        rospy.init_node("mover_node")
        self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_cb)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1000)
        self.vel = Twist()

        self.l_ray_front = self.r_ray_front = 0
        self.dist_to_wall_front = 0

        self.l_ray_left = self.r_ray_left = 0
        self.dist_to_wall_left = 0

        self.scan_data = []

        self.rotate_90()
        rospy.spin()

    def scan_cb(self, msg):
        self.l_ray_front = msg.ranges[LIDAR_DEGREE - DEGREE_SHIFT]
        self.r_ray_front = msg.ranges[DEGREE_FRONT + DEGREE_SHIFT]
        self.dist_to_wall_front = msg.ranges[DEGREE_FRONT]

        self.l_ray_left = msg.ranges[DEGREE_LEFT - DEGREE_SHIFT]
        self.r_ray_left = msg.ranges[DEGREE_LEFT + DEGREE_SHIFT]
        self.dist_to_wall_left = msg.ranges[DEGREE_LEFT]

        self.scan_data = msg

    def ros_publisher(self):
        self.pub.publish(self.vel)
        rospy.loginfo(self.vel)

    def rotate_90(self):
        self.vel.angular.z = 1
        self.ros_publisher()
        while True:
            rospy.loginfo('l %s r %s', self.l_ray_left, self.r_ray_left)
            if compare_with_delta(self.l_ray_left, self.r_ray_left):
                self.vel.angular = 0
                rospy.loginfo('turned')
                break
            elif self.l_ray_left > self.r_ray_left:
                self.vel.angular = -1
            elif self.r_ray_left > self.l_ray_left:
                self.vel.angular = 1
            self.ros_publisher()

    def move_to_wall(self):
        self.vel.linear.x = 0.18


MoverClass()
