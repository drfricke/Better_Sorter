#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import ubinascii, ujson, urequests, utime

# Write your program here
brick.sound.beep()
go_button = TouchSensor(Port.S1)
m_rot = Motor(Port.D)
m_elbow = Motor(Port.B)
m_hand = Motor(Port.C)
belt = Motor(Port.A)

def get_key():
    fin = open('key.txt')
    for element in fin:
        return element
def SL_setup():
    Key = get_key()
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
    headers = {"Accept":"application/json","x-ni-api-key":Key}
    return urlBase, headers   
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply
def Get_SL(Tag):
    urlBase, headers = SL_setup()
    urlValue = urlBase + Tag + "/values/current"
    print(urlValue)
    print(headers)
    try:
        value = urequests.get(urlValue,headers=headers).text
        print(value)
        data = ujson.loads(value)
        print('data')
        print(data)
        result = data.get("value").get("value")
        print(result)
    except Exception as e:
        print(e)
        result = 'failed'
    return result    
def Create_SL(Tag, Type):
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     propName={"type":Type,"path":Tag}
     try:
          urequests.put(urlTag,headers=headers,json=propName).text
     except Exception as e:
          print(e)


m_rot.reset_angle(0)
m_elbow.reset_angle(0)
m_hand.reset_angle(45)


def grab():
    m_hand.run_target(500, 0)
def open_up():
    m_hand.run_target(500, 45)
def one_eighty():
    grab()
    m_elbow.run_target(1000,1200)
    m_rot.run_target(1000,2100)
def zero():
    grab()
    m_elbow.run_target(1000, 1200)
    m_rot.run_target(1000, 0,)
def dump():
    grab()
    m_elbow.run_target(1000,1600)
    open_up()
def up():
    grab()
    m_elbow.run_target(1000,0)
def ninety():
    grab()
    m_elbow.run_target(1000,1200)
    m_rot.run_target(1000,1050)
def which_bin(shape):
    value = int(shape) 
    target = -200 * value
    belt.run_target(500,target)

def sorter():
    open_up()
    while go_button.pressed() != True:
        wait(50)
    ninety()
    open_up()
    Put_SL('move', 'STRING', 'true')
    wait(100)
    Put_SL('move', 'STRING', 'false')
    wait(5000)
    shape = Get_SL('shape')
    which_bin(shape)
    zero()
    dump()
    up()
    which_bin('0')


sorter()
