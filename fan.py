import RPi.GPIO as GPIO
import time

# GPIO setup
FAN_PWM_PIN = 18  # GPIO pin for PWM control
FAN_TACH_PIN = 24  # GPIO pin for tachometer input

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PWM_PIN, GPIO.OUT)
GPIO.setup(FAN_TACH_PIN, GPIO.IN)

# PWM setup
fan_pwm = GPIO.PWM(FAN_PWM_PIN, 25000)  # 25kHz PWM frequency
fan_pwm.start(0)  # Start PWM with 0% duty cycle

# Function to set the fan speed
def set_fan_speed(duty_cycle):
    fan_pwm.ChangeDutyCycle(duty_cycle)

# Function to read the RPM from the fan's tachometer
def read_tachometer():
    tach_count = 0
    timeout = time.time() + 1  # 1-second timeout
    while time.time() < timeout:
        if GPIO.input(FAN_TACH_PIN) == 0:
            tach_count += 1
            while GPIO.input(FAN_TACH_PIN) == 0:
                pass
    rpm = (tach_count / 2) * 60
    return rpm

# Main loop
try:
    while True:
        # Example: Set fan speed to 50% for testing
        set_fan_speed(50)
        
        # Read and print the RPM
        rpm = read_tachometer()
        print(f"Fan RPM: {rpm}")
        
        time.sleep(2)  # Wait for 2 seconds before next reading

except KeyboardInterrupt:
    pass

finally:
    fan_pwm.stop()
    GPIO.cleanup()
