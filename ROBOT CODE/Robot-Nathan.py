"""
Yoni's code that barely works and everyone kinda like but it also kinda reminds them of their time back in Vietnam, Jan 15

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
Autonomous: 0.25 Hz
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
#import random

cstick = wpilib.Joystick(1)
lstick = wpilib.Joystick(2)
rstick = wpilib.Joystick(3)
rbmotor = wpilib.Victor(4)
lbmotor = wpilib.Victor(3)
rfmotor = wpilib.Victor(2)
lfmotor = wpilib.Victor(1)
spmotor = wpilib.Jaguar(5)

def CheckRestart():
	if 9 in PressedButton():
		raise RuntimeError("Restart")

def PressedButton():
	list = []
	for i in range(12):
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
			"""for action in queue.split(""):
				if not (self.IsAutonomous() and self.IsEnabled()):
					break
				if action == 1:
					lbmotor.Set(0.25)
					lfmotor.Set(0.25)
				elif action == 2:
					rbmotor.Set(0.25)
					rfmotor.Set(0.25)
				elif action == 3:
					rbmotor.Set(0.25)
					rfmotor.Set(0.25)
					lbmotor.Set(0.25)
					lfmotor.Set(0.25)
			wpilib.Wait(0.5)"""
			setMotors(-0.3, -0.25)
			wpilib.Wait(7.5)
			setMotors(0.5,-0.5)
			wpilib.Wait(1.2)
			setMotors(-0.3, -0.25)
			wpilib.Wait(7.5)
			setMotors(0.5,-0.5)
			wpilib.Wait(1.15)
			setMotors(0,0)

			break

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
					setMotors(-0.1, 0.5)
				elif button == 4:
					setMotors(0.5, -0.1)
				elif button == 5:
					setMotors(-1, 1)
				elif button == 6:
					setMotors(1, -1)
				elif button == 7:
					 setJaguar(rstick.GetY())
				elif button == 11:
					setMotors(lstick.GetY(), lstick.GetY())
				elif button == 12:
					setMotors(rstick.GetY(), rstick.GetY())
			if len(PressedButton()) == 0:
				setMotors(cstick.GetY(), cstick.GetTwist())

			wpilib.Wait(0.04)

def setLMotor(speed):
	lbmotor.Set(speed * -1)
	lfmotor.Set(speed * -1)

def setRMotor(speed):
	rbmotor.Set(speed * 1)
	rfmotor.Set(speed * 1)

def setMotors(left, right):
	lbmotor.Set(left * -1)
	lfmotor.Set(left * -1)
	rbmotor.Set(right * 1)
	rfmotor.Set(right * 1)
	
def setJaguar(speed):
	spmotor.Set(speed * 1)
	
def run():
	robot = MyRobot()
	robot.StartCompetition()