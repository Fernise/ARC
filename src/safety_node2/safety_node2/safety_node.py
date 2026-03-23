#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import numpy as np
# TODO: include needed ROS msg type headers and libraries
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from std_srvs.srv import Trigger


class SafetyNode(Node):
    """
    The class that handles emergency braking.
    """
    def __init__(self):
        super().__init__('safety_node')
        """
        One publisher should publish to the /drive_out topic with a AckermannDriveStamped drive message.

        You should also subscribe to the /scan topic to get the LaserScan messages and
        the /odom topic to get the current speed of the vehicle,
        and to /drive_in to get the drive commands.

        The subscribers should use the provided odom_callback and scan_callback as callback methods

        NOTE that the x component of the linear velocity in odom is the speed
        """
        self.speed = 0.
        # TODO: create ROS subscribers and publishers.
        self.ttc_threshold = 0.5
        self.last_drive_msg = AckermannDriveStamped()
        self.brake_engaged = False
        self.min_ttc = np.inf

        # Suscribers
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.create_subscription(AckermannDriveStamped, '/drive_in', self.drive_callback, 10)


        # Publisher
        self.drive_out_pub = self.create_publisher(AckermannDriveStamped, '/drive_out', 10)
        self.reset_srv = self.create_service(Trigger, '/reset_safety_node', self.reset_callback)

    def odom_callback(self, odom_msg):
        # TODO: update current speed
        # x component of the linear velocity in odom is the speed
        self.speed = odom_msg.twist.twist.linear.x

    def scan_callback(self, scan_msg):
        # TODO: calculate TTC
        self.min_ttc = np.inf
        v = self.last_drive_msg.drive.speed

        for i, r in enumerate(scan_msg.ranges):
            if not np.isfinite(r):
                continue

            angle = scan_msg.angle_min + i * scan_msg.angle_increment
            range_rate = v * np.cos(angle)

            if range_rate > 0:
                ttc = r / range_rate
                self.min_ttc = min(self.min_ttc, ttc)


        # TODO: publish command to brake
        if self.min_ttc < self.ttc_threshold:
            self.brake_engaged = True
            brake_msg = AckermannDriveStamped()
            brake_msg.drive.speed = 0.0
            self.drive_out_pub.publish(brake_msg)
        else:
            self.drive_out_pub.publish(self.last_drive_msg)


    def drive_callback(self, drive_msg):
        self.last_drive_msg = drive_msg

        if self.brake_engaged:
            brake_msg = AckermannDriveStamped()
            brake_msg.drive.speed = 0.0
            self.drive_out_pub.publish(brake_msg)
        else:
            self.drive_out_pub.publish(drive_msg)


    def reset_callback(self, request, response):
        if self.min_ttc < self.ttc_threshold:
            response.success = False
            response.message = 'Reset failed: TTC still below threshold.'
        else:
            self.brake_engaged = False
            response.success = True
            response.message = 'Safety node reset successful.'
        return response


def main(args=None):
    rclpy.init(args=args)
    safety_node = SafetyNode()
    rclpy.spin(safety_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    safety_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
