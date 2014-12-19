"""
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
lstick = wpilib.Joystick(3)
rstick = wpilib.Joystick(2)
rbmotor = wpilib.Victor(4)
lbmotor = wpilib.Victor(3)
rfmotor = wpilib.Victor(2)
lfmotor = wpilib.Victor(1)
spmotor = wpilib.Jaguar(5)

def CheckRestart():
	if 9 in PressedButton(rstick):
		raise RuntimeError("Restart")

def PressedButton(stick):
	list = []
	for i in range(20):
		if stick.GetRawButton(i):
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
		#todo: make this loop not rely on a wait that causes the robot to freak out when entered into teliop mode
		# it will make it so that the motors are controllable in teleop mode when autonomous has been run recently
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
			setMotorsFromStick(cstick)
			print(PressedButton(cstick))
			handleButtons(PressedButton(cstick))
			wpilib.Wait(0.04)


def handleButtons(buttons):
	for button in buttons:
		if button == 1:
			setJaguar(cstick.GetY())
			
def setMotorsFromStick(stick):
	throttle = stick.GetThrottle()
	X = stick.GetX()
	
	throttleGain = 1
	throttleExp = 2
	
	xGain = 1
	xExp = 2
	
	if throttle < 0:
		throttle = throttle ** throttleExp
		throttle *= -throttleGain
	else:
		throttle = throttle ** throttleExp
		throttle *= throttleGain
		
	if X < 0:
		X = X ** xExp
		X *= -xGain
	else:
		X = X ** xExp
		X *= xGain
	
	setMotors(throttle-X, throttle+X)

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
