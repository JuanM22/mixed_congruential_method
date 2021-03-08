import view.kolmogorovSmirnovGUI as interface

class Run:
    
    def __init__(self):
        self.run = None
    
    def main(self):
        interface.runProgram()

r = Run()
r.main()