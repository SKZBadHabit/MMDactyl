import time
import digitalio
import os
import board
import usb_hid
import displayio
import busio
import terminalio
import adafruit_matrixkeypad
import microcontroller
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import asyncio
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import socketpool
import wifi
from asyncio import create_task, sleep as async_sleep
import json
from adafruit_httpserver import Server, REQUEST_HANDLED_RESPONSE_SENT, Request, Response
import adafruit_ntp
import gc
from adafruit_hid.keycode import Keycode
import ssl
import adafruit_requests
import secrets

#import own files:
from keymapping import (
    key_mappings_keypad1,
    key_mappings_keypad2,
    key_mappings_keypad1_layer2,
    key_mappings_keypad2_layer2,
    keys,
    keys1
)




# TODO start and stop webserver / WIFI over button and in energy saving Mode turn off wifi but i think not possible


# TODO add Tilde and add it to the layout!!!!!!!!


#! --> Mhz Settings of Microcontroller paused!!!! ATTENTION RP 2350 is other than RP 2040!!

# ! Variable Konfiguration:



Codeversion = "Code6.1c"
custom_hostname = "MMDactyl"
WlanSSID_Secret = secrets.secrets["H_WIFI_SSID"]
WlanPW_Secret = secrets.secrets["H_WIFI_PASSWORD"]




print("freemem start gc: ", gc.mem_free())




# Set up a keyboard/mouse device.
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# Define the columns and rows using GPIO pins.
cols = [digitalio.DigitalInOut(x) for x in (board.GP0, board.GP1, board.GP2, board.GP19, board.GP20, board.GP21)]
rows = [digitalio.DigitalInOut(x) for x in (board.GP3, board.GP4, board.GP5, board.GP10, board.GP11)]



# Create matrix keypad objects.
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
keypad1 = adafruit_matrixkeypad.Matrix_Keypad(cols, rows, keys1)

layer = 1  # Initialize the layer variable
layer_fixed = 0

# Define debounce time in seconds for each keypad
DEBOUNCE_TIME_KEYPAD1 = 0.02
DEBOUNCE_TIME_KEYPAD2 = 0.02

# Variables to track last key press time for each keypad
last_key_press_time_keypad1 = time.monotonic()
last_key_press_time_keypad2 = time.monotonic()



# Variables to display refresh time
display_delay_1 = time.monotonic()
display_delay_2 = time.monotonic()
display_delay_3 = time.monotonic()


# Display Refresh time
DISPLAY_REFRESH_TIME_1 = 61 # Asynchron for better performance
DISPLAY_REFRESH_TIME_2 = 62 # Asynchron for better performance
DISPLAY_REFRESH_TIME_3 = 123 # Asynchron for better performance


# MIXED
cpu_temp = 0
runtime_now = time.monotonic()
runtime_refresh = time.monotonic()
current_runtime = 0
alltime_runtime = 0
FILENAME_RUNTIME = "/runtime.txt"
FILENAME_KEYPRESS = "/keypress.txt"
ENERGY_SAVE_REFRESH_TIME = 380
DATE_TIME_REFRESH_TIME = 60
GC_REFRESH_TIME = 910
gc_refresh = 0
energy_save = time.monotonic()
energy_mod = 0
current_keypress = 0
alltime_keypress = 0
templastcurrentkeypresses = 0
display_off_manually = 0
date_time_refresh =0
formatted_time = "00:00"
formatted_date = "01.01.1000"
ntp_time = None
display_is_on = True
key_141_pressed = False
key_131_pressed = False
caps_is_on = False
wificheckpingcounter = 0
humidity = 00
temperature_celsius = 00
WifiStatus = "Wifi NO"
MAX_WIFI_RETRIES = 3
WIFI_RETRY_DELAY = 5  # Seconds


# Define the GPIO pin connected to the LED
led_pin = board.GP22
# Initialize the GPIO pin as an output
led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT



# Define a list to track currently pressed keys for each keypad
pressed_keys_keypad1 = []
pressed_keys_keypad2 = []



