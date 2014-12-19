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

xboxController = wpilib.Joystick(1)
lstick = wpilib.Joystick(3)
rstick = wpilib.Joystick(2)

lfmotor = wpilib.Victor(1) #left front drive motor
rfmotor = wpilib.Victor(2) #right front drive motor
lbmotor = wpilib.Victor(3) #left back drive motor
rbmotor = wpilib.Victor(4) #right back drive motor
spmotor = wpilib.Jaguar(5) #Jaguar motor
wdmotor = wpilib.Victor(6) #snowblower motor
sbmotor = wpilib.Victor(7) #window motor

def CheckRestart():
	if 7 in PressedButton(xboxController):
		print("Killed by driver ('back' button on xBox controller)")
		raise RuntimeError("DriverRestart")
	elif 9 in PressedButton(rstick):
		print("Killed by operator (button 9 on right joystick)")
		raise RuntimeError("OperatorRightRestart")
	elif	6 in PressedButton(lstick):
		print("Killed by operator (button 6 on left joystick)")
		raise RuntimeError("OperatorLeftRestart")
	return False

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
		#queue = "1212121233330000"
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
			setMotors(-1, -1)
			wpilib.Wait(0.5)
			setMotors(0.5,-0.5)
			wpilib.Wait(0.75)
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
			setMotorsFromStick(xboxController)
			handleButtons(PressedButton(xboxController))
			setSnow(lstick.GetY()) 
			setWindow(rstick.GetY())
			setJaguar(rstick.GetX())
			wpilib.Wait(0.04)


def handleButtons(buttons):
	for button in buttons:
		if button == 1:
			setJaguar(xboxController.GetY())
			
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
	rbmotor.Set(right * -1)
	rfmotor.Set(right * -1)
	
def setJaguar(speed):
	spmotor.Set(speed * 1)
	
def setSnow(speed):
	sbmotor.Set(speed * 1)
	
def setWindow(speed):
	wdmotor.Set(speed * -1)

#Experimental method to get around phantom errors
#def setMotor(motor, speed):
#	motor.Set(speed)
	
def run():
	robot = MyRobot()
	robot.StartCompetition()
