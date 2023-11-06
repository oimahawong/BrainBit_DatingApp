####Program takes in two normalized vector waves for a given video sample
#### 
####
####Returns a percentage which is the match amount for the two waves 
####

import math

#Input received two normalized waave vectors passed as parameters wav 1 & 2
def MatchMyWaves(wav1: float, wav2: float) -> float:

        waveMatch : float = 0
        waveIt : float = 0
        waveThat : float = 0
        
        if(wav1 - wav2 == 0 && wav2 - wav1 == 0):
            return waveMatch = 1
        elif(abs(wav1 - wav2 > 1) && abs(wav2 - wav1 > 0)):
            waveIt = abs(1 - wav1)
            waveThat = abs(1 - wav2)
            return MatchMyWaves((waveIt),(waveThat))
        elif(abs(wav1 - wav2) <= 0.99999999 && abs(wav2 - wav1) > 0.9999999):
            return waveMatch = .99999999
        elif(abs(wav1 - wav2) <= 0.9999999 && abs(wav2 - wav1) > 0.999999):
            return waveMatch = .9999999
        elif(abs(wav1 - wav2) <= 0.999999 && abs(wav2 - wav1) > 0.99999):
            return waveMatch = .999999
        elif(abs(wav1 - wav2) <= 0.999999 && abs(wav2 - wav1) > 0.99999):
            return waveMatch = .99999
        elif(abs(wav1 - wav2) <= 0.99999 && abs(wav2 - wav1) > 0.9999):
            return waveMatch = .9999
        elif(abs(wav1 - wav2) <= 0.9999 && abs(wav2 - wav1) > 0.999):
            return waveMatch = .999
        elif(abs(wav1 - wav2) <= 0.999 && abs(wav2 - wav1) > 0.99):
            return waveMatch = .99
        elif(abs(wav1 - wav2) <= 0.99 && abs(wav2 - wav1) > 0.98):
            return waveMatch = .98
        elif(abs(wav1 - wav2) <= 0.98 && abs(wav2 - wav1) > 0.97):
            return waveMatch = .97
        elif(abs(wav1 - wav2) <= 0.97 && abs(wav2 - wav1) > 0.96):
            return waveMatch = .96
        elif(abs(wav1 - wav2) <= 0.96 && abs(wav2 - wav1) > 0.9):
            return waveMatch = .95
        elif(abs(wav1 - wav2) <= 0.9 && abs(wav2 - wav1) > 0.8):
            return waveMatch = .9
        elif(abs(wav1 - wav2) <= 0.9 && abs(wav2 - wav1) > 0.8):
            return waveMatch = .8
        elif(abs(wav1 - wav2) <= 0.8 && abs(wav2 - wav1) > 0.7):
            return waveMatch = .7
        elif(abs(wav1 - wav2) <= 0.7 && abs(wav2 - wav1) > 0.6):
            return waveMatch = .6
        elif(abs(wav1 - wav2) <= 0.6 && abs(wav2 - wav1) > 0.5):
            return waveMatch = .5  
        elif(abs(wav1 - wav2) <= 0.5 && abs(wav2 - wav1) > 0.4):
            return waveMatch = .4
        elif(abs(wav1 - wav2) <= 0.4 && abs(wav2 - wav1) > 0.3):
            return waveMatch = .3
        elif(abs(wav1 - wav2) <= 0.3 && abs(wav2 - wav1) > 0.2):
            return waveMatch = .2
        elif(abs(wav1 - wav2) <= 0.1 && abs(wav2 - wav1) > 0):
            return waveMatch = .1
        else:
            return waveMatch = 0
        
        
        
        
        
        
        
        
        
        return waveMatch
        
        
        
        
        
 '''       

class Python_Switch:
    def day(self, month):
 
        default = "Incorrect day"
 
        return getattr(self, 'case_' + str(month), lambda: default)()
 
    def case_1(self):
        return "Jan"
 
    def case_2(self):
        return "Feb"
 
    def case_3(self):
        return "Mar"
 
 
my_switch = Python_Switch()
 
print(my_switch.day(1))
 
print(my_switch.day(3))
'''