##libaries needed for the project
from array import array
from random import randint
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO_TRIGGER_Forward = 29 ## sets GPIO_TRIGGER_Forward to pin 29
GPIO_ECHO_Forward = 31## sets GPIO_ECHO_Forward to pin 31

GPIO.setup(GPIO_TRIGGER_Forward, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Forward, GPIO.IN)

GPIO_TRIGGER_Left = 38## sets GPIO_TRIGGER_Left to pin 38
GPIO_ECHO_Left = 40## sets GPIO_ECHO_Left to pin 40

GPIO.setup(GPIO_TRIGGER_Left, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Left, GPIO.IN)

GPIO_TRIGGER_Right = 7## sets GPIO_TRIGGER_Right to pin 7
GPIO_ECHO_Right = 37## sets GPIO_ECHO_Right to pin 37

GPIO.setup(GPIO_TRIGGER_Right, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Right, GPIO.IN)

GPIO_TRIGGER_Back = 36
GPIO_ECHO_Back = 32

GPIO.setup(GPIO_TRIGGER_Back, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Back, GPIO.IN)

GPIO.setwarnings(False)## gets rid of warnings 


upPin = 12 ## right ENB
downPin = 13 ## left ENA
leftPin = 15 ## left ENA
rightPin = 11 ## right ENB

ENA = 33
ENB = 35

Freq = 200

x = randint(0,1)## sets x to a random number from 0 to 1

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwm = GPIO.PWM(ENA,Freq)
pwm2 = GPIO.PWM(ENB,Freq)

pwm.start(50)## motor 1 starts at 50%
pwm2.start(50) ## motor 2 starts at 50%

##initialising variables that are needed in the code
lis = ["Left", "Right"]##this is for the random turn
long = array ("b",[True])
TStamp = array ("i", [5,0])
Dis = array ("f", [0,0,0,0]) ##el 0 is Left el 1 is Right el 2 is Forward and el 3 is Back and el 4 is a place holder for range
stopDis = array ("f", [0])
flag = array ("b", [False, False,True])
z = array ("f", [1])

global kp
kp=0

def Start():
    pwm.start(50)## this starts the motor1 on 50% 
    pwm2.start(50)## this starts the second motor on 50%
##  speed()
    distanceF()## calls def DistanceF
    print("Forward")
    adjust()
    if (Dis[2] <= 10):## if element is less or equal to 15 
        print("Slowly Moving forward")
        init()## calls the def init 
        time.sleep(1)## stops after a second 
        forward() ## calls forward 
        time.sleep(0.1)## sleeps after 0.2 seconds 
        init()## calls init 
        distanceF()## calls distanceF which is the front sensor
        time.sleep(1)## sleeps after a second 
    else:## if the argument wasnt met do this 
        print("Safe to move forward fast")
        forward()## calls forward 
        time.sleep(0.3)## sleeps after 0.5 
        init()## calls init 
        time.sleep(1)
        adjust()
##        if (Dis[0] < Dis[1]) and (Dis[2] >= 25):## if left is less than Right and forward is greater or equal to 25 do something 
##            print("Adjust Right now")
##            right()
##            time.sleep(0.1)
##            init()
##            time.sleep(1)
####        elif (((Dis[0]) <= Dis[1]-1) or ((Dis[0]) >= Dis[1]+1)) and (Dis[2] >= 25):## if Left is less or equal to Right + 1 or Left - 1 is greater or equal Right - 1 and forward is greater or equal to 25 do something 
####            print("Straight Again")
####            left()
####            time.sleep(0.05)
####            init()
####            time.sleep(1)
##        elif (Dis[1] < (Dis[0])) and (Dis[2] >= 25):## if Right is less than left -1 and Dis[2] is greater or equal to 25 do something 
##            print("Adjust LEFT now")
##            left()
##            time.sleep(0.1)
##            init()
##            time.sleep(1)
####        elif ((Dis[1] <= Dis[0]+1) or (Dis[1] >= Dis[0]-1)) and (Dis[2] >= 25):## if right is less than or equal to left + 1 or right is greater or equal to left -1 and forward is greater than 25 do something
####            print("Straight Again")
####            right()
####            time.sleep(0.05)
####            init()
####            time.sleep(1)
####            reset()

    if (Dis[2] <= 11):## if forward is less or equal to 11
        print ("Stop")
        init()
        time.sleep(2)
        flag[0]= True
        flag[1]= False
        distanceF()
        check()

