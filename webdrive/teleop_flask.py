#!/usr/bin/python
##########################################################################
# teleop_flask.py
# License: MIT
# Original Author:  Dave Barrett, mentor team 5109
# Contributors:
# Purpose: To implement a simple flask interface
#    which operates the team 5109 'Tinybot'
#    This gives us manual drive capabilities
#    and a simple interface for teleoperation
#    in some very easy to understand code.
# TL;DR: Drive a bot from a web interface
##########################################################################
# Copyright 2020 Johns Creek Gladiator Robotics
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##########################################################################
from __future__ import print_function # In python 2.7
import sys
from flask import Flask, request, render_template
import pigpio
import json
import sys

###############
# Defines, to keep track of pins
###############
leftPWM = 12
rightPWM = 13

###############
# Setup stuff.  GPIO directions, etc
##############
# Rather than specify a velocity, let's pick a pwm duty cycle to
# run at.  Ideally this matches whatever we have the slider set
# on our web page
steadySpeed=700000

# we're using pigpio, so pigpiod needs to be loaded as a daemon
# prior to starting this script
pi = pigpio.pi()

# set the modes of our output drives
pi.set_mode(7,pigpio.OUTPUT) #left
pi.set_mode(1,pigpio.OUTPUT)

pi.set_mode(0,pigpio.OUTPUT) #right
pi.set_mode(5,pigpio.OUTPUT)

# Next is a convenient way to get where the app is defined
app = Flask(__name__)



##############
# Function: direction(way)
# This is probably obvious, but
# sets up your drive IO pins depending on
# which way you want to go
# Returns: currently nothing.
# may want to return a success, failure
# bit at some point
#############
def direction(way):
    if (way == 'forward'):
        pi.write(7,0)
        pi.write(1,1)

        pi.write(0,1)
        pi.write(5,0)

    elif (way == 'backward'):
        pi.write(7,1)
        pi.write(1,0)

        pi.write(0,0)
        pi.write(5,1)

    elif (way == 'left'):
        pi.write(7,1)
        pi.write(1,0)

        pi.write(0,1)
        pi.write(5,0)

    elif (way == 'right'):
        pi.write(7,0)
        pi.write(1,1)

        pi.write(0,0)
        pi.write(5,1)



################
# Function go(howfastLeft, howFastRight)
# Sets the PWM value for each
# drive wheel
# Returns: nada
################
def go(howFastLeft, howFastRight):
    pi.hardware_PWM(leftPWM, 1000, howFastLeft)
    pi.hardware_PWM(rightPWM, 1000, howFastRight)



##################
# This is what happens when
# You hit the root ip address:port
#################
@app.route('/')
def execute():
    return render_template('drive.html')


##################
# The rest of these are pretty
# obvious.  When this address is called
# the specified function occurs.
# These are called from javascript under
# newdrive.html
##################
@app.route('/forward')
def setForward():
    direction('forward')
    go(steadySpeed, steadySpeed)
    return ("nothing")


@app.route('/backward')
def setBackward():
    direction('backward')
    go(steadySpeed, steadySpeed)
    return ("nothing")

@app.route('/left')
def setLeft():
    direction('left')
    go(steadySpeed, steadySpeed)
    return ("nothing")

@app.route('/right')
def setRight():
    direction('right')
    go(steadySpeed, steadySpeed)
    return ("nothing")

@app.route('/fright')
def setFrontRight():
    direction('forward')
    go(steadySpeed, steadySpeed/2)
    return ("nothing")

@app.route('/bright')
def setBackRight():
    direction('backward')
    go(steadySpeed, steadySpeed/2)
    return ("nothing")

@app.route('/fleft')
def setFrontLeft():
    direction('backward')
    go(steadySpeed/2, steadySpeed)
    return ("nothing")

@app.route('/bleft')
def setBackLeft():
    direction('backward')
    go(steadySpeed/2, steadySpeed)
    return ("nothing")

@app.route('/stop')
def setStop():
    go(0,0)
    return ("nothing")

# OK this one is a *little* more tricky, in that
# I'm collecting some data sent.  Ever see something
# that looks like /url?stuff=23
# well, this handles that sort of thing, like
# /speed?data=50
# means you had your slider set to 50
@app.route('/speed', methods=['GET','POST'])
def speed():
    global steadySpeed
    clicked = None
    clicked = (request.args.get('data'))
    steadySpeed = int(clicked) * 10000
    return ("nothing")
    





###################
# Here's where we specify the server
# to publish.  0.0.0.0 means
# It'll take an html get from anyone
###################
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run('0.0.0.0')




