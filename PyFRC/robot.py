try:
	import wpilib
except ImportError:
	from pyfrc import wpilib

class MyRobot(wpilib.SimpleRobot):
	def __init__(self):
		super().__init__()
		
		self.cstick = wpilib.Joystick(1)
		self.lstick = wpilib.Joystick(2)
		self.rstick = wpilib.Joystick(3)

		self.lfmotor = wpilib.Victor(1)
		self.rfmotor = wpilib.Victor(2)
		self.lbmotor = wpilib.Victor(3)
		self.rbmotor = wpilib.Victor(4)
		self.spmotor = wpilib.Jaguar(5)
		self.wdmotor = wpilib.Victor(6)
		self.sbmotor = wpilib.Victor(7)

		self.compressor = wpilib.Compressor(2,2)
		self.solenoidA1 = wpilib.Solenoid(1)
		self.solenoidA2 = wpilib.Solenoid(2)
		self.solenoidB1 = wpilib.Solenoid(3)
		self.solenoidB2 = wpilib.Solenoid(4)
		self.solenoidC1 = wpilib.Solenoid(5)
		self.solenoidC2 = wpilib.Solenoid(6)
	
	def Disabled(self):
		self.GetWatchdog().SetEnabled(False)
		print("**** DISABLED ****")
		while self.IsDisabled():
			self.CheckRestart()
			wpilib.Wait(0.01)
		
	def Autonomous(self):
		self.GetWatchdog().SetEnabled(False)
		print("**** AUTONOMOUS ****")
		while self.IsAutonomous() and self.IsEnabled():
			self.CheckRestart()

			self.solenoidA1.Set(False)
			self.solenoidA2.Set(True)
			wpilib.Wait(0.5)
			self.solenoidA1.Set(True)
			self.solenoidA2.Set(False)
			wpilib.Wait(0.5)

	def OperatorControl(self):
		print("**** TELEOP ****")
		dog = self.GetWatchdog()
		dog.SetEnabled(True)
		dog.SetExpiration(0.25)

		while self.IsOperatorControl() and self.IsEnabled():
			dog.Feed()
			self.CheckRestart()
			
			# Motor control
			self.setMotorsFromStick(self.cstick)
			self.setJaguar(0)
			self.handleButtons(self.PressedButton())
			wpilib.Wait(0.04)
	
	def Test(self):
		self.GetWatchdog().SetEnabled(False)
		print("**** TEST ****")
		print("Beginning test routine")
		print("======================")
		print("Driving test")
		print("Michelle hates me! Boohoo!")
		
	#Non-RobotPy Methods
	
	def CheckRestart(self):
		if "6L" in self.PressedButton():
			print("Operator killed robot with button 9 on the left joystick")
			raise RuntimeError("OperatorLeftRestart")
		elif "9R" in self.PressedButton():
			print("Operator killed robot with button 6 on the right joystick")
			raise RuntimeError("OperatorRightRestart")
		elif "7C" in self.PressedButton():
			print("Driver killed robot with back button on the xBox controller")
			raise RuntimeError("DriverRestart")

	def PressedButton(self):
		list = []
		for i in range(12):
			if self.cstick.GetRawButton(i):
				list.append(str(i)+"C")
			if self.rstick.GetRawButton(i):
				list.append(str(i)+"R")
			if self.lstick.GetRawButton(i):
				list.append(str(i)+"L")
		return list
	
	def handleButtons(self, buttons):
		for button in buttons:
			if button == "1R":
				print("Extending piston")
				self.solenoidA1.Set(False)
				self.solenoidA2.Set(True)
			elif button == "2R":
				print("Retracting piston")
				self.solenoidA1.Set(True)
				self.solenoidA2.Set(False)
			elif button == "4R":
				print("Spinning rollers inward")
				self.setJaguar(-1)
			elif button == "6R":
				print("Spinning rollers outward")
				self.setJaguar(1)
			elif button == "2L":
				print("Lowering roller arm")
				self.solenoidB1.Set(True)
				self.solenoidB2.Set(False)
			elif button == "3L":
				print("Lifting roller arm")
				self.solenoidB1.Set(False)
				self.solenoidB2.Set(True)
			elif button == "4L":
				print("Lowering forklift")
				self.solenoidC1.Set(True)
				self.solenoidB2.Set(False)
			elif button == "5L":
				print("Lifting forklift")
				self.solenoidC1.Set(False)
				sself.solenoidC2.Set(True)
		
	def setMotorsFromStick(self, stick):
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
		
		self.setMotors(throttle-X, throttle+X)

	def setMotors(self, left, right):
		self.lbmotor.Set(left * -1)
		self.lfmotor.Set(left * -1)
		self.rbmotor.Set(right * -1)
		self.rfmotor.Set(right * 1)

	def setJaguar(self, speed):
		self.spmotor.Set(speed * 0.75)

	def startCompressor(self):
		print("Starting compressor")
		self.compressor.Start()

def run():
	robot = MyRobot()
	robot.startCompressor()
	robot.StartCompetition()
	
	return robot


if __name__ == '__main__':
	wpilib.run()