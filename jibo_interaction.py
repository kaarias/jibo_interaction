from fysom import *
from random import *

from jibo_msgs.msg import JiboAction
from jibo_msgs.msg import JiboVec3
from std_msgs.msg import Header  # standard ROS msg header

import os
import sys
import time
import rospy
import pyaudio
import keyboard
import recorder
import datetime
import sys, select
import question_selector
import speech_recognition as sr


 ####GLOBAL_VARIABLES####
repeat_instructions = True
repeat_question = True
repeat_silence = True
QUIT = False
num_questions_asked = 1
counter = 0

index = str(pyaudio.PyAudio().get_device_count() - 1)
index = int(index[:2])
TALKING = False
TIMEOUT = 5

PREV_STATE = 'instructions'
question_list = question_selector.random_selector()

fsm = Fysom({'initial': 'instructions',
             'final': 'end',
             'events': [
                {'name': 'repeat_instructions', 'src': 'instructions', 'dst': 'instructions'},
                {'name': 'ask_question',  'src': 'instructions',   'dst': 'question'},
		        {'name': 'repeat_question',  'src': 'listen',   'dst': 'question'},
		        {'name': 'start_listening',  'src': 'question',   'dst': 'listen'},
		        {'name': 'keep_listening',  'src':'listen',   'dst': 'listen'},
		        {'name': 'done_listening',  'src': 'listen',   'dst': 'done'},
		        {'name': 'next_question',  'src': 'done',   'dst': 'question'},
		        {'name': 'stay_done',  'src': 'done',   'dst': 'done'},
		        {'name': 'finish_task',  'src': 'done',   'dst': 'end'},
		        {'name': 'instruct_to_silence',  'src': 'instructions',   'dst': 'silence'},
                {'name': 'silence_to_instruct',  'src': 'silence',   'dst': 'instructions'},
                {'name': 'question_to_silence',  'src': 'question',   'dst': 'silence'},
                {'name': 'silence_to_question',  'src': 'silence',   'dst': 'question'},
                {'name': 'listen_to_silence',  'src': 'listen',   'dst': 'silence'},
                {'name': 'silence_to_listen',  'src': 'silence',   'dst': 'listen'},
                {'name': 'done_to_silence',  'src': 'done',   'dst': 'silence'},
                {'name': 'silence_to_done',  'src': 'silence',   'dst': 'done'},
                {'name': 'end_to_silence',  'src': 'end',   'dst': 'silence'},
                {'name': 'silence_to_end',  'src': 'silence',   'dst': 'end'},
                {'name': 'silence_to_silence', 'src': 'silence', 'dst': 'silence'}]})


#############################################################################################
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

mySender = RobotSender()
mySender.start_robot_publisher()
mySender.start_robot_publisher()

def send_robot_tts_cmd(string1):
    mySender.send_robot_tts_cmd(string1)
    #print(string)

################################################################################


def oninstructions():
    if repeat_instructions:
        send_robot_tts_cmd("Lets talk")
        time.sleep(1)
	send_robot_tts_cmd("I am going to ask you three questions and you can share your thoughts with me. We will do one question at a time.")
        time.sleep(1)
        send_robot_tts_cmd("When you start a question please say 'start'. When you're finished talking say 'done'")
        time.sleep(1)
	send_robot_tts_cmd("Are you ready? If you're ready say 'continue'. If you want me to repeat the instructions say 'repeat'.")
    else:
        pass

def onsilence():
    send_robot_tts_cmd("Are you still there? If you are still there and would like to continue please say 'continue'.")
    time.sleep(1)

def onquestion():
    if repeat_question:
        if num_questions_asked == 1:
            send_robot_tts_cmd("Here is the first question")
            time.sleep(3)
            send_robot_tts_cmd(question_list[0])
            time.sleep(3)
            send_robot_tts_cmd("Say 'start' when you're ready to start and 'done' when you're finished answering.")


        if num_questions_asked == 2:
            send_robot_tts_cmd("Here is the second question")
            time.sleep(3)
            send_robot_tts_cmd(question_list[1])
            time.sleep(3)
            send_robot_tts_cmd("Say 'start' when you're ready to start and 'done' when you're finished answering.")


        if num_questions_asked == 3:
            send_robot_tts_cmd("Here is the third question")
            time.sleep(3)
            send_robot_tts_cmd(question_list[2])
            time.sleep(3)
            send_robot_tts_cmd("Say 'start' when you're ready to start and 'done' when you're finished answering.")

    else:
        pass

