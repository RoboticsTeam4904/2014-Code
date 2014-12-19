import wpilib

lstick = wpilib.Joystick(1)
rstick = wpilib.Joystick(2)
lmotor = wpilib.Victor(1)
rmotor = wpilib.Victor(2)


class MyRobot(wpilib.SimpleRobot):
    def OperatorControl(self):
        while self.IsOperatorControl() and self.IsEnabled():
            # Motor control
            lmotor.Set(lstick.GetY())
			rmotor.Set(rstick.GetY())
            wpilib.Wait(0.04)

def run():
    robot = MyRobot()
    robot.StartCompetition()