################################################################
#Starting Display

displayio.release_displays()


sda, scl = board.GP16, board.GP17

i2c = busio.I2C(scl, sda)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)




################################################################
# Function to center text on the display

def create_centered_label(font, text, display_width, y_position, color):
    text_area = label.Label(font, text=text, color=color)
    
    # Calculate the text width
    text_width = text_area.bounding_box[2]
    
    # Calculate positions to center the text on the x-axis
    x = (display_width - text_width) // 2
    
    # Set the position of the text area
    text_area.x = x
    text_area.y = y_position
    
    return text_area


################################################################
# Function to update the label text and re-center it

def update_label_text(label, new_text, width):
    label.text = new_text
    x = (width - label.bounding_box[2]) // 2
    label.x = x

################################################################


async def handle_http_requests():
    try:
        while True:
            # Process any waiting requests
            pool_result = server.poll()

            if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
                # Do something only after handling a request
                pass

            await async_sleep(0)
    except Exception as e:
        print("no WIFI connection")
        

################################################################
""" 
    if wifi.radio.connected:
        WifiStatus = "Wifi con"
        thirdline_label.text = WifiStatus + "     Now:" + str(current_runtime)
        print("Wifi status: " + str(wifi.radio.connected))
    else:
        WifiStatus = "Wifi dis"
        thirdline_label.text = WifiStatus + "     Now:" + str(current_runtime)
        print("Wifi status: " + str(wifi.radio.connected))
    pass
"""
# Global variable to track WifiStatus variation
wifi_status_variation = 0

def checkWifiAlive():
    global wifi_status_variation  # Use the global variable

    # List of WifiStatus variations for connected and disconnected states
    wifi_status_list = ["Wifi-con", "Wifi/con", "Wifi+con", "Wifi\\con"]
    wifi_status_list2 = ["Wifi-dis", "Wifi/dis", "Wifi+dis", "Wifi\\dis"]

    # Get IP address for google.at
    host = "www.google.at"
    try:
        addr_info = pool.getaddrinfo(host, 80)[0]  # Get IP address (port 80 for HTTP)
        addr = addr_info[4][0]
        print(f"Pinging {host} ({addr})...")

        # Measure ping time
        start_time = time.monotonic()
        with pool.socket(pool.AF_INET, pool.SOCK_STREAM) as s:
            s.connect((addr, 80))  # Establish TCP connection to Google's server
            end_time = time.monotonic()
        print(f"Ping successful! Time: {end_time - start_time:.4f} seconds")
        
        # Update WifiStatus with the current variation for connected state
        WifiStatus = wifi_status_list[wifi_status_variation]
        
        # Increment and cycle through the list
        wifi_status_variation = (wifi_status_variation + 1) % len(wifi_status_list)

        # Update the display label
        thirdline_label.text = WifiStatus + "     Now:" + str(current_runtime)

    except Exception as e:
        # Update WifiStatus with the current variation for disconnected state
        WifiStatus = wifi_status_list2[wifi_status_variation]
        
        # Increment and cycle through the list
        wifi_status_variation = (wifi_status_variation + 1) % len(wifi_status_list2)
        
        # Update the display label
        thirdline_label.text = WifiStatus + "     Now:" + str(current_runtime)
        print(f"Failed to ping {host}: {e}")


################################################################ 

