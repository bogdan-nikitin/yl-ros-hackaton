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
        # дистанции, которые надо держать при движении вперёд и ключ к ним
        self.dist_x = 0
        self.distanses_x = [0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4]
        # скорости
        self.lin = 0.1
        self.ang = 0.1
        # ключ скана
        self.scan_key
        rospy.spin()

    def scan_cb(self, msg):
        # правый, левый и луч нормали
        self.r_ray = msg.ranges[(10, 275)[self.scan_key]]
        self.l_ray = msg.ranges[(355, 265)[self.scan_key]]
        self.dist_to_wall = msg.ranges[(0, 270)[self.scan_key]]
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
        elif self.dist_to_wall < self.dintanses_x[self.dist_x] + 0.072:
            # стоим-ждём
            self.velocity.linear.x = 0
            self.velocity.angular.z = 0
            self.dist_x += 1
            self.scan_key = 1 - self.scan_key
            press_to_start = input()
        else:
            self.velocity.linear.x = self.lin
        self.ros_publisher()

    def turner(self):
        # поворачиваемс до состония, параллельного стене
        # ещё не учёл растоние
        if self.r_ray == self.l_ray:
            # стоим-ждём
            self.velocity.linear.x = 0
            self.velocity.angular.z = 0
            self.scan_key = 1 - self.scan_key
            press_to_start = input()
        elif self.r_ray < self.l_ray:
            self.velocity.angular.z = self.ang
        elif self.r_ray > self.l_ray:
            self.velocity.angular.z = -self.ang
         self.pub.publish(self.velocity)

TurtleMoverClass()
