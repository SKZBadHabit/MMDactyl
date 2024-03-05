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











# TODO start and stop webserver over button!









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

# Timers
WEB_UPDATE_TIME = 11
web_update = 0
cpu_temp = 0
runtime_now = time.monotonic()
runtime_refresh = time.monotonic()
current_runtime = 0
alltime_runtime = 0
RUNTIME_REFRESH_TIME = 300 # five minutes update runtime
FILENAME = "/runtime.txt"
ENERGY_SAVE_REFRESH_TIME = 180
energy_save = time.monotonic()

energy_mod = 0

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
    "242": Keycode.P,#
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

ssid = os.getenv("H_WIFI_SSID")
password = os.getenv("H_WIFI_PASSWORD")

print("try to", ssid)
wifi.radio.connect(ssid, password)
print("success to", ssid)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

@server.route("/static")
def runtime_data(request: Request):
    global current_runtime, alltime_runtime, cpu_temp, layer
    if time.monotonic() - web_update >= WEB_UPDATE_TIME:
        data = {
            "runtime_now": current_runtime,
            "runtime_all": alltime_runtime,
            "cpu_temp": cpu_temp,
            "layer": layer
        }
        web_update = time.monotonic()
    return Response(request, json.dumps(data), content_type="application/json")



# Start the server.
server.start(str(wifi.radio.ipv4_address))

async def handle_http_requests():
    while True:
        # Process any waiting requests
        pool_result = server.poll()

        if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
            # Do something only after handling a request
            pass

        await async_sleep(0)

################################################################



async def power_save():
    global energy_save, energy_mod

    if time.monotonic() - energy_save >= ENERGY_SAVE_REFRESH_TIME:
        
        energy_mod = 1
        display_off()
        cpu_low_power()
        
        energy_save = time.monotonic()

def power_save_off():
    cpu_full_power()
    display_on()

def cpu_low_power():
    cpu_frequency_mhz = microcontroller.cpu.frequency
    print("old CPU Frequency:", cpu_frequency_mhz, "Hz")
    # Set CPU frequency to 65 MHz
    microcontroller.cpu.frequency = 65000000
    cpu_frequency_mhz = microcontroller.cpu.frequency
    print("now CPU Frequency:", cpu_frequency_mhz, "Hz")
    
def cpu_full_power():
    cpu_frequency_mhz = microcontroller.cpu.frequency
    print("old CPU Frequency:", cpu_frequency_mhz, "Hz")
    microcontroller.cpu.frequency = 125000000
    cpu_frequency_mhz = microcontroller.cpu.frequency
    print("now CPU Frequency:", cpu_frequency_mhz, "Hz")

def display_off():
    save_mode = displayio.Group()
    display.show(save_mode)
    display.refresh()

def display_on():
        display_main()


def display_main():
    global display_delay_1, maindpgroup, cpu_label, layer_label, runtime_now_label, runtime_all_label

    maindpgroup = displayio.Group()

    cpu_label = label.Label(terminalio.FONT, text="CPU Temp:    " + "{:.2f}".format(cpu_temp) + " °C", color=0xFFFF00, x=0, y=7)
    layer_label = label.Label(terminalio.FONT, text="Layer:          " + str(layer), color=0xFFFF00, x=0, y=22)
    runtime_now_label = label.Label(terminalio.FONT, text="Runtime now:   " + str(current_runtime) + "min", color=0xFFFF00, x=0, y=37)
    runtime_all_label = label.Label(terminalio.FONT, text="Runtime all:   " + str("{:.0f}".format(alltime_runtime/60)) + " h", color=0xFFFF00, x=0, y=52)
  
    maindpgroup.append(layer_label)
    maindpgroup.append(cpu_label)
    maindpgroup.append(runtime_now_label)
    maindpgroup.append(runtime_all_label)        

    display.show(maindpgroup)
    #display.refresh()




################################################################

# Runtime Read/Writer:

# Function to read all-time runtime from file
def read_alltime_runtime():
    global alltime_runtime

    try:
        with open(FILENAME, "r") as file:
            alltime_runtime = int(file.read())
    except Exception as e:
        print("Error reading file:", e)
        return 0
    