def ON(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
     
def OFF(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def init():
    pwm.ChangeDutyCycle(50)
    pwm2.ChangeDutyCycle(50)
    OFF(leftPin)
    OFF(rightPin)
    OFF(upPin)
    OFF(downPin)
    OFF(ENA)
    OFF(ENB)
    distanceF()
    distanceL()
    distanceR()

def forward(): ##moves the carforward
    ON(upPin)
    ON(downPin)
    OFF(leftPin)
    OFF(rightPin)
    ON(ENA)
    ON(ENB)
        
def backward():##moves the car backwards
    ON(leftPin)
    ON(rightPin)
    OFF(upPin)
    OFF(downPin)
    ON(ENA)
    ON(ENB)
    
def left(): ##spins the car to the left
    ON(leftPin)
    ON(upPin)
    OFF(downPin)
    OFF(rightPin)
    ON(ENA)
    ON(ENB)

def right(): ##spins the car to the right
    ON(rightPin)
    ON(downPin)
    OFF(upPin)
    OFF(leftPin)
    ON(ENA)
    ON(ENB)
        
##def checkDis():
##
##    if TStamp[0] <= 30 and TStamp[0] > 0:
##        TStamp[0] = TStamp[0] - 1
##    elif TStamp[0] == 0:
##        long[0] = True
##
##    if long[0] == True:
##        distanceF()

def distanceF(): ##uses the front sensor to get data 
    GPIO.output(GPIO_TRIGGER_Forward, True)## gets the distance from the front senseor
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_Forward, False)

    while GPIO.input(GPIO_ECHO_Forward) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO_Forward) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance2 = (TimeElapsed * 34300) / 2
    distance = int(distance2)
    Dis[2] = distance## sets the forward elemet in the array
    
    if (flag[0] == True):
        stopDis[0] = distance
        flag[0] = False
    print ("F")
    print (distance)
    
##    if distance > 30:
##        long[0] = False
##        TStamp[0] = 1

    return distanceF## takes the program back to where we left off 

def distanceL(): ##uses the left sensor to get data
    GPIO.output(GPIO_TRIGGER_Left, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_Left, False)

    while GPIO.input(GPIO_ECHO_Left) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO_Left) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance2 = (TimeElapsed * 34300) / 2
    distance = int(distance2)
    
    Dis[0] = distance
##    print ("L")
##    print (distance)
    
    return distanceL
    
def distanceR(): ##uses the right sensor to get data 
    GPIO.output(GPIO_TRIGGER_Right, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_Right, False)

    while GPIO.input(GPIO_ECHO_Right) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO_Right) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance2 = (TimeElapsed * 34300) / 2
    distance = int(distance2)
    
    Dis[1] = distance
##    print ("R")
##    print (distance)

    return distanceR

def distanceB(): ##uses the back sensor on the car to get data 
    GPIO.output(GPIO_TRIGGER_Back, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_Back, False)

    while GPIO.input(GPIO_ECHO_Back) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO_Back) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance2 = (TimeElapsed * 34300) / 2
    distance = int(distance2)
    
    Dis[3] = distance
##    print ("R")
##    print (distance)

    return distanceB

