import time
import digitalio
import board
import usb_hid
import adafruit_matrixkeypad
import microcontroller
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import board, busio, displayio, os, terminalio
import adafruit_displayio_ssd1306
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import asyncio
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import socketpool
import wifi
from asyncio import create_task, sleep as async_sleep
import json
from adafruit_httpserver import Server, REQUEST_HANDLED_RESPONSE_SENT, Request, FileResponse, Response
import adafruit_ntp
import gc



# TODO start and stop webserver / WIFI over button and in energy saving Mode





#Setting to orignal herz
microcontroller.cpu.frequency = 125000000

# Set up a keyboard/mouse device.
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# Define the columns and rows using GPIO pins.
cols = [digitalio.DigitalInOut(x) for x in (board.GP0, board.GP1, board.GP2, board.GP19, board.GP20, board.GP21)]
rows = [digitalio.DigitalInOut(x) for x in (board.GP3, board.GP4, board.GP5, board.GP10, board.GP11)]

# Define the keys for the matrix.
keys = (("111", "112", "113", "114", "115", "116"),
        ("121", "122", "123", "124", "125", "126"),
        ("131", "132", "133", "134", "135", "136"),
        ("141", "142", "143", "144", "145", "146"),
        ("151", "152", "153", "154", "155", "156"))

keys1 = (("211", "212", "213", "214", "215"),
         ("221", "222", "223", "224", "225"),
         ("231", "232", "233", "234", "235"),
         ("241", "242", "243", "244", "245"),
         ("251", "252", "253", "254", "255"),
         ("261", "262", "263", "264", "265"))

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
DISPLAY_REFRESH_TIME_STARTER = 5 # Asynchron for better performance
DISPLAY_REFRESH_TIME_1 = 61 # Asynchron for better performance
DISPLAY_REFRESH_TIME_2 = 62 # Asynchron for better performance
DISPLAY_REFRESH_TIME_3 = 353 # Asynchron for better performance

# MIXED
cpu_temp = 0
runtime_now = time.monotonic()
runtime_refresh = time.monotonic()
current_runtime = 0
alltime_runtime = 0
RUNTIME_REFRESH_TIME = 300 # five minutes update runtime
FILENAME_RUNTIME = "/runtime.txt"
FILENAME_KEYPRESS = "/keypress.txt"
ENERGY_SAVE_REFRESH_TIME = 380
DATE_TIME_REFRESH_TIME = 63
GC_REFRESH_TIME = 310
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



# Define a list to track currently pressed keys for each keypad
pressed_keys_keypad1 = []
pressed_keys_keypad2 = []

# Define key mappings
key_mappings_keypad1 = {
    "111": Keycode.FIVE,
    "112": Keycode.THREE,#
    "113": Keycode.ONE,#
    "114": Keycode.BACKSPACE,#
    "115": Keycode.NINE,#
    "116": Keycode.SEVEN,#
    "121": Keycode.T,#
    "122": Keycode.E,#
    "123": Keycode.Q,#
    "124": Keycode.BACKSLASH,#
    "125": Keycode.O,#
    "126": Keycode.U,#
    "131": Keycode.G,#
    "132": Keycode.D,#
    "133": Keycode.A,#
    "134": Keycode.QUOTE,#
    "135": Keycode.L,#
    "136": Keycode.J,#
    "141": Keycode.B,#
    "142": Keycode.C,#
    "143": Keycode.Z,#
    "144": Keycode.RIGHT_SHIFT,#
    "145": Keycode.PERIOD,#
    "146": Keycode.M,#
    "151": "151",#
    "152": Keycode.RIGHT_ALT,#
    "153": Keycode.LEFT_GUI,#
    "154": Keycode.MINUS,
    "155": Keycode.LEFT_BRACKET,
    "156": Keycode.ENTER,
}

