#!/usr/bin/env python

#
# Copyright (c) 2018-2019 Intel Corporation
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
#
"""
Classes to handle Carla gnsss
"""

from sensor_msgs.msg import NavSatFix

from carla_ros_bridge.sensor import Sensor


class Gnss(Sensor):
    """
    Actor implementation details for gnss sensor
    """

    def __init__(self, carla_actor, parent, communication, synchronous_mode, sensor_name="GNSS"):
        """
        Constructor

        :param carla_actor: carla actor object
        :type carla_actor: carla.Actor
        :param parent: the parent of this
        :type parent: carla_ros_bridge.Parent
        :param communication: communication-handle
        :type communication: carla_ros_bridge.communication
        :param synchronous_mode: use in synchronous mode?
        :type synchronous_mode: bool
        """
        super(Gnss, self).__init__(carla_actor=carla_actor, parent=parent,
                                   communication=communication, synchronous_mode=synchronous_mode,
                                   prefix="gnss/" + carla_actor.attributes.get('role_name'),
                                   sensor_name=sensor_name)

    # pylint: disable=arguments-differ
    def sensor_data_updated(self, carla_gnss_measurement):
        """
        Function to transform a received gnss event into a ROS NavSatFix message

        :param carla_gnss_measurement: carla gnss measurement object
        :type carla_gnss_measurement: carla.GnssMeasurement
        """
        navsatfix_msg = NavSatFix()
        navsatfix_msg.header = self.get_msg_header(timestamp=carla_gnss_measurement.timestamp)
        navsatfix_msg.latitude = carla_gnss_measurement.latitude
        navsatfix_msg.longitude = carla_gnss_measurement.longitude
        navsatfix_msg.altitude = carla_gnss_measurement.altitude
        self.publish_message(self.get_topic_prefix() + "/fix", navsatfix_msg)