def speed(): ## this had an error in that i have fixed on the 6th of Aug where Dis[2] was Dis[0] meaning it was taking the left sensors reading rather than the front.
    ## also some of the Dis[2] were just Dis with no [] meaning they didnt do anything and the if statement could never be done.
    ## this may also need to be changed due to the car stopping and starting. (but thats just a thought, i hope you enjoy reading this)

    if Dis[2] > 30:## when forward is less than 30 set speed to ...
         pwm.ChangeDutyCycle(70)
         pwm2.ChangeDutyCycle(70)
    elif Dis[2] <= 30 and Dis[2] >= 26:## when forward is less than or equal to 30 and forward is greater or equal to 26 set speed to ...
        pwm.ChangeDutyCycle(60)
        pwm2.ChangeDutyCycle(60)
    elif Dis[2] <= 25 and Dis[2] >= 21:## when forward is less than or equal to 25 and forward is greater or equal to 21 set speed to ...
        pwm.ChangeDutyCycle(55)
        pwm2.ChangeDutyCycle(55)
    elif Dis[2] <= 20 and Dis[2] >= 16:## when forward is less than or equal to 20 and forward is greater or equal to 16 set speed to ...
        pwm.ChangeDutyCycle(50)
        pwm2.ChangeDutyCycle(50)
    elif Dis[2] <= 15 and Dis[2] >= 11:## when forward is less than or equal to 15 and forward is greater or equal to 11 set speed to ...
        pwm.ChangeDutyCycle(30)
        pwm2.ChangeDutyCycle(30)

def reset(): ##this resets the data
    lis[0] = "Left"## makes element 1 in lis array Left
    lis[1] = "Right"## makes element 2 in lis array Right

def check():
    while (True):## inf loop
        
        x = randint(0,1)## makes x a random number from 0 to 1 

        if (Dis[2] >= 20 and Dis[2] < 40):
            break
        elif (lis[x] == "Left"):## if element equals left then do something
            while (True):## inf loop
                print ("check L")
                distanceL()
                
                if (Dis[x] < 20):
                    lis[x] = "A"## sets left to A so it cant be used again until reset 
                    break
                elif (Dis[x] >= 20):## is left is greater or equal to 35 do something 
                    left()
                    time.sleep(0.1)
                    pwm.ChangeDutyCycle(50)
                    pwm2.ChangeDutyCycle(50)
                    init()
                    time.sleep(1)             
    ##                distanceR()
    ##                distanceL()
                    print("Turning left looking for range")
    ##                print(stopDis[0])

                    if ((Dis[1] >= (stopDis[0] - 3)) and (Dis[1] <= (stopDis[0] + 3))):## if right greater or equal to stopdis - 3 and right is less than stopdis + 3 do something
                        print("IN RANGE")
                        print(Dis[1])
                        init()
                        time.sleep(2)
    ##                    distanceF()
                        z[0]+=1
                        
                        if (z[0] > 1):## if z is greater than 1 do something 
                            if Dis[2] >= 30:## if forward is greater or equal to 30 do something
                                print("forward again")
                                pwm.ChangeDutyCycle(50)
                                pwm2.ChangeDutyCycle(50)
                                print("just moving foward")
                                forward()
                                time.sleep(0.2)
                                init()
                                time.sleep(2)
                                adjust()
                                reset()
                                print("reset fully")
                                flag[1] = True
                                z[0] = 0
                                break

                    elif (Dis[3] <= 10 and Dis[2] >= 30 and Dis[1] <= 15):
                        print("forward pew")
                        pwm.ChangeDutyCycle(50)
                        pwm2.ChangeDutyCycle(50)
                        forward()
                        time.sleep(0.2)
                        init()
                        time.sleep(2)
                        reset()
                        print("reset boii")

                            
        elif (lis[x] =="Right"):## if element equals Right then do somehing
            while (True):## inf loop
                print ("check R")
                distanceR()
                
                if (Dis[x] < 20):## if right is less than 20
                    lis[x] = "A"## set right to A so it cant be used 
                    break
                elif(Dis[x] >= 20):## if right is greater or equal to 20 do something 
                    print ("moving R")
                    right()
                    time.sleep(0.1) 
                    pwm.ChangeDutyCycle(50)
                    pwm2.ChangeDutyCycle(50)
                    init()
                    time.sleep(2)

                    print("Right looking for range")
                    print(stopDis[0])
                    
                    if ((Dis[0] >= (stopDis[0] - 3)) and (Dis[0] <= (stopDis[0] + 3))):## if left is greater or equal to stopdis - 3 and left is less than or equal to stopdis + 3 
                        print("IN RANGE")
                        print(Dis[0])
                        init()
                        time.sleep(2)
                        print("Distance forward should be greater than 10..",Dis[2])
    ##                    distanceF()
                        z[0]+=1
                        
                        if (z[0] > 1):## if z is greater than 1 do something 
                            if Dis[2] >= 30:## if forward is less or equal to 30 do something
                                print("forward again")
                                pwm.ChangeDutyCycle(50)
                                pwm2.ChangeDutyCycle(50)
                                forward()
                                time.sleep(0.2)
                                init()
                                time.sleep(2)
                                adjust()
                                reset()
                                print("reset fully")
                                flag[1] = True
                                z[0] = 0
                                break
                    
                    elif (Dis[3] <= 10 and Dis[2] >= 30 and Dis[0] <= 15):
                        print("forward pew pew")
                        pwm.ChangeDutyCycle(50)
                        pwm2.ChangeDutyCycle(50)
                        forward()
                        time.sleep(0.2)
                        init()
                        time.sleep(2)
                        reset()
                        print("reset boy")
                                
        elif (lis[0] != "Left" and lis[1] != "Right"):## if the elements havent been rest correctly then this will allow the loop to break and reset the array back to how it was 
            if (Dis[2] >= 15):## if forward is greater than 15 do something
                Start()
                reset()

            else:## if the if statement isnt met do this 
                left()
                time.sleep(1.1)
                init()
                time.sleep(5)
                reset()


