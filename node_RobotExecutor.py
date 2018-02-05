#!/usr/bin/env python
import time
import rospy # ROS
from jibo_msgs.msg import JiboAction # ROS msgs to talk to Jibo
from jibo_msgs.msg import JiboState # ROS msgs to get info from Jibo
from jibo_msgs.msg import JiboVec3
from std_msgs.msg import Bool # for child_attention topic
from std_msgs.msg import Header # standard ROS msg header
from std_msgs.msg import String
from std_msgs.msg import Int32
import node_RobotExecutor_flags as nref
import string
from random import randint


'''animations = [ 
        "YES", yep_01.keys
        "AGREEMENT", greetings_08.keys
        "LAUGH", laughter_01.keys
        "NO", nope_01_01.keys
        "FRUSTRATED", frustrated_01.keys
        "SAD", sad_02.keys
        "NOD", listening_begin_02.keys
        "FLAT_AGREEMENT", listening_begin_02.keys 
        "PERKUP", perkup_01.keys
        "PUZZLED", confused_01.keys
        "SCARED", scared_sound_00.keys
        "SILENT_SAD", sad_02.keys
        "EXCITED", happy_05.keys
        "INTERESTED", interested_01.keys
        "THINKING", thinking_08.keys
        "YAWN", yawn_03.keys 
        "POSE1", body_lean_right_01_01.keys
        "POSE2", body_lean_left_01_01.keys
        "SHIMMY", seaweed_01_01.keys
        "HAPPY_DANCE", carlton_01_01.keys
        "HAPPY_WIGGLE", happy_dance_01.keys
        "POSE_SLEEPING", sleeping_idle_00_01.keys
        "SHIFT_WEIGHT1", shift_01.keys
        "SHIFT_WEIGHT2", shift_10.keys
        "SWAY", samba_01_01.keys
        "DANCE", side_shaker_01_01.keys
        "ROCKING", rocking_01.keys
        "POSE_FORWARD", pose_forward.keys
        "IDLESTILL", body_look_center_middle_01_01.keys
        "SWIPE_STAGERIGHT" swipe_stage_right_01.keys
        ]'''

flags=nref.node_RobotExecutor_flags()
BCenabled = True
ISSPEAKING_THRESHOLD = 0 # > ISSPEAKING_THRESHOLD is speaking
last_sb = 0

def send_motion_message(motion):
    """ Publish JiboAction do motion message """
    #print 'sending motion message: %s' % motion
    print 'sending motion message'
    msg = JiboAction()
    msg.do_motion = True
    msg.motion = motion
    pub_re.publish(msg)
    #rospy.loginfo(msg)

def send_lookat_message(lookat):
    """ Publish JiboAction lookat message """
    #print 'sending lookat message: %s' % lookat
    print 'sending lookat message'
    msg = JiboAction()
    msg.do_look_at = True
    msg.look_at = lookat
    pub_re.publish(msg)
    rospy.loginfo(msg)
    
def send_motion_lookat_message(motion,lookat):
    """ Publish JiboAction motion_lookat message """
    #print 'sending lookat message: %s' % lookat
    print 'sending motion_lookat message'
    msg = JiboAction()
    msg.do_look_at = True
    msg.look_at = lookat
    msg.do_motion = True
    msg.motion = motion
    pub_re.publish(msg)
    rospy.loginfo(msg)

def send_speech_message(speech):
    """ Publish JiboAction playback audio message """
    #print '\nsending speech message: %s' % speech
    print '\nsending speech message'
    msg = JiboAction()
    msg.do_sound_playback = True
    msg.wav_filename = speech
    pub_re.publish(msg)
    #rospy.loginfo(msg)
    
def send_tts_message(): #not working
    """ Publish JiboAction tts message """
    #print '\nsending speech message: %s' % speech
    print '\nsending tts message'
    msg = JiboAction()
    msg.do_text_to_speech = True
    msg.tts_text = "hello"
    pub_re.publish(msg)
    rospy.loginfo(msg)
    
