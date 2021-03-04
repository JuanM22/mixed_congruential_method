from controller.main import Control

class Run:
    
    def __init__(self):
        self.run = None
    
    def main(self):
        control = Control()
        control.runProgram()

r = Run()
r.main()