from machine import I2C, Pin, PWM, ADC, Timer
from vl53l0x1 import setup_tofl_device, TBOOT
import utime
import time
import ssd1306
import freesans20
import writer


print("Setting up I2C")


timer = Timer(-1)


# tofl
left_xshut = Pin(16, Pin.OUT)
left_xshut.value(0)

right_xshut = Pin(17, Pin.OUT)
right_xshut.value(0)

i2c = I2C(id = 0, sda = Pin(0), scl = Pin(1))
# i2c_2 = I2C(id = 0, sda = Pin(16), scl= Pin(17))

left_xshut.value(1)
time.sleep_us(TBOOT)
tofl0 = setup_tofl_device(i2c, 40000, 14, 12)
tofl0.set_address(0x31)

right_xshut.value(1)
time.sleep_us(TBOOT)
tofl1 = setup_tofl_device(i2c, 40000, 14, 12)


print ("NOW WE ARE SETTING UP OLED ")

display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(1)# test
display.show()
utime.sleep(0.5)
display.fill(0)# test
display.show()



# Buzzer setup
pwm = PWM(Pin(15))
pwm.freq(1000)
pwm.duty_u16(0)

# Potentiometer setup
pot = ADC(Pin(26))

# Button setup
button_add = Pin(14, Pin.IN, Pin.PULL_UP)
button_sub = Pin(13, Pin.IN, Pin.PULL_UP)
    

print("Button setup done")

# The buzzer notifies of the tresholds lenght
def short_noise(pwm, loudness):
    pwm.duty_u16(loudness)  
    utime.sleep(0.1)  
    pwm.duty_u16(0)  
    utime.sleep(0.3)
    
  
def set_threshold(threshold, button_add, button_sub, pwm):
    times_played = 1
    loudness = pot.read_u16()
    if button_add.value() == 0:
        threshold += 100
        times_played = int(str(threshold)[:1])
        print (times_played)
        for _ in range(times_played):
            short_noise(pwm, loudness)
        if threshold > 800:
            threshold = 800
        
    elif button_sub.value() == 0:
        threshold -= 100
        times_played = int(str(threshold)[:1])
        print (times_played)
        for _ in range(times_played):
            short_noise(pwm, loudness)
        if threshold < 100:
            threshold = 100   
     
    return threshold
        
# Measures the distances between ToF sensors and an objects. Notifies if there is something in forint of the sensor or in thresholds range. 
def measure(tofl0, tofl1, display, pwm, updated_threshold):
    off = 0
    while True:
        measurement = tofl1.read()
        measurement_1 = tofl0.read()
        loudness = pot.read_u16()
  
        print("viens mērījumi:", tofl1.ping(), "mm |",  "divi mērījumi:", tofl0.ping(), "mm |")

        threshold = set_threshold(updated_threshold, button_add, button_sub, pwm)
        threshold_range = threshold + 100
        
        # oled displays the tof values
        large_text = writer.Writer(display, freesans20)
        large_text = writer.Writer(display, freesans20)
        large_text.set_textpos(50, 30)
        large_text.printstring(str(tofl1.ping()))
        large_text = writer.Writer(display, freesans20)
        large_text.set_textpos(5, 30)
        large_text.printstring("ToF:")
        
        #displays the second tofs values
        display.text("ToF2:", 5, 50, 1)
        display.text(str(tofl0.ping()), 50, 50, 1)
        
        #display threshold value
        display.text("th:", 10, 5, 1)
        display.text(str(threshold), 40, 5, 1)
        
        display.show()
        utime.sleep(0.5)
        display.fill(0)
        
        # Activate the buzzer
        if measurement >= threshold and measurement <= threshold_range:
            pwm.duty_u16(loudness)
            utime.sleep(0.3)
            pwm.duty_u16(0)
        elif off == 1:
            break
        
# Checks if there is change in the second ToFs' measures. If there is change in the distance  then notifies about it.     
def get_average_measurement(tofl0, tofl1, pwm, loudness):
    while True:
        measurement = tofl1.read()
        measurement_1 = tofl0.read()
        measurements = []
        for _ in range(3):

            measurements.append(measurement_1)
            utime.sleep(0.5)
        
        average_measurement = sum(measurements) / len(measurements)
        print("Average measurement of tofl0:", average_measurement)
    
        fourth_measurement = tofl0.ping()
        print("Fourth measurement:", fourth_measurement)
        if fourth_measurement + 30  > average_measurement:
            pwm.duty_u16(loudness)
            utime.sleep(0.2)
            pwm.duty_u16(0)
        elif fourth_measurement - 30 < average_measurement:
            pwm.duty_u16(loudness)
            utime.sleep(0.2)
            pwm.duty_u16(0)



def turn_on(tofl0, tofl1, display, pwm):
    threshold = 100

    while True:
        updated_threshold = set_threshold(threshold, button_add, button_sub, pwm)
        measure(tofl0, tofl1, display, pwm, updated_threshold)
        #get_average_measurement(tofl0, tofl1, pwm, loudness)
        utime.sleep(0.1)
        


try:
    turn_on(tofl0, tofl1, display, pwm)
finally:
    # Restore default address
    print("Restoring")
#     tofl0.set_address(0x29)
    tofl0.set_address(0x29)