def send_speech_motion_message(speech,motion):
    """ Publish JiboAction playback audio message """
    print '\nsending speech and motion message'
    msg = JiboAction()
    msg.do_sound_playback = True
    msg.wav_filename = speech
    msg.do_motion = True
    msg.motion = motion
    pub_re.publish(msg)
    #rospy.loginfo(msg)    

def onMessageReceived_rs(data): #robot state
    global flags
    # when we get jibo state messages, set a flag indicating whether the
    # robot is in motion or playing sound or not
    flags.jibo_is_playing_sound = data.is_playing_sound

    # Instead of giving us a boolean to indicate whether jibo is in motion
    # or not, we get the name of the animation. Let's check whether it is
    # our "idle" animation (usually, the idle animation is either
    # MOTION_IDLESTILL or MOTION_BREATHING).
    flags.jibo_is_doing_motion = data.doing_motion
    
    print flags
    
def onMessageReceived_bc(data):
    global BCenabled
    
    if(BCenabled == True):
        n=randint(1,5)
        '''if(isSpeaking):
            if(n==1):
                send_motion_message("NOD")
            else:
                send_motion_message("SHIFT_WEIGHT1")
        
        else:'''
        print "\n",data.data," - ",n
        if(data.data=="Wordy"):
            if(n==1):
                send_motion_message("YES")
            elif(n==2):
                send_motion_message("LAUGH")
            elif(n==3):
                send_motion_message("SILENT_CONFIRM")
            elif(n==4):
                send_motion_message("SILENT_YES")
            else:
                send_speech_message("cyber4/emotional_dialogic_hmm.wav")

        elif(data.data=="LongPause"):
            if(n==1):
                send_motion_message("AGREEMENT")
            elif(n==2):
                send_motion_message("INTERESTED")
            elif(n==3):
                send_motion_message("SILENT_LAUGH")
            elif(n==4):
                send_motion_message("SILENT_INTERESTED")
            else:
                send_speech_message("cyber4/emotional_dialogic_mmm.wav")

        elif(data.data=="Energy"):
            if(n==1):
                send_motion_message("EXCITED")
            elif(n==2):
                send_speech_message("cyber4/emotional_ending_01.wav")
            elif(n==3):
                send_motion_message("LAUGH_AGREEMENT")
            elif(n==4):
                send_motion_message("LAUGH_YES")
            else:
                send_speech_message("cyber4/emotional_dialogic_mmhm.wav")
    
def onMessageReceived_gui_re(data):
    #send_speech_motion_message("cyber4/emotional_intro_02.wav","ROCKING")
    d=data.data.split("+")
    print "\nReceived: ",d[1]
    if(d[1]=="motion"):
        send_motion_message(d[0])
    elif(d[1]=="speech"):
        send_speech_message(d[0])
    elif(d[1]=="lookat"):
        v=d[0].split(",")
        vect=Vec3(float(v[0]),float(v[1]),float(v[2]))
        send_lookat_message(vect)
    elif(d[1]=="motion&lookat"):
        ml=d[0].split("&")
        v=ml[1].split(",")
        vect=Vec3(float(v[0]),float(v[1]),float(v[2]))
        send_motion_lookat_message(ml[0],vect)
    elif(d[1]=="instr"):
        if(d[0]=="enable_BC"):
            BCenabled=True
        elif(d[0]=="disable_BC"):
            BCenabled=False
            
def onMessageReceived_sb(data):
    global last_sb
    last_sb = int(data.data)
    
def isSpeaking():
    global ISSPEAKING_THRESHOLD, last_sb
    if(last_sb>ISSPEAKING_THRESHOLD):
        return True
    return False
            
node = rospy.init_node('node_RobotExecutor', anonymous=True)
pub_re = rospy.Publisher('jibo', JiboAction, queue_size = 1)
sub_rs = rospy.Subscriber('msg_rs', JiboState, onMessageReceived_rs) #robot state
sub_bc = rospy.Subscriber('msg_bc', String, onMessageReceived_bc) #backchanneling
sub_gui_re = rospy.Subscriber('msg_gui_re', String, onMessageReceived_gui_re)
#sub_sb = rospy.Subscriber('msg_sb/raw', Int32, onMessageReceived_sb)
rospy.spin()
