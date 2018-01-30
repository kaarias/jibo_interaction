#!/usr/bin/python


import rospy
from jibo_msgs.msg import JiboAction, JiboVec3
from std_msgs.msg import Header  # standard ROS msg header



ROSCORE_TO_JIBO_TOPIC = '/jibo'


class RobotSender:

    def __init__(self):
        self.robot_commander = None

    def start_robot_publisher(self):
        """
        Starts up the robot publisher node
        """

        rospy.init_node('Jibo_Test_Node', anonymous=True)
        print('Robot Pub Node started')

        
        msgType = JiboAction
        msgTopic = ROSCORE_TO_JIBO_TOPIC

        self.robot_commander = rospy.Publisher(msgTopic, msgType, queue_size=10)
        rate = rospy.Rate(10)  # spin at 10 Hz
        rate.sleep()  # sleep to wait for subscribers


    def send_robot_motion_cmd(self, command):
        """
        send a Motion Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        
        msg.do_motion = True
        msg.do_tts = False
        msg.do_lookat = False

        msg.motion = command   

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_tts_cmd(self, text, *args):
        """
        send a Motion Command to Jibo
        """

        msg = JiboAction()    
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        
        msg.do_motion = False
        msg.do_tts = True
        msg.do_lookat = False

        msg.tts_text = text

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_lookat_cmd(self, x, y, z):
        """
        send a Motion Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        
        msg.do_motion = False
        msg.do_tts = False
        msg.do_lookat = True

        position = JiboVec3()
        position.x = x
        position.y = y
        position.z = z

        msg.look_at = position

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

    def send_robot_audio_cmd(self, audio_command):
        """
        send a Motion Command to Jibo
        """

        msg = JiboAction()
        # add header
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()

        
        msg.do_motion = False
        msg.do_tts = False
        msg.do_lookat = False
        msg.do_sound_playback = True

        msg.audio_filename = audio_command

        self.robot_commander.publish(msg)
        rospy.loginfo(msg)

