import RPi.GPIO as GPIO
import time
 

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_BUZZER= 4


 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)

#PWM for buzzer
p = GPIO.PWM(GPIO_BUZZER,2) 
p.start(50)

#def pulssimodulaatio():
    #p.ChangeDutyCycle(dc)
    #p.ChangeFrequency(freq)



def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
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
            time.sleep(1)
              
 
        
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()