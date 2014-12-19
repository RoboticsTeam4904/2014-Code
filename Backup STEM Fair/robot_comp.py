import wpilib

cstick = wpilib.Joystick(1)
lstick = wpilib.Joystick(2)
rstick = wpilib.Joystick(3)

lfmotor = wpilib.Victor(1)
rfmotor = wpilib.Victor(2)
lbmotor = wpilib.Victor(3)
rbmotor = wpilib.Victor(4)
spmotor = wpilib.Jaguar(5)
wdmotor = wpilib.Victor(6)
sbmotor = wpilib.Victor(7)

compressor = wpilib.Compressor(2,2)
solenoidA1 = wpilib.Solenoid(1)
solenoidA2 = wpilib.Solenoid(2)
solenoidB1 = wpilib.Solenoid(3)
solenoidB2 = wpilib.Solenoid(4)
solenoidC1 = wpilib.Solenoid(5)
solenoidC2 = wpilib.Solenoid(6)

def CheckRestart():
	#if "6L" in PressedButton():
	#	print("Operator killed robot with button 6 on the left joystick")
	#	raise RuntimeError("OperatorLeftRestart")
	if "9R" in PressedButton():
		print("Operator killed robot with button 9 on the right joystick")
		raise RuntimeError("OperatorRightRestart")
	elif "7C" in PressedButton():
		print("Driver killed robot with back button on the xBox controller")
		raise RuntimeError("DriverRestart")

def PressedButton():
	list = []
	for i in range(20):
		if cstick.GetRawButton(i):
			list.append(str(i)+"C")
		if rstick.GetRawButton(i):
			list.append(str(i)+"R")
		if lstick.GetRawButton(i):
			list.append(str(i)+"L")
	return list

class MyRobot(wpilib.SimpleRobot):
	def RobotInit(self):
		print("Initializing robot")
	
	def Disabled(self):
		print("**** DISABLED ****")
		while self.IsDisabled():
			CheckRestart()
			wpilib.Wait(0.01)

	def Autonomous(self):
		print("**** AUTONOMOUS ****")
		self.GetWatchdog().SetEnabled(False)
		
		setMotors(1,1)
		setJaguar(0)
		wpilib.Wait(1)
		
		while self.IsAutonomous() and self.IsEnabled():
			CheckRestart()

			setMotors(0,0)
			wpilib.Wait(0.02)

	def OperatorControl(self):
		print("**** TELEOP ****")
		dog = self.GetWatchdog()
		dog.SetEnabled(True)
		dog.SetExpiration(0.25)

		while self.IsOperatorControl() and self.IsEnabled():
			dog.Feed()
			CheckRestart()
			
			# Motor control
			setMotorsFromStick(cstick)
			setJaguar(rstick.GetX())
			handleButtons(PressedButton())
			wpilib.Wait(0.04)

def handleButtons(buttons):
	for button in buttons:
		if button == "1R":
			print("Extending alligator mouth piston")
			solenoidA1.Set(False)
			solenoidA2.Set(True)
		elif button == "2R":
			print("Retracting alligator mouth piston")
			solenoidA1.Set(True)
			solenoidA2.Set(False)
		elif button == "2L":
			print("Lowering alligator arm")
			solenoidB1.Set(False)
			solenoidB2.Set(True)
		elif button == "3L":
			print("Lifting alligator arm")
			solenoidB1.Set(True)
			solenoidB2.Set(False)
		elif button == "4L":
			print("Lowering forklift")
			solenoidC1.Set(False)
			solenoidC2.Set(True)
		elif button == "5L":
			print("Lifting forklift")
			solenoidC1.Set(True)
			solenoidC2.Set(False)

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

def setMotors(left, right):
	lbmotor.Set(left * -1)
	lfmotor.Set(left * -1)
	rbmotor.Set(right * -1)
	rfmotor.Set(right * 1)

def setJaguar(speed):
	spmotor.Set(speed * 0.75)

def startCompressor():
	print("Starting compressor")
	compressor.Start()

def run():
	startCompressor()
	robot = MyRobot()
	robot.StartCompetition()