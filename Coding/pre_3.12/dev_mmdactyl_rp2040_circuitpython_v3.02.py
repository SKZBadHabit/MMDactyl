import time
import digitalio
import board
import usb_hid
import adafruit_matrixkeypad
import microcontroller
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import os
import board, busio, displayio, os, terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import socketpool
import wifi
from adafruit_httpserver import Server, Request, Response


# TODO : Display no refresh when pressing buttons! --> Delays input!!!!!
# TODO : Runntime all not working for now!!!!!!!!!


# Set up a keyboard/mouse device.
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

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

# Define debounce time in seconds for each keypad
DEBOUNCE_TIME_KEYPAD1 = 0.02
DEBOUNCE_TIME_KEYPAD2 = 0.02

# Variables to track last key press time for each keypad
last_key_press_time_keypad1 = time.monotonic()
last_key_press_time_keypad2 = time.monotonic()

# Variables to display refresh time
display_delay = time.monotonic()

# Display Refresh time
DISPLAY_REFRESH_TIME = 60
runntimeall_delay = time.monotonic()
RUNNTIMEALL = 60

# Timers
runtime_now = time.monotonic()


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
    "121": "121",#
    "122": Keycode.E,#
    "123": Keycode.Q,#
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

board_type = os.uname().machine
print(f"Board: {board_type}")

if 'Pico' in board_type:
    sda, scl = board.GP16, board.GP17
    print("Supported.")
    
elif 'ESP32-S2' in board_type:
    scl, sda = board.IO41, board.IO40 # With the ESP32-S2 you can use any IO pins as I2C pins
    print("Supported.")
    
else:
    print("This board is not directly supported. Change the pin definitions above.")
    
i2c = busio.I2C(scl, sda)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display Group
splash = displayio.Group()
display.show(splash)



################################################################



# Function to read the previous total runtime from the file
def read_previous_runtime():
    try:
        with open("/total_runtime.txt", "w") as file:
            file.write(str("hugo!"))
        with open("/total_runtime.txt", "r") as file:
            previous_total_runtime = file.read()
    except OSError:
        # If the file doesn't exist or cannot be read, return 0
        return 0



def write_alltime_runtime():
    global runntimeall_delay, previous_total_runtime

    # Read the previous total runtime from the file
    previous_total_runtime = read_previous_runtime()

    # Runntime all in minutes!
    if time.monotonic() - runntimeall_delay >= RUNNTIMEALL:
        total_runtime_minutes = previous_total_runtime + str((time.monotonic() - runtime_now) / 60)

        # Open the file in append mode and write the new total runtime
        with open("/total_runtime.txt", "w") as file:
            file.write(str(total_runtime_minutes))
            
        runntimeall_delay = time.monotonic()




################################################################



        
# Create the CPU temperature label
cpu_label = label.Label(terminalio.FONT, text="CPU Temp:    ", color=0xFFFF00, x=0, y=7)
layer_label = label.Label(terminalio.FONT, text="Layer:          ", color=0xFFFF00, x=0, y=22)
runtime_now_label = label.Label(terminalio.FONT, text="Runtime now: ", color=0xFFFF00, x=0, y=37)


# Add the label to the splash Group
splash.append(layer_label)
splash.append(cpu_label)
splash.append(runtime_now_label)


def display_refresh():
    """Refresh the display with updated CPU temperature."""
    global display_delay
    if time.monotonic() - display_delay >= DISPLAY_REFRESH_TIME:
        # Create the CPU temperature label

        cpu_temp = microcontroller.cpu.temperature
        cpu_label.text = "CPU Temp:    " + str("{:.2f}".format(cpu_temp)) + " °C"  # Update the label text
        runtime_now_label.text = "Runtime now:    " + str("{:.0f}".format((time.monotonic() - runtime_now) / 60)) + " min"
        display.refresh()  # Refresh the display to reflect the changes
        display_delay = time.monotonic()

################################################################

def handle_keypad1():
    """Handle key presses for keypad 1."""
    global last_key_press_time_keypad1, pressed_keys_keypad1, layer

    if time.monotonic() - last_key_press_time_keypad1 >= DEBOUNCE_TIME_KEYPAD1:
        keys = keypad.pressed_keys
        for key in keys:
            if key not in pressed_keys_keypad1:
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
    global last_key_press_time_keypad2, pressed_keys_keypad2, layer

    if time.monotonic() - last_key_press_time_keypad2 >= DEBOUNCE_TIME_KEYPAD2:
        keys1 = keypad1.pressed_keys
        for key in keys1:
            if key not in pressed_keys_keypad2:
                if layer == 1:
                    if key in key_mappings_keypad2:
                        if key_mappings_keypad2[key] == "233":
                            layer = 2
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
                            mouse.move(x=0, y=3)
     
                        elif key == "222":
                            mouse.move(x=0, y=-3)

                        elif isinstance(key_mappings_keypad2_layer2[key], tuple):
                            for keycode in key_mappings_keypad2_layer2[key]:
                                kbd.press(keycode)

                        else:
                            if key_mappings_keypad2_layer2[key] == "233":
                                pass

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
                    if key_mappings_keypad2_layer2[key] == "233":
                        layer = 1
                        pressed_keys_keypad2.remove("233")
                        kbd.release_all()

                    else:
                        kbd.release(key_mappings_keypad2_layer2[key])
                        pressed_keys_keypad2.remove(key)

        last_key_press_time_keypad2 = time.monotonic()



################################################################
        
        
#One time functions:

layer_label.text = "Layer:          " + str(layer)

#previous_total_runtime = read_previous_runtime()
#TODO WRITE only File System ------->
#with open("/wow.txt", "w") as file:
#           file.write(str("GOOOOO!"))

# Main loop
while True:
    
    # Functions
    display_refresh()
    #write_alltime_runtime()

    # Keyboard Action
    handle_keypad1()
    handle_keypad2()