key_mappings_keypad2 = {
    "211": Keycode.FOUR,#
    "212": Keycode.R,#
    "213": Keycode.F,#
    "214": Keycode.V, #
    "215": Keycode.SPACE,#
    "221": Keycode.TWO,#
    "222": Keycode.W,#
    "223": Keycode.S,#
    "224": Keycode.X,#
    "225": Keycode.LEFT_ALT,
    "231": Keycode.ESCAPE,#
    "232": Keycode.TAB,#,
    "233": "233", #
    "234": Keycode.LEFT_SHIFT,#
    "235": Keycode.LEFT_CONTROL,#
    "241": Keycode.ZERO,#
    "242": Keycode.P,#
    "243": Keycode.SEMICOLON,#
    "244": Keycode.FORWARD_SLASH,#
    "245": Keycode.RIGHT_BRACKET,#
    "251": Keycode.EIGHT,#
    "252": Keycode.I,#
    "253": Keycode.K,#
    "254": Keycode.COMMA,#
    "255": Keycode.EQUALS,#
    "261": Keycode.SIX,#
    "262": Keycode.Y,#
    "263": Keycode.H,#
    "264": Keycode.N,#
    "265": Keycode.SPACE,#
}

# Define layer 2 key mappings
key_mappings_keypad1_layer2 = {
    "111": Keycode.F5,
    "112": Keycode.F3,#
    "113": Keycode.F1,#
    "114": Keycode.BACKSPACE,#
    "115": Keycode.F9,#
    "116": Keycode.F7,#
    "121": Keycode.T,#
    "122": "122",#
    "123": "123",#
    "124": Keycode.F11,#
    "125": Keycode.PAGE_DOWN,#
    "126": Keycode.PAGE_UP,#
    "131": "131",#
    "132": "132",#
    "133": "133",#
    "134": Keycode.F12,#
    "135": Keycode.RIGHT_ARROW,#
    "136": Keycode.LEFT_ARROW,#
    "141": "141",
    "142": Keycode.C,#
    "143": Keycode.Z,#
    "144": Keycode.RIGHT_SHIFT,#
    "145": Keycode.GRAVE_ACCENT,#
    "146": Keycode.M,#
    "151": "151",# FN Change Hold
    "152": Keycode.RIGHT_ALT,#
    "153": Keycode.LEFT_GUI,#
    "154": Keycode.DELETE,
    "155": Keycode.LEFT_BRACKET,
    "156": Keycode.ENTER,
}

key_mappings_keypad2_layer2 = {
    "211": Keycode.F4,#
    "212": "212",#
    "213": "213",#
    "214": Keycode.V, #
    "215": Keycode.SPACE,#
    "221": Keycode.F2,#
    "222": "222",#
    "223": "223",#
    "224": Keycode.X,#
    "225": Keycode.LEFT_ALT,
    "231": Keycode.ESCAPE,#
    "232": Keycode.TAB,#,
    "233": "233", # FN Change
    "234": Keycode.LEFT_SHIFT,#
    "235": Keycode.LEFT_CONTROL,#
    "241": Keycode.F10,#
    "242": 242,# Display
    "243": Keycode.SEMICOLON,#
    "244": Keycode.KEYPAD_BACKSLASH,#
    "245": Keycode.RIGHT_BRACKET,#
    "251": Keycode.F8,#
    "252": Keycode.UP_ARROW,#
    "253": Keycode.DOWN_ARROW,
    "254": Keycode.COMMA,#
    "255": Keycode.EQUALS,#
    "261": Keycode.F6,#
    "262": Keycode.INSERT,#
    "263": Keycode.HOME,#
    "264": Keycode.END,#
    "265": Keycode.SPACE,#
}

################################################################
#Starting Display

displayio.release_displays()

sda, scl = board.GP16, board.GP17    
i2c = busio.I2C(scl, sda)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)



################################################################

#Wireless Setup

startdproup = displayio.Group()

info = label.Label(terminalio.FONT, text="Startup", color=0xFFFF00, x=0, y=30)
startdproup.append(info)        
display.show(startdproup)


