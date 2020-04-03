from subprocess import call
import time
class CallPy(object):
    
    def __init__(self, path ='bot.py'):
        self.path = path
        
    def call_python_file(self):
        call(["python3", "{}".format(self.path)])

        
if __name__ == "__main__":
    while(True):
        try:
            c=CallPy()
            c.call_python_file()
        except:
            pass
            