##this was the origional version of the class adjust this would do a similar job but the new verision is much more precise and furfills the job better
##def Central(): 
##    
##    distanceL()
##    distanceR()
##    while (TStamp[1] <= 6):
##        right()
##        time.sleep(0.08)
##        print("blob")
##        init()
##        time.sleep(2)
##        distanceL()
##        distanceR()
##        TStamp[1] = TStamp[1] + 1
##        if(lis[0] == "Left"):
##            if(Dis[1] <= 15):
##                if((Dis[0] + 5) <= Dis[1]):
##                    print("*DAB*")
##                    break
##                
##        elif(lis[1] == "Right"):
##            if(Dis[0] <= 15):
##                if((Dis[1] + 5) <= Dis[0]):
##                    print("*DAB*")
##                    break

def adjust(): ##this makes sure the car is a certain distance away from the wall.
    Center = False
    while(Center == False):
        print("boo")##just for error checking
        print("Left")
        print(Dis[0])
        print("Right")
        print(Dis[1])
        
        if (Dis[0] < Dis[1]):##left - moves the car to the right making it central
            if (Dis[0] >= 6):
                Center = True
                
            elif (Dis[0] == 5 or Dis[0] == 4):
                right()
                time.sleep(0.06)
                init()
                time.sleep(1)
                
            elif (Dis[0] == 3):
                right()
                time.sleep(0.08)
                init()
                time.sleep(1)

            elif (Dis[0] == 2):
                right()
                time.sleep(0.09)
                init()
                time.sleep(1)

            elif (Dis[0] == 1):
                right()
                time.sleep(0.1)
                init()
                time.sleep(1)
                
        elif (Dis[1] < Dis[0]):##right - moves the car to the left making it central
            if (Dis[1] >= 6):
                Center = True
                
            elif (Dis[1] == 5 or Dis[1] == 4):
                left()
                time.sleep(0.06)
                init()
                time.sleep(1)

            elif (Dis[1] == 3):
                left()
                time.sleep(0.08)
                init()
                time.sleep(1)

            elif (Dis[1] == 2):
                left()
                time.sleep(0.09)
                init()
                time.sleep(1)

            elif (Dis[1] == 1):
                left()
                time.sleep(0.1)
                init()
                time.sleep(1)
                
        distanceL()
        distanceR()

        if (Dis[0] == Dis[1]):
            Center = True
            
while (1):## inf loop

    Start()## this starts the whole program and eveything is done inside this def
            
    
