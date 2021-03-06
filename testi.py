#imports
import RPi.GPIO as GPIO
import time
 
#set GPIO_pin numbers
GPIO.setmode(GPIO.BCM)
GPIO_TRIG = 23
GPIO_ECHO = 24
GPIO_BUZZER= 4

#set GPIO input/output
GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

#initialise PWM for buzzer
p = GPIO.PWM(GPIO_BUZZER,2) 
p.start(50)

#function to change pwm (dc = dutyCyce, freq = frequency)
def pulssimodulaatio(dc,freq):
    p.ChangeDutyCycle(dc)
    p.ChangeFrequency(freq)


#function to measure distance
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIG, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeDuration = StopTime - StartTime
    distance = (TimeDuration * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print (dist)
            #round dist
            dist = round(dist,0)
            

            #if-else to set correct PWM with pulssimodulaatio()  
            if dist > 100:
                pulssimodulaatio(0,2)

            elif dist in range(100,90,-1):
                pulssimodulaatio(50,2)
            
            elif dist in range(90,80,-1):
                pulssimodulaatio(50,3)

            elif dist in range(80,70,-1):
                pulssimodulaatio(50,4)
            
            elif dist in range(70,60,-1):
                pulssimodulaatio(50,5)
            
            elif dist in range (60,50,-1):
                pulssimodulaatio(50,6)
            
            elif dist in range(50,40,-1):
                pulssimodulaatio(50,7)

            elif dist in range(40,30,-1):
                pulssimodulaatio(50,8)
            
            elif dist in range(30,20,-1):
                pulssimodulaatio(50,9)
            
            elif dist in range(20,10,-1):
                pulssimodulaatio(50,10)
            
            elif dist in range (10,0,-1):
                pulssimodulaatio(100,10)

            time.sleep(1)
            
        
    except KeyboardInterrupt:
        print("Exit by user")
        GPIO.cleanup()