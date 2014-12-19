"""
Yoni's fab code, Jan 15

NOTE: Stick strengths are guessed! I assumed a -1 to +1 system,
but there is no testing to back this up! TEST FIRST OR DIE!
Also, designed for Logitech Extreme 3 Pro (or something like that)
Last thing, I promise! Beware this comment (import first issue?)

Actions
=======
Disabled:
	None

Autonomous:
	Go (in half second chunks at 0.25P):
	Left Right Left Right Left Right Left Right
	Both Both Both Both None None None None

Teleop:
	Tank drive
	
Buttons
=======
Active only during teleop
On left stick
Hold down!

3 | left donut
4 | right donut
5 | left spin
6 | right spin
10 | random every tick
11 | linear (left)
12 | linear (right)

Sensitivity
============
Disabled: 0.01 Hz
Autonomous: 0.5 Hz (for ease of code)
Teleop: 0.04 Hz

Hardware
=========
Joystick 1 (Left)
Joystick 2 (Right)

Victor 1 (Right back)
Victor 2 (Left back)
Victor 3 (Right front)
Victor 4 (Left front)
(The order is optimised for TankDrive())
"""

import wpilib
import random #for button 10

lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)
rbmotor = wpilib.Victor(1)
lbmotor = wpilib.Victor(2)
rfmotor = wpilib.Victor(3)
lfmotor = wpilib.Victor(4)

def CheckRestart():
	if 9 in PressedButton():
		raise RuntimeError("Restart")

def PressedButton():
	list = []
    for i in Range(12):
    	if lstick.GetRawButton(i):
    		list.append(i)
    return list

class MyRobot(wpilib.SimpleRobot):
    def Disabled(self):
        while self.IsDisabled():
            CheckRestart()
            wpilib.Wait(0.01)

    def Autonomous(self):
        self.GetWatchdog().SetEnabled(False)
        queue = "1212121233330000"
        while self.IsAutonomous() and self.IsEnabled():
            CheckRestart()
            for action in queue.split(""):
            	if not (self.IsAutonomous() and self.IsEnabled()):
            		break
            	if action == 1:
            		lbmotor.Set(0.25)
            		lfmotor.Set(0.25)
            	else if action == 2:
            		rbmotor.Set(0.25)
            		rfmotor.Set(0.25)
            	else if action == 3:
            		rbmotor.Set(0.25)
            		rfmotor.Set(0.25)
            		lbmotor.Set(0.25)
            		lfmotor.Set(0.25)
            wpilib.Wait(0.5)

    def OperatorControl(self):
        dog = self.GetWatchdog()
        dog.SetEnabled(True)
        dog.SetExpiration(0.25)

        while self.IsOperatorControl() and self.IsEnabled():
            dog.Feed()
            CheckRestart()

            # Motor control
			for button in PressedButton():
				if button == 3:
					lbmotor.Set(1)   #Stick max?
					lfmotor.Set(1)   # ||
				else if button == 4:
					rbmotor.Set(1)   # ||
					rfmotor.Set(1)   # ||
				else if button == 5:
					rbmotor.Set(-1)  # ||
					rfmotor.Set(-1)  # ||
					lbmotor.Set(1)   #Stick min?
					lfmotor.Set(1)   # ||
				else if button == 6:
					rbmotor.Set(1)   #Stick max
					rfmotor.Set(1)   # ||
					lbmotor.Set(-1)  #Stick min?
					lfmotor.Set(-1)  # ||
				else if button == 10:
					rand1 = random.random() * 2 - 1
					rand2 = random.random() * 2 - 1
					rbmotor.Set(rand1)
					rfmotor.Set(rand1)
					lbmotor.Set(rand2)
					lfmotor.Set(rand2)
				else if button == 11:
					rbmotor.Set(lstick.GetY())
					rfmotor.Set(lstick.GetY())
					lbmotor.Set(lstick.GetY())
					lfmotor.Set(lstick.GetY())
				else if button == 12:
					rbmotor.Set(rstick.GetY())
					rfmotor.Set(rstick.GetY())
					lbmotor.Set(rstick.GetY())
					lfmotor.Set(rstick.GetY())
			else:
				rbmotor.Set(rstick.GetY())
				rfmotor.Set(rstick.GetY())
				lbmotor.Set(lstick.GetY())
				lfmotor.Set(lstick.GetY())

            wpilib.Wait(0.04)

def run():
    robot = MyRobot()
    robot.StartCompetition()