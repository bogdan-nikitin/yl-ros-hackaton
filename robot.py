#!/usr/bin/env python
#-*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class TurtleMoverClass(object):

    def __init__(self):
        rospy.init_node("wild_west_python_node")
        self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_front)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.velocity = Twist()
        rospy.spin()
        # дистанции, которые надо держать при движении вперёд и ключ к ним
        self.dist_x = 0
        self.distanses_x = [20, 40, 20, 20, 20, 20, 40]

    def scan_front(self, msg):
        # правый, левый и луч нормали(0 градусов)
        self.r_ray = msg.ranges[10]
        self.l_ray = msg.ranges[350]
        self.dist_to_wall = msg.ranges[0]
        # вызываем движение
        self.mover()

    def scan_side(self, msg):
        # правый, левый и луч нормали(270 градусов)
        self.r_ray = msg.ranges[280]
        self.l_ray = msg.ranges[260]
        self.dist_to_wall = msg.ranges[270]
        # вызываем поворот
        self.turner()

    def ros_publisher(self):
        self.pub.publish(self.velocity)

    def mover(self):
        # проверка отклонение и фикс направления
        if self.r_ray == self.l_ray:
            self.velocity.angular.z = 0
        elif self.r_ray < self.l_ray:
            self.velocity.angular.z = 0.1
        elif self.r_ray > self.l_ray:
            self.velocity.angular.z = -0.1

        # русские вперёд!    
        if self.dist_to_wall == float('inf'):
            pass
        elif self.dist_to_wall < self.dintances_x[self.dist_x] + 7.2:
            # меняем функцию скана на сабе, стоим-ждём
            self.velocity.linear.x = 0
            self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_side)
            self.dist_x += 1
            press_to_start = input()
        else:
            self.velocity.linear.x = 0.1
        self.ros_publisher()

    def turner(self):
        # поворачиваемс до состония, параллельного стене
        # ещё не учёл растоние
        if self.r_ray == self.l_ray:
            # меняем функцию скана на сабе, стоим-ждём
            self.velocity.angular.z = 0
            self.sub = rospy.Subscriber("/scan", LaserScan, self.scan_front)
            press_to_start = input()
        elif self.r_ray < self.l_ray:
            self.velocity.angular.z = 0.1
        elif self.r_ray > self.l_ray:
            self.velocity.angular.z = -0.1
         self.pub.publish(self.velocity)

TurtleMoverClass()