ssid = os.getenv("H_WIFI_SSID")
password = os.getenv("H_WIFI_PASSWORD")

display_html_power = False  # Initialize display power variable

try:
    print("try to con", ssid)
    info.text = "try to " + ssid
    wifi.radio.connect(ssid, password)
    print("success to", ssid)
    info.text = "con to " + ssid
    time.sleep(2)

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
            "keyboard_time": formatted_date + "  " + formatted_time
        }
        return Response(request, json.dumps(data), content_type="application/json")

    # Start the server.
    server.start(str(wifi.radio.ipv4_address))
    info.text = "IP: " + str(wifi.radio.ipv4_address)
    time.sleep(2)

except Exception as e:
    print("no WIFI connection")
    info.text = "not con to " + ssid
    time.sleep(2)

    

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
        

async def time_date():
    global formatted_time, formatted_date, date_time_refresh

    if time.monotonic() - date_time_refresh >= DATE_TIME_REFRESH_TIME:

        try:
            # Get the datetime from the NTP server
            ntp_time = ntp.datetime
            
            # Format the time as "HH:MM"
            formatted_time = "{:02d}:{:02d}".format(ntp_time.tm_hour, ntp_time.tm_min)
            # Format the date as "DD.MM.YYYY"
            formatted_date = "{:02d}.{:02d}.{:04d}".format(ntp_time.tm_mday, ntp_time.tm_mon, ntp_time.tm_year)

            # Print the formatted time and date
            print("Time:", formatted_time)
            print("Date:", formatted_date)

            date_time_refresh = time.monotonic()

            return formatted_time, formatted_date
    
        except Exception as e:
            print("no WIFI connection / NTP not working")
            date_time_refresh = time.monotonic()


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
        cpu_low_power()
        
        energy_save = time.monotonic()


################################################################

def power_save_off():
    cpu_full_power()
    if display_off_manually == 0:
        display_on()


################################################################

def cpu_low_power():
    cpu_frequency_mhz = microcontroller.cpu.frequency
    print("old CPU Frequency:", cpu_frequency_mhz, "Hz")
    # Set CPU frequency to 65 MHz
    microcontroller.cpu.frequency = 65000000
    cpu_frequency_mhz = microcontroller.cpu.frequency
    print("now CPU Frequency:", cpu_frequency_mhz, "Hz")


################################################################
    
def cpu_full_power():
    cpu_frequency_mhz = microcontroller.cpu.frequency
    print("old CPU Frequency:", cpu_frequency_mhz, "Hz")
    microcontroller.cpu.frequency = 125000000
    cpu_frequency_mhz = microcontroller.cpu.frequency
    print("now CPU Frequency:", cpu_frequency_mhz, "Hz")


################################################################

def display_off():
    save_mode = displayio.Group()
    display.show(save_mode)
    display.refresh()


################################################################

def display_on():
        display_main()


################################################################


def display_main():
    global display_delay_1, maindpgroup, cpu_label, layer_label, runtime_now_label, keypress_now_label, formatted_time

    maindpgroup = displayio.Group()

    cpu_label = label.Label(terminalio.FONT, text="CPU Temp:    " + "{:.2f}".format(cpu_temp) + " °C", color=0xFFFF00, x=0, y=7)
    layer_label = label.Label(terminalio.FONT, text="Layer:          " + str(layer), color=0xFFFF00, x=0, y=22)
    runtime_now_label = label.Label(terminalio.FONT, text="Runtime now:  " + str(current_runtime) + "min", color=0xFFFF00, x=0, y=37)
    keypress_now_label = label.Label(terminalio.FONT, text=formatted_date + "    " + formatted_time, color=0xFFFF00, x=0, y=52)
  
    maindpgroup.append(layer_label)
    maindpgroup.append(cpu_label)
    maindpgroup.append(runtime_now_label)
    maindpgroup.append(keypress_now_label)        

    display.show(maindpgroup)
    #display.refresh()