def get_weather():
    global temperature_celsius, humidity

    if WifiStatus == "Wifi con":
        
        url = "http://api.openweathermap.org/data/2.5/weather?q=Wels,AT&appid=513deb54b6b7f25ce82cf1de9366c104"

        pool = socketpool.SocketPool(wifi.radio)  # Assuming wifi.radio is already connected
        requests = adafruit_requests.Session(pool, ssl.create_default_context())

        try:
            # Fetch weather data from OpenWeatherMap API
            response = requests.get(url)
            response_as_json = response.json()

            # Extract relevant information from the JSON response
            temperature_kelvin = response_as_json['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            humidity = response_as_json['main']['humidity']

            # Print the temperature and humidity
            print("Temperature: %.2f°C" % temperature_celsius)
            print("Humidity: %s%%" % humidity)

            secondline_label.text = f"{temperature_celsius:.0f}°C/{humidity}%       L: {str(layer)}"


        except Exception as e:
            print("Error:", str(e))


################################################################        


async def time_date():
    global formatted_time, formatted_date, date_time_refresh, ntp_time

    if WifiStatus == "Wifi con":

        if time.monotonic() - date_time_refresh >= DATE_TIME_REFRESH_TIME:

            if ntp_time is None:
                try:
                    # Get the datetime from the NTP server
                    ntp_time = ntp.datetime
                    ntp_time = time.localtime(time.mktime(ntp_time) + 3600)
                except Exception as e:
                    print("no WIFI connection / NTP not working")
                    date_time_refresh = time.monotonic()
            
            if ntp_time is not None:

                ntp_time = time.localtime(time.mktime(ntp_time) + 60)

                # Format the time as "HH:MM"
                formatted_time = "{:02d}:{:02d}".format(ntp_time.tm_hour, ntp_time.tm_min)
                # Format the date as "DD.MM.YYYY"
                formatted_date = "{:02d}.{:02d}.{:04d}".format(ntp_time.tm_mday, ntp_time.tm_mon, ntp_time.tm_year)

                # Print the formatted time and date
                print("Time:", formatted_time)
                print("Date:", formatted_date)

                date_time_refresh = time.monotonic()

                return formatted_time, formatted_date



################################################################        

async def gc_collecting():
    global gc_refresh

    if time.monotonic() - gc_refresh >= GC_REFRESH_TIME:
        #show memory used:
        print("freemem before gc: ", gc.mem_free())
        gc.collect()
        print("freemem after gc: ", gc.mem_free())
        gc_refresh = time.monotonic()        

################################################################
        
        
async def power_save():
    global energy_save, energy_mod

    if time.monotonic() - energy_save >= ENERGY_SAVE_REFRESH_TIME:
        
        energy_mod = 1
        display_off()
        #cpu_low_power()
        checkWifiAlive()
        get_weather()
        save_to_storage()
        
        energy_save = time.monotonic()


################################################################

def power_save_off():
    #cpu_full_power()

    if display_off_manually == 0:
        display_on()


################################################################

def display_off():
    global display_is_on
        
    display_is_on = False
    save_mode = displayio.Group()
    display.root_group = save_mode
    display.refresh()
    lighting_off()


################################################################

def display_on():
        global display_is_on

        display_is_on = True
        display_main()
        lighting_on()


################################################################


def lighting_on():
    led.value = True

################################################################

def lighting_off():
    led.value = False

################################################################

def caps_off():
    global caps_is_on
    caps_is_on = False
    firstline_label.text = Codeversion + "    Caps:OFF"

################################################################

def caps_on():
    global caps_is_on
    caps_is_on = True
    firstline_label.text = Codeversion + "    Caps:ON"

################################################################



def display_main():
    global maindpgroup, firstline_label, secondline_label, thirdline_label, fourthtline_label

    maindpgroup = displayio.Group()

    firstline_label = label.Label(terminalio.FONT, text=Codeversion +"    Caps:OFF", color=0xFFFF00, x=0, y=7)
    secondline_label = label.Label(terminalio.FONT, text=f"{temperature_celsius:.0f}°C/{humidity}%       L: {str(layer)}", color=0xFFFF00, x=0, y=22)
    thirdline_label = label.Label(terminalio.FONT, text= WifiStatus + "     Now:" + str(current_runtime), color=0xFFFF00, x=0, y=37)
    fourthtline_label = label.Label(terminalio.FONT, text=formatted_date + "    " + formatted_time, color=0xFFFF00, x=0, y=52)

    maindpgroup.append(secondline_label)
    maindpgroup.append(firstline_label)
    maindpgroup.append(thirdline_label)
    maindpgroup.append(fourthtline_label)        

    display.root_group = maindpgroup
    #display.refresh()




################################################################

#  Read/Writer:

# Function to read all-time runtime from file
def read_from_storage():
    global alltime_runtime, alltime_keypress

    try:
        with open(FILENAME_RUNTIME, "r") as file:
            alltime_runtime = int(file.read())
        with open(FILENAME_KEYPRESS, "r") as file:
            alltime_keypress = int(file.read())

    except Exception as e:
        print("Error reading file:", e)
        return 0
    

################################################################



def save_to_storage():
    global runtime_refresh, current_runtime, alltime_runtime, alltime_keypress, current_keypress, templastcurrentkeypresses, last_save_time

    # Check if this is the first time running the function
    if 'last_save_time' not in globals():
        last_save_time = time.monotonic()

    # Calculate the time passed since the last time this function was called (in seconds)
    time_now = time.monotonic()
    time_elapsed = time_now - last_save_time  # Time elapsed in seconds



    # Check if a full minute has passed
    if time_elapsed >= 60:  # Only consider full minutes (60 seconds)
        try:
            # Calculate the number of full minutes that have passed
            minutes_elapsed = int(time_elapsed // 60)  # Get full minutes
            current_runtime += minutes_elapsed
            alltime_runtime += minutes_elapsed

            # Update keypresses
            alltime_keypress += current_keypress - templastcurrentkeypresses
            templastcurrentkeypresses = current_keypress

            # Save all-time runtime and keypresses to files
            try:
                with open(FILENAME_RUNTIME, "w") as file:
                    file.write(str(alltime_runtime))

                with open(FILENAME_KEYPRESS, "w") as file:
                    file.write(str(alltime_keypress))

            except Exception as e:
                print("Skipping file write. Read-only filesystem:", e)

            # Update the last save time, subtracting any remaining seconds (less than a minute)
            last_save_time = time_now - (time_elapsed % 60)  # Subtract remaining seconds

        except Exception as e:
            print("Error in save_to_storage:", e)

        # Optionally print the results for debugging
        print("All-time Keypresses:", alltime_keypress)
        print("All-time Runtime (in minutes):", alltime_runtime)





################################################################


async def display_refresh_cpu():
    global display_delay_1, cpu_temp
    if time.monotonic() - display_delay_1 >= DISPLAY_REFRESH_TIME_1:
        cpu_temp = microcontroller.cpu.temperature
        firstline_label.text = "CPU Temp:    " + "{:.2f}".format(cpu_temp) + " °C"
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_1 = time.monotonic()


################################################################

async def display_refresh_current_runtime():

    global current_runtime
    global display_delay_2

    if time.monotonic() - display_delay_2 >= DISPLAY_REFRESH_TIME_2:
        thirdline_label.text = WifiStatus + "     Now:" + str(current_runtime)
        
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_2 = time.monotonic()


################################################################

async def display_refresh_date_time():

    global alltime_runtime, display_delay_3, formatted_time, formatted_date

    if time.monotonic() - display_delay_3 >= DISPLAY_REFRESH_TIME_3:

        fourthtline_label.text = formatted_date + "    " + formatted_time
        
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_3 = time.monotonic()

        
        
################################################################
 
    


def handle_keypad1():
    """Handle key presses for keypad 1."""
    global last_key_press_time_keypad1, pressed_keys_keypad1, layer, display_delay, energy_save, maindpgroup, energy_mod, secondline_label, current_keypress, key_141_pressed, key_131_pressed

    if time.monotonic() - last_key_press_time_keypad1 >= DEBOUNCE_TIME_KEYPAD1:
        keys = keypad.pressed_keys
        for key in keys:
            if key not in pressed_keys_keypad1:
                current_keypress += 1
                energy_save = time.monotonic()
                if energy_mod == 1:
                    power_save_off()
                    energy_mod = 0

                # display_delay = time.monotonic()
                if layer == 1:
                    if key in key_mappings_keypad1:
                        if key == "151":
                            layer = 2
                            secondline_label.text = f"{temperature_celsius:.0f}°C/{humidity}%       L: {str(layer)}"
                            pressed_keys_keypad1.append("151")
                        else:
                            kbd.press(key_mappings_keypad1[key])
                            pressed_keys_keypad1.append(key)

                if layer == 2:
                    if key in key_mappings_keypad1_layer2:

                        if key == "141":
                            if key_141_pressed == False:
                                pressed_keys_keypad1.append("141")
                                mouse.press(Mouse.LEFT_BUTTON)
                                key_141_pressed = True
                                

                        elif key == "131":
                            if key_131_pressed == False:
                                pressed_keys_keypad1.append("131")
                                mouse.press(Mouse.RIGHT_BUTTON)
                                key_131_pressed = True

                        elif key == "143":
                            mouse.click(Mouse.LEFT_BUTTON)
                            
                        
                        elif key == "133":
                            mouse.move(x=-3, y=0)

                        elif key == "132":
                            mouse.move(x=3, y=0)

                        elif key == "122":
                            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                            cc.release()

                        elif key == "123":
                            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                            cc.release()
                            
                        elif key == "121":
                            microcontroller.reset()
                            
                        elif isinstance(key_mappings_keypad1_layer2[key], tuple):
                            for keycode in key_mappings_keypad1_layer2[key]:
                                kbd.press(keycode)
                        else:
                            if key == "151":
                                pass
                            else:
                                kbd.press(key_mappings_keypad1_layer2[key])
                                pressed_keys_keypad1.append(key)

        for key in pressed_keys_keypad1.copy():
            if key not in keys:
                if layer == 1:
                    if key in key_mappings_keypad1:
                        kbd.release(key_mappings_keypad1[key])
                        pressed_keys_keypad1.remove(key)

                if layer == 2:
                    if key == "151":
                        layer = 1
                        secondline_label.text = f"{temperature_celsius:.0f}°C/{humidity}%       L: {str(layer)}"
                        pressed_keys_keypad1.remove("151")
                        kbd.release_all()
                        
                        # Release Mouse buttons left and right when exiting layer before releasing buttons!
                        if key_141_pressed == True:
                            mouse.release(Mouse.LEFT_BUTTON)
                            key_141_pressed = False
                            pressed_keys_keypad1.remove("141")
                        elif key_131_pressed == True:
                            mouse.release(Mouse.RIGHT_BUTTON)
                            key_131_pressed = False
                            pressed_keys_keypad1.remove("131")
                        

                    elif key == "141":
                        if key_141_pressed == True:
                            mouse.release(Mouse.LEFT_BUTTON)
                            key_141_pressed = False
                            pressed_keys_keypad1.remove("141")
                    
                    elif key == "131":
                        if key_131_pressed == True:
                            mouse.release(Mouse.RIGHT_BUTTON)
                            key_131_pressed = False
                            pressed_keys_keypad1.remove("131")

                    else:
                        if key in key_mappings_keypad1_layer2:
                            if isinstance(key_mappings_keypad1_layer2[key], tuple):
                                for keycode in reversed(key_mappings_keypad1_layer2[key]):
                                    kbd.release(keycode)
                            else:
                                kbd.release(key_mappings_keypad1_layer2[key])
                        pressed_keys_keypad1.remove(key)

        last_key_press_time_keypad1 = time.monotonic()


################################################################

def handle_keypad2():
    """Handle key presses for keypad 2."""
    global last_key_press_time_keypad2, pressed_keys_keypad2, layer, display_delay, energy_save, layer_fixed, maindpgroup, energy_mod, secondline_label, current_keypress, display_is_on, caps_is_on

    if time.monotonic() - last_key_press_time_keypad2 >= DEBOUNCE_TIME_KEYPAD2:

        keys1 = keypad1.pressed_keys
        for key in keys1:
            if key not in pressed_keys_keypad2:
                
                current_keypress += 1
                energy_save = time.monotonic()
                if energy_mod == 1:
                    power_save_off()
                    energy_mod = 0

                #display_delay = time.monotonic()
                if layer == 1:
                    if key in key_mappings_keypad2:
                        if key == "233":
                            layer = 2
                            secondline_label.text = f"{temperature_celsius:.0f}°C/{humidity}%       L: {str(layer)}"
                            pressed_keys_keypad2.append("233")
                            

                        else:
                            kbd.press(key_mappings_keypad2[key])
                            pressed_keys_keypad2.append(key)

                if layer == 2:
                    if key in key_mappings_keypad2_layer2:
                        if key == "212":
                            mouse.move(wheel=1)
                        
                        elif key == "213":
                            mouse.move(wheel=-1)

                        elif key == "223":
                            mouse.move(x=0, y=5)

                        elif key == "222":
                            mouse.move(x=0, y=-5)

                            
                        elif key == "232":
                            if caps_is_on == True:
                                caps_off()
                                caps_is_on = False
                                kbd.press(Keycode.CAPS_LOCK)
                                pressed_keys_keypad2.append("232")
                            elif caps_is_on == False:
                                caps_on()
                                caps_is_on = True
                                kbd.press(Keycode.CAPS_LOCK)
                                pressed_keys_keypad2.append("232")

                        elif key == "215":
                            cc.send(ConsumerControlCode.MUTE)
                            cc.release()
                            #TEST this part
                            #pressed_keys_keypad1.append("215")


                        elif key == "233":
                            if layer_fixed == 1:
                                layer_fixed = 0
                                layer = 1
                                secondline_label.text = f"{temperature_celsius:.0f}°C/{humidity}%       L: {str(layer)}"
                                #SLEEP/DELAY for changing layer fix!!!!
                                time.sleep(0.5)

                        elif key == "242":
                            save_to_storage()
                            checkWifiAlive()
                            get_weather()


                        elif key == "243":
                            if display_is_on == True:
                                display_off()
                                display_is_on = False
                            elif display_is_on == False:
                                display_on()
                                display_is_on = True
                            

                        elif isinstance(key_mappings_keypad2_layer2[key], tuple):
                            for keycode in key_mappings_keypad2_layer2[key]:
                                kbd.press(keycode)

                        else:
                        
                            kbd.press(key_mappings_keypad2_layer2[key])
                            pressed_keys_keypad2.append(key)

        for key in pressed_keys_keypad2.copy():
            if key not in keys1:
                if layer == 1:
                    if key in key_mappings_keypad2:
                        kbd.release(key_mappings_keypad2[key])
                        pressed_keys_keypad2.remove(key)

                if layer == 2:
                    if key in key_mappings_keypad2_layer2:
                        if key == "233":
                            
                            pressed_keys_keypad2.remove("233")
                            layer_fixed = 1
                            

                        else:
                            kbd.release(key_mappings_keypad2_layer2[key])
                            pressed_keys_keypad2.remove(key)

        last_key_press_time_keypad2 = time.monotonic()


################################################################
################################################################
################################################################
################################################################


# Pre start:



# Define the labels and their initial text
            
startdpgroup = displayio.Group()  # Clear the existing Group and create a new one
one = label.Label(terminalio.FONT, text=" MM-Dactyl", color=0xFFFF00, x=0, y=10, scale=2)
two = create_centered_label(terminalio.FONT, "ModelNr: 3-02", 128, 29, 0xFFFF00)
three = create_centered_label(terminalio.FONT,"test",  128, 48, 0xFFFF00)

        
# Add the labels to the splash Group
startdpgroup.append(one)
startdpgroup.append(two)
startdpgroup.append(three)


display.root_group = startdpgroup

################################################################

#Wireless Setup



ssid = WlanSSID_Secret
password = WlanPW_Secret



display_html_power = False  # Initialize display power variable

try:
    print("try to con", ssid)
    update_label_text(three, "try to " + ssid, 128)

    #Set hostname
    wifi.radio.hostname = custom_hostname



    for attempt in range(MAX_WIFI_RETRIES):
        try:
            wifi.radio.connect(ssid, password)
            print("success to", ssid)
            update_label_text(three, "con to " + ssid, 128)
            WifiStatus = "Wifi con"

        except Exception as e:
            update_label_text(three, "try " + str(attempt) + " to " + ssid, 128)
            time.sleep(WIFI_RETRY_DELAY)


    if WifiStatus == "Wifi con":
        pool = socketpool.SocketPool(wifi.radio)
        server = Server(pool, "/static", debug=True)
        ntp = adafruit_ntp.NTP(pool, tz_offset=1)

    

        @server.route("/data", methods=["GET", "POST"])  # Allow POST requests
        def runtime_data(request: Request):
            global current_runtime, alltime_runtime, layer, display_html_power, display_off_manually, formatted_time

            if request.method == "POST":
                try:
                    data = request.json()
                    display_html_power = data.get("display_html_power", False)
                    print("Display HTML Power:", display_html_power)
                    if display_html_power == True:
                        display_off_manually = 1
                        display_off()
                    if display_html_power == False:
                        display_on()
                        display_off_manually = 0
                except Exception as e:
                    print("Error processing POST request:", e)
            
            data = {
                "cpu_speed": microcontroller.cpu.frequency / 1000000,
                "cpu_temp": microcontroller.cpu.temperature,
                "runtime_now": current_runtime,
                "runtime_all": str("{:.0f}".format(alltime_runtime / 60)),
                "keypress_now": current_keypress,
                "keypress_all": alltime_keypress,
                "layer": layer,
                "display_html_power": display_html_power,  # Include display power state in response,
                "keyboard_time": formatted_date + "  " + formatted_time,
                "Codeversion": Codeversion
            }
            return Response(request, json.dumps(data), content_type="application/json")
        
        @server.route("/wifi", methods=["POST"])
        def wifi_toggle(request: Request):
            try:
                data = request.json()


                pass
        
                
            except Exception as e:
                print("Error toggling WiFi:", e)
            return Response(request, "{}", content_type="application/json")


        # Start the server.
        
        server.start(str(wifi.radio.ipv4_address))
        update_label_text(three, "IP: " + str(wifi.radio.ipv4_address), 128)


        try:
            print("--------------------------------------------------------------")
            print("WIFI full Informations:")
            print("IP Address:", str(wifi.radio.ipv4_address))
            print("Subnet:", str(wifi.radio.ipv4_subnet))
            print("Gateway:", str(wifi.radio.ipv4_gateway))
            print("DNS:", str(wifi.radio.ipv4_dns))
            print("Wi-Fi is connected:", str(wifi.radio.connected))
            print("--------------------------------------------------------------")
        except:
            print("wifi readout not working")
        
        time.sleep(1)

except Exception as e:
    print(f"Wi-Fi connection failed: {e}")
    update_label_text(three, "not con to " + ssid, 128)
    WifiStatus = "Wifi dis"

    

################################################################
################################################################
################################################################
################################################################
        

#set refresh earlier to refresh display data for initialisation
display_delay_1 = time.monotonic() - 59
display_delay_2 = time.monotonic() - 60
display_delay_3 = time.monotonic() - 340

print("freemem all loaded gc: ", gc.mem_free())

display_main()    

get_weather()

read_from_storage()

#start timer
save_to_storage()

lighting_on()

################################################################


async def main():

    create_task(handle_http_requests()),
    
    while True:
        await gc_collecting()
        await time_date()
        await power_save()
        await display_refresh_current_runtime()  # Await display_refresh()
        await display_refresh_date_time()  # Await display_refresh()

        #await display_refresh_cpu()

        handle_keypad1()
        handle_keypad2()
        await asyncio.sleep(0.01)  # Ensure event loop runs smoothly
    

# Create and run the event loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
    
except KeyboardInterrupt:
    pass
finally:
    loop.close()




