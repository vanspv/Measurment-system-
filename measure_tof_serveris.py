import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from machine import I2C, Pin, PWM, ADC
from vl53l0x import VL53L0X
import ssd1306
import framebuf
import time
import freesans20
import writer
 
# ssid = 'Galaxy S23 4B61'
# password = 'gogogogo'
 
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    for attempt in range(5): # Retry up to 5 times
        try:
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                print('Attempting connection...')
                sleep(1)
            ip = wlan.ifconfig()[0]
            print(f'Connection established on {ip}')
            return ip
        except Exception as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            sleep(2) # Wait before retrying
    print("Failed to connect after multiple attempts.")
    return None
 
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection
 
def webpage(state):
    html = f"""
<!DOCTYPE html>
<html>
<form action="./mesureon">
<input type="submit" value="mesure_distance_on" />
</form>
<form action="./mesureoff">
<input type="submit" value="mesure_distance_off" />
</form>
<p>system is {state}</p>
</body>
</html>
    """
    return str(html)
 
def serve(connection):
    state = 'OFF'
    pico_led.off()
    i2c = I2C(id=0, sda=Pin(0), scl=Pin(1))
    tof = VL53L0X(i2c)
    tof.set_measurement_timing_budget(40000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    pot_2 = ADC(Pin(27))
    threshold_min = 50
    threshold_max = 8190
    pot_max = 1280
    pot_min = 65535
    pot = ADC(Pin(26))
    pwm = PWM(Pin(15))
    pwm.freq(1000)
    pwm.duty_u16(0)
    buzzer_on = False
 
    while True:
        try:
            client, addr = connection.accept()
            request = client.recv(1024).decode()
            print(f"Received request: {request}")
            if '/mesureon' in request:
                pico_led.on()
                state = 'ON'
                # Your existing code for ON state
                while True: 
#                     messurment = tof.read()
                    loudness = pot.read_u16()
                    threshold_value = pot_2.read_u16()
                    print(tof.ping(), "mm", loudness, threshold_value)
                    scaledValue = ((threshold_value - pot_min) / (pot_max - pot_min)) * (threshold_max - threshold_min) + threshold_min
                    threshold = scaledValue
                    threshold_range = scaledValue + 50
                    large_text = writer.Writer(display, freesans20)

                    # oled displays the tof values
                    large_text = writer.Writer(display, freesans20)
                    large_text.set_textpos(40, 30)
                    large_text.printstring(str(tof.ping()))
                    large_text = writer.Writer(display, freesans20)
                    large_text.set_textpos(5, 30)
                    large_text.printstring("tof:")
                    #display threshold value
                    display.text("th:", 10, 5, 1)
                    display.text(str(scaledValue), 40, 5, 1)
                    display.show()
                    sleep(0.1)
                    display.fill(0)
                    # buzzeris iesledzas
                if messurment >= threshold and messurment <= threshold_range:
                     pwm.duty_u16(loudness)
                if '/mesureoff' in request: 
                    break 

                else:
                     pwm.duty_u16(0)
                     display.fill(0)
            elif '/mesureoff' in request:
                    pico_led.off()
                    display.fill(0)
                    state = 'OFF'
                
                # Your existing code for OFF state
            else:
                print("Unknown request")
            html = webpage(state)
            client.send(html)
            client.close()
        except Exception as e:
            print(f"Error handling request: {e}")
            continue
 
try:
    ip = connect()
    if ip is not None:
        connection = open_socket(ip)
        serve(connection)
except KeyboardInterrupt:
    machine.reset()
    display.fill(0)