def onfinish_task():
    send_robot_tts_cmd("You did an awesome job answering questions today")
    time.sleep(3)
    send_robot_tts_cmd("Lets talk again tomorrow")
    r6 = sr.Recognizer()
    counter1 = 0    
    loop = True
    while loop:
        with sr.Microphone(index) as source:
            r6.adjust_for_ambient_noise(source)
            print("before")
            audio = r6.listen(source)
            print("LISTENING")
    
        try:
            if "bye" in r6.recognize_google(audio):
                send_robot_tts_cmd("Bye bye!1")
                loop = False
        except sr.UnknownValueError:
            counter1 += 1
            if counter1 <= 2:
                print(counter1)
                pass
            else:
                loop = False
                send_robot_tts_cmd("Bye bye!2")

def silent_return(state):
    if state == 'instructions':
        fsm.silence_to_instruct()
    if state == 'question':
        repeat_question = True
        fsm.silence_to_question()
    if state == 'listen':
        fsm.silence_to_listen()
    if state == 'done':
        fsm.silence_to_done()


def format_filename(time):
    time = time.replace(" ", "_")
    time = time + ".wav"
    return time

filename = format_filename(str(datetime.datetime.now()))



if __name__ == '__main__':


    rec = recorder.Recorder(channels=2)
    with rec.open(filename, 'wb') as recfile2:
        recfile2.start_recording()
        time.sleep(5.0)
    

        while fsm.current != 'end':


            while fsm.current == 'instructions':
                PREV_STATE = 'instructions'
                #sys.path.insert(0, '/home/prg-brix7/Moody_BackChanneling-master/Live')
                #import saver 
                #os.system('xterm -e python /home/prg-brix7/Moody_BackChanneling-master/Live/node_ComponentManager.py')
                oninstructions()
                repeat_instructions = False

                # obtain audio 
                r1 = sr.Recognizer()
                with sr.Microphone(index) as source:
                    r1.adjust_for_ambient_noise(source)
                    print("before")
                    audio = r1.listen(source)
                    print("LISTENING")
                try:
                    #if person says repeat
                    if "repeat" in r1.recognize_google(audio):
                        repeat_instructions = True
                        print("YOU SAID REPEAT!")

                    #check to see if person says move on
                    if "continue" in r1.recognize_google(audio):
                        fsm.ask_question()
                        print("YOU SAID CONTINUE!")
    	    
                except sr.UnknownValueError:
                    counter += 1
                    if counter <= 2:
                        print(counter)
                        pass
                    else:
                        counter = 0
                        fsm.instruct_to_silence()


            
            while fsm.current == 'question':
    	        onquestion()
                repeat_question = False

                # obtain audio 
                r2 = sr.Recognizer()
                with sr.Microphone(index) as source:
                    r2.adjust_for_ambient_noise(source)
                    print("before")
                    audio = r2.listen(source)
                    print("LISTENING")

                try:
                    if "repeat" in r2.recognize_google(audio):
                        repeat_question = True
                        send_robot_tts_cmd("YOU SAID REPEAT!")

                    if "start" in r2.recognize_google(audio):
                        send_robot_tts_cmd('We are starting')
                        time.sleep(3)
                        fsm.start_listening()

                except sr.UnknownValueError:
                    counter += 1
                    if counter <= 2:
                        print(counter)
                        pass
                    else:
                        counter = 0
                        PREV_STATE = 'question'
                        fsm.question_to_silence()

    	    while fsm.current == 'listen':
                send_robot_tts_cmd('im listening')
                # obtain audio 
                r3 = sr.Recognizer()
                with sr.Microphone(index) as source:
                    r3.adjust_for_ambient_noise(source)
                    print("before")
                    audio = r3.listen(source)
                    print("LISTENING")

                if PREV_STATE != 'listen':
                    PREV_STATE = 'listen'
                    #start backchanneling


                try:
                    if "done" in r3.recognize_google(audio):
                        #stop backchanneling
                        print("you said DONE")
                        fsm.done_listening()
               
                    elif "repeat" in r3.recognize_google(audio):
                        print("you said REPEAT")
                        repeat_question = True
                        fsm.repeat_question()

                    elif ("I" in r3.recognize_google(audio) or "the" in r3.recognize_google(audio) or
                         "and" in r3.recognize_google(audio) or "to" in r3.recognize_google(audio) or
                         "like" in r3.recognize_google(audio) or "is" in r3.recognize_google(audio) or
                         "for" in r3.recognize_google(audio) or "but" in r3.recognize_google(audio) or 
                         "me" in r3.recognize_google(audio) or "that" in r3.recognize_google(audio)):
                        print(fsm.current)
                        print("You're talking and I'm listening")
                        fsm.keep_listening()


                except sr.UnknownValueError:
                    counter += 1
                    if counter <= 3:
                        print(counter)
                        pass
                    else:
                        counter = 0
                        PREV_STATE = 'question'
                        fsm.listen_to_silence()



            if fsm.current == 'done':

                send_robot_tts_cmd("You are done with that question. Are you ready to move on?")
                time.sleep(3)
                send_robot_tts_cmd("If you are ready then say 'yes'. If you are not ready say 'no'")
                
                r4 = sr.Recognizer()
                with sr.Microphone(index) as source:
                    r4.adjust_for_ambient_noise(source)
                    print("before")

                    audio = r4.listen(source)
                    print("LISTENING")

                try:
                    if "yes" in r4.recognize_google(audio):
                        num_questions_asked += 1
                        repeat_question = True
                        if num_questions_asked <4:
                            fsm.next_question()
                        else:
                            fsm.finish_task()
                    if "no" in r4.recognize_google(audio):
                        send_robot_tts_cmd("ok I will wait")
                        time.sleep(10)
                        fsm.stay_done()
                except sr.UnknownValueError:
                    counter += 1
                    if counter <= 2:
                        print(counter)
                        pass
                    else:
                        counter = 0
                        PREV_STATE = 'done'
                        fsm.done_to_silence()



            while fsm.current == 'silence':
                if repeat_silence:
                    onsilence()

                r5 = sr.Recognizer()
                with sr.Microphone(index) as source:
                    r5.adjust_for_ambient_noise(source)
                    print("before")
                    audio = r5.listen(source)
                    print("LISTENING")

                try:
                    if "continue" in r5.recognize_google(audio):
                        if PREV_STATE == 'instructions':
                            repeat_instructions = True
                        elif PREV_STATE == 'question':
                            repeat_question = True
                        else:
                            repeat_instructions = False
                            repeat_question = False

                        silent_return(PREV_STATE)

                except sr.UnknownValueError:
                    counter += 1
                    if counter <= 5:
                        print(counter)
                        pass
                        if counter %2 == 0:
                          repeat_silence = True
                        else:
                            repeat_silence = False
                    else:
                        print("HERE!!!!!!!!!!")
                        counter = 0
                        QUIT = True
                        fsm.silence_to_end()
                
        
        if fsm.current == 'end':
            #say goodbye
            onfinish_task()  

    recfile2.stop_recording()

    print("WE ARE DONE WITH THE THING")
    if QUIT:
        print("you quit")
        src = "/home/prg-brix7/projects/ros_catkin_ws/src/jibo_msgs/" + filename
        dst = "/home/prg-brix7/projects/ros_catkin_ws/src/jibo_msgs/audio_files/failure/FAIL_" + filename
        os.rename(src, dst)
    else:
        print("You did not quit. Good for you")
        src = "/home/prg-brix7/projects/ros_catkin_ws/src/jibo_msgs/" + filename
        dst = "/home/prg-brix7/projects/ros_catkin_ws/src/jibo_msgs/audio_files/success/" + filename
        os.rename(src, dst)


            
    
