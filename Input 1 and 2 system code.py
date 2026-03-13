"""
Name: Nolan Walker and Gabe Morielli
Description: Push Button, servo Motor with lid and wheel simulation
Date: 8-Mar-2026
"""

from machine import Pin, PWM
import time
from time import sleep
# Parameters to finetune with hardware testing

OPENED: int = 0
CLOSED: int = 90

max_duty = 7864
min_duty = 1802

delivery_button_pressed = Pin(16, Pin.IN, Pin.PULL_UP)
reverse_button_pressed = Pin(22, Pin.IN, Pin.PULL_UP)

delivery_done = False

servo_1 = Pin(28, Pin.OUT)
servo_pwm1 = PWM(servo_1, freq=50, duty_u16=min_duty)
motor1 = Pin(8, Pin.OUT)
motor2 = Pin(14, Pin.OUT)

delay = 5
quick_delay = 0.5
drive_time = 15
buffer_time = 2

def motors_on():
    print("Motors on now")
    motor1.value(1)
    motor2.value(1)

def motors_off():
    print("Motors off now")
    motor1.value(0)
    motor2.value(0)

def angle_to_duty(angle):
    return int(min_duty + (angle / 180.0) * (max_duty - min_duty))

def run_sequence():
    
    print("Opening lid")
    servo_pwm1.duty_u16(angle_to_duty(OPENED))
    sleep(delay)
   
    print("Closing lid")
    servo_pwm1.duty_u16(angle_to_duty(CLOSED))

    sleep(buffer_time)
    
    print("Waiting buffer")
   
    motors_on()
    sleep(drive_time)

   
    motors_off()

    
    print("Reopening lid")
    servo_pwm1.duty_u16(angle_to_duty(OPENED))
    sleep(delay)

    print("Reclosing lid")
    servo_pwm1.duty_u16(angle_to_duty(CLOSED))

    sleep(quick_delay)
    print("Food is delivered")

def return_sequence():
    print("Returning to caf now")
    sleep(buffer_time)
    motors_on()
    sleep(drive_time)
    motors_off()
    print("Arrived back to origin")

def main():
    global delivery_done
    duty = angle_to_duty(CLOSED)
    servo_pwm1.duty_u16(duty)

    while True:
        if delivery_button_pressed.value() == 0:
            if delivery_done == False:
                sleep(0.02)
                run_sequence()
                delivery_done = True
            else:
                    print("Delivery is already complete, press yellow button to return")

            while delivery_button_pressed.value() == 0:
                    sleep(0.01)

        if reverse_button_pressed.value() == 0:
            sleep(0.02)

            if reverse_button_pressed.value() == 0:
                if delivery_done:
                    return_sequence()
                    delivery_done = False
                else:
                    print("Cannot return: box has not been delivered yet.")

                while reverse_button_pressed.value() == 0:
                    sleep(0.01)


if __name__ == "__main__":
    main()