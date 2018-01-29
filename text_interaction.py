from fysom import *
import speech_recognition as sr
import sys, select
import pyaudio
from random import *
import time
import rospy
import keyboard
from jibo_msgs.msg import JiboAction
from jibo_msgs.msg import JiboVec3
from std_msgs.msg import Header  # standard ROS msg header

 ####GLOBAL_VARIABLES####
repeat_instructions = True
repeat_question = True
num_questions_asked = 1
max_silence = 3
TALKING = False
TIMEOUT = 5
PREV_STATE = 'instructions'

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





def send_robot_tts_cmd(string):
    print(string)

def oninstructions():
    if repeat_instructions:
        send_robot_tts_cmd("Lets talk")
	send_robot_tts_cmd("I am going to ask you three questions and you can share your thoughts with me. We will do one question at a time. When you start a question please say 'start'. When you're finished talking say 'done'")
	send_robot_tts_cmd("Are you ready? If you're ready say 'continue'. If you want me to repeat the instructions say 'repeat'.")
    else:
        pass

def onsilence():
    send_robot_tts_cmd("Are you still there? If you are still there and would like to continue please say 'continue'.")

def onquestion():
    if repeat_question:
        if num_questions_asked == 1:
            #Neutral Question
            send_robot_tts_cmd("Here is the first question")
            send_robot_tts_cmd("What is something you did for another person today?")
            send_robot_tts_cmd("Say 'start' when you're ready to start and 'done' when you're finished answering.")
        if num_questions_asked == 2:
            #Negative Question
            send_robot_tts_cmd("Here is the second question")
            send_robot_tts_cmd("Was there anything that made you angry today?")
            send_robot_tts_cmd("Say 'start' when you're ready to start and 'done' when you're finished answering.")
        if num_questions_asked == 3:
            #Positive Question
            send_robot_tts_cmd("Here is the third question")
            send_robot_tts_cmd("What is something fun you did today?")
            send_robot_tts_cmd("Say 'start' when you're ready to start and 'done' when you're finished answering.")
    else:
        pass

def onfinish_task():
    send_robot_tts_cmd("You did an awesome job answering questions today")
    send_robot_tts_cmd("Lets talk again tomorrow")
    i, o, e = select.select( [sys.stdin], [], [], 7 )
    if (i):
        userinp = sys.stdin.readline().strip()
        send_robot_tts_cmd("Bye bye!")
    else:
        send_robot_tts_cmd("Bye bye!")
    #should wait some time for a child response and then stop recording audio and save

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


if __name__ == '__main__':

    while fsm.current != 'end':
    
        if fsm.current == 'instructions':
            PREV_STATE = 'instructions'

            oninstructions()
            repeat_instructions = False
            i, o, e = select.select( [sys.stdin], [], [], 10 )
            if (i):
                userinp = sys.stdin.readline().strip()

                if userinp == 'repeat':
                    repeat_instructions = True
                    send_robot_tts_cmd("YOU SAID REPEAT!")
                if userinp == 'continue':
                    send_robot_tts_cmd("YOU SAID CONTINUE!")
                    fsm.ask_question()
            else:
                send_robot_tts_cmd('timed out')
                fsm.instruct_to_silence()

        if fsm.current == 'question':
            send_robot_tts_cmd("moved on to question!")
	    onquestion()
            repeat_question = False
            i, o, e = select.select( [sys.stdin], [], [], 10 )
            if (i):
                userinp = sys.stdin.readline().strip()
                if userinp == 'repeat':
                    repeat_question = True
                    send_robot_tts_cmd("YOU SAID REPEAT!")
                if userinp == 'start':
                    send_robot_tts_cmd('We are starting')
                    fsm.start_listening()
            else:
                PREV_STATE = 'question'
                fsm.question_to_silence()

	if fsm.current == 'listen':
            send_robot_tts_cmd('im listening')
            if PREV_STATE != 'listen':
                PREV_STATE = 'listen'
                sentence_until_bk = randint (1,4)
                i, o, e = select.select( [sys.stdin], [], [], 20 )
            else:
                PREV_STATE = 'listen'
                i, o, e = select.select( [sys.stdin], [], [], 40 )
            if (i) or TALKING:
                userinp = sys.stdin.readline().strip()
                if userinp == 'done':
                    #stop backchanneling
                    fsm.done_listening()
           
                if userinp == 'repeat':
                    repeat_question = True
                    fsm.repeat_question()
                if userinp != 'done' and userinp != 'repeat':
                    sentence_until_bk -= 1
                    if sentence_until_bk == 0:
                        send_robot_tts_cmd("mmhmmmm")
                        sentence_until_bk = randint (1,4)
                    fsm.keep_listening() 
            else:
                fsm.listen_to_silence()

        if fsm.current == 'done':
            send_robot_tts_cmd("You are done with that question. Are you ready to move on?")
            send_robot_tts_cmd("If you are ready then say 'yes'. If you are not ready say 'no'")
            i, o, e = select.select( [sys.stdin], [], [], 20 )
            if (i):
                userinp = sys.stdin.readline().strip()
                if userinp == 'yes':
                    num_questions_asked += 1
                    repeat_question = True
                    if num_questions_asked <4:
                        fsm.next_question()
                    else:
                        fsm.finish_task()
                if userinp == 'no':
                    send_robot_tts_cmd("ok I will wait")
                    time.sleep(10)
                    fsm.stay_done()
            else:
                PREV_STATE = 'done'
                fsm.done_to_silence()

        if fsm.current == 'silence':
            if max_silence > 0:
                onsilence()
                i, o, e = select.select( [sys.stdin], [], [], 10 )
                if (i):
                    userinp = sys.stdin.readline().strip()
                    if userinp == 'continue':
                        max_silence = 3
                        if PREV_STATE == 'instructions':
                            repeat_instructions = True
                        elif PREV_STATE == 'question':
                            repeat_question = True
                        else:
                            repeat_instructions = False
                            repeat_question = False

                        silent_return(PREV_STATE)
                else:
                    max_silence -= 1
                    fsm.silence_to_silence()
            else:
                fsm.silence_to_end()
            
    
    if fsm.current == 'end':
        #stop recording
        #say goodbye
        onfinish_task()  


            
    