# Function to save all-time runtime to file
def save_alltime_runtime():
    global runtime_refresh
    global current_runtime
    global alltime_runtime
    global cpu_temp

    if time.monotonic() - runtime_refresh >= RUNTIME_REFRESH_TIME:
        try:
            
            current_runtime += 5
            alltime_runtime += 5

            with open(FILENAME, "w") as file:
                file.write(str(alltime_runtime))

        except Exception as e:
            print("Error writing to file:", e)
        runtime_refresh = time.monotonic()

################################################################


    

async def display_start():
    global cpu_label, layer_label, runtime_now_label, runtime_all_label, maindpgroup

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
    runtime_all_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=0, y=52)
        
    # Add the labels to the splash Group
    maindpgroup.append(layer_label)
    maindpgroup.append(cpu_label)
    maindpgroup.append(runtime_now_label)
    maindpgroup.append(runtime_all_label)        

    display.show(maindpgroup)

    cpu_temp = microcontroller.cpu.temperature
    
    # Update CPU temperature label
    cpu_label.text = "CPU Temp:    " + "{:.2f}".format(cpu_temp) + " °C"
    # Update layer label
    layer_label.text = "Layer:          " + str(layer)
    # Update runtime now label
    runtime_now_label.text = "Runtime now:   " + str(current_runtime) + "min"
    # Update runtime all label
    runtime_all_label.text = "Runtime all:   " + str("{:.0f}".format(alltime_runtime/60)) + " h"


    

################################################################


async def display_refresh_cpu():
    global display_delay_1
    if time.monotonic() - display_delay_1 >= DISPLAY_REFRESH_TIME_1:
        cpu_temp = microcontroller.cpu.temperature
        cpu_label.text = "CPU Temp:    " + "{:.2f}".format(cpu_temp) + " °C"
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_1 = time.monotonic()

async def display_refresh_current_runtime():

    global current_runtime
    global display_delay_2

    if time.monotonic() - display_delay_2 >= DISPLAY_REFRESH_TIME_2:
        runtime_now_label.text = "Runtime now:   " + str(current_runtime) + " min"
        
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_2 = time.monotonic()

async def display_refresh_all_runtime():

    global alltime_runtime
    global display_delay_3

    if time.monotonic() - display_delay_3 >= DISPLAY_REFRESH_TIME_3:

        runtime_all_label.text = "Runtime all:   " + str("{:.0f}".format(alltime_runtime/60)) + " h"
        
        #display.refresh  # Refresh the display to reflect the changes
        display_delay_3 = time.monotonic()


        
        
################################################################

def handle_keypad1():
    """Handle key presses for keypad 1."""
    global last_key_press_time_keypad1, pressed_keys_keypad1, layer, display_delay, energy_save, maindpgroup, energy_mod, layer_label

    if time.monotonic() - last_key_press_time_keypad1 >= DEBOUNCE_TIME_KEYPAD1:


        keys = keypad.pressed_keys
        for key in keys:
            if key not in pressed_keys_keypad1:
                
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
    global last_key_press_time_keypad2, pressed_keys_keypad2, layer, display_delay, energy_save, layer_fixed, maindpgroup, energy_mod, layer_label

    if time.monotonic() - last_key_press_time_keypad2 >= DEBOUNCE_TIME_KEYPAD2:

        keys1 = keypad1.pressed_keys
        for key in keys1:
            if key not in pressed_keys_keypad2:

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

                        elif key == "232":
                            display_off()

                        elif isinstance(key_mappings_keypad2_layer2[key], tuple):
                            for keycode in key_mappings_keypad2_layer2[key]:
                                kbd.press(keycode)

                        elif key == "233":
                            if layer_fixed == 1:
                                layer_fixed = 0
                                layer = 1
                                layer_label.text = "Layer:          " + str(layer)
                                #SLEEP/DELAY for changing layer fix!!!!
                                time.sleep(0.5)
                                

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
    #create_task(handle_http_requests()),
    
    while True:
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