################################################################

#  Read/Writer:

# Function to read all-time runtime from file
def read_alltime_runtime():
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

# Function to save all-time runtime/keypress to file
def save_alltime_runtime():
    global runtime_refresh, current_runtime, alltime_runtime, cpu_temp, alltime_keypress, current_keypress, templastcurrentkeypresses


    if time.monotonic() - runtime_refresh >= RUNTIME_REFRESH_TIME:
        try:
            
            current_runtime += 5
            alltime_runtime += 5

            

            alltime_keypress += current_keypress - templastcurrentkeypresses
            templastcurrentkeypresses = current_keypress

            with open(FILENAME_RUNTIME, "w") as file:
                file.write(str(alltime_runtime))

            with open(FILENAME_KEYPRESS, "w") as file:
                file.write(str(alltime_keypress))
            


        except Exception as e:
            print("Error writing to file:", e)
        runtime_refresh = time.monotonic()

################################################################


    

async def display_start():
    global cpu_label, layer_label, runtime_now_label, keypress_now_label, maindpgroup, formatted_time, formatted_date, ntp_time

    try:
        ntp_time = ntp.datetime    
        # Format the time as "HH:MM"
        formatted_time = "{:02d}:{:02d}".format(ntp_time.tm_hour, ntp_time.tm_min)
        # Format the date as "DD.MM.YYYY"
        formatted_date = "{:02d}.{:02d}.{:04d}".format(ntp_time.tm_mday, ntp_time.tm_mon, ntp_time.tm_year)
    except Exception as e:
        print("_no WIFI connection / NTP not working")

    # Define the labels and their initial text
            
    startdpgroup = displayio.Group()  # Clear the existing Group and create a new one
    one = label.Label(terminalio.FONT, text="     MM - Dactyl", color=0xFFFF00, x=0, y=15)
    two = label.Label(terminalio.FONT, text="    ModelNr: 3-02", color=0xFFFF00, x=0, y=33)

        
    # Add the labels to the splash Group
    startdpgroup.append(one)
    startdpgroup.append(two)

    display.show(startdpgroup)
        
    # ----------------------- Progress BAR ---------------------------
    # Define progress bar parameters
    progress_bar_width = 100
    progress_bar_height = 10
    progress_bar_x = 14
    progress_bar_y = 50  # Adjusted y position
    progress_color = 0x00FF00  # Green

    # Create the progress bar background
    background_rect = Rect(progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height, fill=0x000000)
    startdpgroup.append(background_rect)

    # Calculate step size for filling the progress bar in 2 seconds
    step_size = progress_bar_width / 20  # 60 steps for 2 seconds

    # Fill the progress bar
    for i in range(20):
        progress_width = i * step_size
        progress_rect = Rect(progress_bar_x, progress_bar_y, max(1, int(progress_width)), progress_bar_height, fill=progress_color)
        startdpgroup.append(progress_rect)
        display.refresh()
        time.sleep(0.033)  # 1/30th of a second for smooth animation
        startdpgroup.remove(progress_rect)

    # After filling, display the progress bar fully filled
    full_progress_rect = Rect(progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height, fill=progress_color)
    startdpgroup.append(full_progress_rect)
    display.refresh()


    #------------ display Maingroup


    maindpgroup = displayio.Group()  # Clear the existing Group and create a new one
    # Define the labels and their initial text
    cpu_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=0, y=7)
    layer_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=0, y=22)
    runtime_now_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=0, y=37)
    keypress_now_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=0, y=52)
        
    # Add the labels to the splash Group
    maindpgroup.append(layer_label)
    maindpgroup.append(cpu_label)
    maindpgroup.append(runtime_now_label)
    maindpgroup.append(keypress_now_label)        

    display.show(maindpgroup)

    cpu_temp = microcontroller.cpu.temperature
    
    # Update CPU temperature label
    cpu_label.text = "CPU Temp:    " + "{:.2f}".format(cpu_temp) + " °C"
    # Update layer label
    layer_label.text = "Layer:          " + str(layer)
    # Update runtime now label
    runtime_now_label.text = "Runtime now:  " + str(current_runtime) + "min"
    # Update runtime all label
    keypress_now_label.text = formatted_date + "    " + formatted_time


    

