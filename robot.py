#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class TurtleMoverClass(object):

    def __init__(self):
        rospy.init_node("wild_west_python_node")
        self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_cb)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.velocity = Twist()
        # дистанции, которые надо держать при движении вперёд и ключ к ним
        self.dist_x = 0
        self.distanses_x = [0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2]
        # скорости
        self.lin = 0.06
        self.ang = 0.06
        # ключ скана
        self.scan_key = 0

        self.l_ray = self.r_ray = 0
        self.dist_to_wall = 0

        rospy.spin()

    def scan_cb(self, msg):
        # правый, левый и луч нормали
        self.r_ray = msg.ranges[(5, 45)[self.scan_key]]
        self.l_ray = msg.ranges[(355, 135)[self.scan_key]]
        self.dist_to_wall = msg.ranges[(0, 90)[self.scan_key]]
        # вызываем движение
        if self.scan_key:
            self.turner()
        else:
            self.mover()

    def ros_publisher(self):
        self.pub.publish(self.velocity)

    def mover(self):
        # проверка отклонение и фикс направления
        if self.r_ray == self.l_ray:
            self.velocity.angular.z = 0
        elif self.r_ray < self.l_ray:
            self.velocity.angular.z = self.ang
        elif self.r_ray > self.l_ray:
            self.velocity.angular.z = -self.ang

        # русские вперёд!    
        if self.dist_to_wall == float('inf'):
            pass
        elif self.dist_to_wall < self.distanses_x[self.dist_x] + 0.072:
            # стоим-ждём
            self.velocity.linear.x = 0
            self.velocity.angular.z = 0
            press_to_start = input()
            rospy.loginfo('stop')
            if self.dist_x != 1:
                self.scan_key = 1
                return
            self.dist_x += 1
        else:
            self.velocity.linear.x = self.lin
        self.ros_publisher()

    def turner(self):
        # поворачиваемся до состония, параллельного стене
        # ещё не учёл растоние
        if (self.r_ray == self.l_ray
                and abs(self.r_ray * math.cos(math.pi / 4) - self.dist_to_wall) <= 0.0001):
            # стоим-ждём
            self.velocity.linear.x = 0
            self.velocity.angular.z = 0
            press_to_start = input()
            self.scan_key = 0
            rospy.loginfo('turned')
            return
        else:
            self.velocity.angular.z = -self.ang * 2
        self.ros_publisher()


    def stabilize(self):
        self.r_ray = msg.ranges[5]
        self.l_ray = msg.ranges[355]
        if self.r_ray == self.l_ray:
            return
        elif self.r_ray < self.l_ray:
            self.velocity.angular.z = self.ang
        elif self.r_ray > self.l_ray:
            self.velocity.angular.z = -self.ang
        self.ros_publisher()


TurtleMoverClass()
