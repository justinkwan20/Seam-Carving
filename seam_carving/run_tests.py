import datetime, os, signal, subprocess, sys, time, unittest

def run(command, stdin = None, timeout = 30):
    """
    Runs the specified command using specified standard input (if any) and
    returns the output on success. If the command doesn't return within the
    specified time (in seconds), "__TIMEOUT__" is returned.
    """

    start = datetime.datetime.now()
    process = subprocess.Popen(command.split(),
                               stdin = subprocess.PIPE, 
                               stdout = subprocess.PIPE,
                               stderr = subprocess.STDOUT)
    if not stdin is None:
        process.stdin.write(stdin)
        process.stdin.close()
    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return "__TIMEOUT__"
    return process.stdout.read().strip()

class Problem1(unittest.TestCase):
    
    def test1(self):
        command = "java PrintEnergy data/6x5.png"
        sought = """6-by-5 image
Printing energy calculated for each pixel.
    57685     50893     91370     25418     33055     37246 
    15421     56334     22808     54796     11641     25496 
    12344     19236     52030     17708     44735     20663 
    17074     23678     30279     80663     37831     45595 
    32337     30796      4909     73334     40613     36556"""
        got = run(command)
        self.assertNotEquals(got, "__TIMEOUT__")
        self.assertEquals(got, sought)
    
class Problem2(unittest.TestCase):
    
    def test1(self):
        command = "java PrintSeams data/6x5.png"
        sought = """6-by-5 image

Horizontal seam:
 57685   50893   91370   25418   33055   37246  
 15421   56334   22808*  54796   11641*  25496  
 12344*  19236*  52030   17708*  44735   20663* 
 17074   23678   30279   80663   37831   45595  
 32337   30796    4909   73334   40613   36556  

Total energy = 104400


Vertical seam:
 57685   50893   91370   25418*  33055   37246  
 15421   56334   22808   54796   11641*  25496  
 12344   19236   52030   17708*  44735   20663  
 17074   23678   30279*  80663   37831   45595  
 32337   30796    4909*  73334   40613   36556  

Total energy = 89955"""
        got = run(command)
        self.assertNotEquals(got, "__TIMEOUT__")
        self.assertEquals(got, sought)
        
class Problem3(unittest.TestCase):
    
    def test1(self):
        command = "java RemoveSeams data/6x5.png 3 3"
        sought = """3-by-2 image
Printing energy calculated for each pixel.
     2053     26346     17589 
    31333     12186      4507"""
        got = run(command)
        self.assertNotEquals(got, "__TIMEOUT__")
        self.assertEquals(got, sought)

if __name__ == "__main__":
    unittest.main()
    