################################################################


async def display_refresh_cpu():
    global display_delay_1, cpu_temp
    if time.monotonic() - display_delay_1 >= DISPLAY_REFRESH_TIME_1:
        cpu_temp = microcontroller.cpu.temperature
        cpu_label.text = "CPU Temp:    " + "{:.2f}".format(cpu_temp) + " °C"
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_1 = time.monotonic()


################################################################

async def display_refresh_current_runtime():

    global current_runtime
    global display_delay_2

    if time.monotonic() - display_delay_2 >= DISPLAY_REFRESH_TIME_2:
        runtime_now_label.text = "Runtime now:  " + str(current_runtime) + "min"
        
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_2 = time.monotonic()


################################################################

async def display_refresh_all_runtime():

    global alltime_runtime, display_delay_3, formatted_time

    if time.monotonic() - display_delay_3 >= DISPLAY_REFRESH_TIME_3:

        keypress_now_label.text = formatted_date + "    " + formatted_time
        
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_3 = time.monotonic()


        
        
################################################################

def handle_keypad1():
    """Handle key presses for keypad 1."""
    global last_key_press_time_keypad1, pressed_keys_keypad1, layer, display_delay, energy_save, maindpgroup, energy_mod, layer_label, current_keypress

    if time.monotonic() - last_key_press_time_keypad1 >= DEBOUNCE_TIME_KEYPAD1:


        keys = keypad.pressed_keys
        for key in keys:
            if key not in pressed_keys_keypad1:
                
                current_keypress += 1
                energy_save = time.monotonic()
                if energy_mod == 1:
                    power_save_off()
                    energy_mod = 0

                #display_delay = time.monotonic()
                if layer == 1:
                    if key in key_mappings_keypad1:
                        if key == "151":
                            layer = 2
                            layer_label.text = "Layer:          " + str(layer)
                            pressed_keys_keypad1.append("151")
                        else:
                            kbd.press(key_mappings_keypad1[key])
                            pressed_keys_keypad1.append(key)

                if layer == 2:
                    if key in key_mappings_keypad1_layer2:
                        if key == "141":
                            mouse.click(Mouse.LEFT_BUTTON)
                            #mouse.move(1, 0)

                        elif key == "131":
                            mouse.click(Mouse.RIGHT_BUTTON)
                        
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
                        layer_label.text = "Layer:          " + str(layer)
                        pressed_keys_keypad1.remove("151")
                        kbd.release_all()
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
    global last_key_press_time_keypad2, pressed_keys_keypad2, layer, display_delay, energy_save, layer_fixed, maindpgroup, energy_mod, layer_label, current_keypress

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
                            layer_label.text = "Layer:          " + str(layer)
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

                        
                        elif key == "233":
                            if layer_fixed == 1:
                                layer_fixed = 0
                                layer = 1
                                layer_label.text = "Layer:          " + str(layer)
                                #SLEEP/DELAY for changing layer fix!!!!
                                time.sleep(0.5)

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
async def main():

    read_alltime_runtime()  # Read all-time runtime at startup
    await display_start()
    create_task(handle_http_requests()),
    
    while True:
        await gc_collecting()
        await time_date()
        await power_save()
        await display_refresh_current_runtime()  # Await display_refresh()
        await display_refresh_all_runtime()  # Await display_refresh()
        await display_refresh_cpu()
        handle_keypad1()
        handle_keypad2()
        save_alltime_runtime()
        await asyncio.sleep(0.01)  # Ensure event loop runs smoothly
        




# Create and run the event loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
    
except KeyboardInterrupt:
    pass
finally:
    loop.close()










