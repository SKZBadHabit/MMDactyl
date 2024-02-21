import time
import digitalio
import board
import usb_hid
import adafruit_matrixkeypad
import microcontroller
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

###############################################################################################

# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)

# Define the columns and rows using GPIO pins.
cols = [digitalio.DigitalInOut(x) for x in (board.GP0, board.GP1, board.GP2)]
rows = [digitalio.DigitalInOut(x) for x in (board.GP6, board.GP7, board.GP8, board.GP9, board.GP10)]

# Define the keys for the matrix.
keys = (("111", "112", "113"),
        ("121", "122", "123"),
        ("131", "132", "133"),
        ("141", "142", "143"),
        ("151", "152", "153"))

keys1 = (("211", "212", "213", "214", "215"),
         ("221", "222", "223", "224", "225"),
         ("231", "232", "233", "234", "235"))

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
DISPLAY_REFRESH_TIME = 5

# Define a list to track currently pressed keys for each keypad
pressed_keys_keypad1 = []
pressed_keys_keypad2 = []

# Define key mappings
key_mappings_keypad1 = {
    "111": Keycode.A,
    "112": Keycode.B,
    "113": Keycode.C,
    "121": Keycode.D,
    "122": Keycode.E,
    "123": Keycode.LEFT_SHIFT, 
    "131": Keycode.G,
    "132": Keycode.H,
    "133": Keycode.I,
    "141": Keycode.J,
    "142": Keycode.K,
    "143": Keycode.L,
    "151": Keycode.M,
    "152": Keycode.N,
    "153": Keycode.O,
}

key_mappings_keypad2 = {
    "211": Keycode.P,
    "212": Keycode.Q,
    "213": Keycode.R,
    "214": Keycode.S,
    "215": "215",
    "221": Keycode.U,
    "222": Keycode.V,
    "223": Keycode.W,
    "224": Keycode.X,
    "225": Keycode.Y,
    "231": Keycode.Z,
    "232": Keycode.ONE,
    "233": Keycode.TWO,
    "234": Keycode.THREE,
    "235": Keycode.FOUR,
}

### Layer 2 ###

key_mappings_keypad1_layer2 = {
    "111": Keycode.A,
    "112": Keycode.DOWN_ARROW,
    "113": Keycode.C,
    "121": Keycode.D,
    "122": Keycode.E,
    "123": Keycode.LEFT_SHIFT,
    "131": Keycode.G,
    "132": Keycode.H,
    "133": Keycode.I,
    "141": Keycode.J,
    "142": Keycode.UP_ARROW,
    "143": Keycode.L,
    "151": Keycode.NINE,
    "152": Keycode.N,
    "153": (Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.ESCAPE),
}

key_mappings_keypad2_layer2 = {
    "211": Keycode.P,
    "212": Keycode.Q,
    "213": Keycode.R,
    "214": Keycode.S,
    "215": "215",
    "221": Keycode.RIGHT_ARROW,
    "222": Keycode.V,
    "223": Keycode.W,
    "224": Keycode.X,
    "225": Keycode.Y,
    "231": Keycode.LEFT_ARROW,
    "232": Keycode.ONE,
    "233": Keycode.TWO,
    "234": Keycode.THREE,
    "235": (Keycode.LEFT_GUI, Keycode.I),
}

###############################################################################################

def informations():
    global display_delay
    if time.monotonic() - display_delay >= DISPLAY_REFRESH_TIME:
        cpu_temp = microcontroller.cpu.temperature
        cpu_freq = microcontroller.cpu.frequency / 1000000
        print(f"CPU Temperature: {cpu_temp}°C, Frequency: {cpu_freq} MHz")
        display_delay = time.monotonic()

###############################################################################################

# Main loop
while True:
    ### Functions ###

    informations()

    ### Keyboard Action ###


    # Check if enough time has elapsed since the last key press for keypad 1oy
    if time.monotonic() - last_key_press_time_keypad1 >= DEBOUNCE_TIME_KEYPAD1:
        # Check keypad 1 for pressed keys
        keys = keypad.pressed_keys
        for key in keys:
            if key not in pressed_keys_keypad1:

                if layer == 1:
                    if key in key_mappings_keypad1:

                        kbd.press(key_mappings_keypad1[key])
                        pressed_keys_keypad1.append(key)

                if layer == 2:
                    if key in key_mappings_keypad1_layer2:
                        # Check if it's a single keycode or a sequence of keycodes
                        if isinstance(key_mappings_keypad1_layer2[key], tuple):
                            # Iterate over the sequence of keycodes
                            for keycode in key_mappings_keypad1_layer2[key]:
                                kbd.press(keycode)
                        else:
                            # It's a single keycode
                            kbd.press(key_mappings_keypad1_layer2[key])
                        pressed_keys_keypad1.append(key)               

        # Check for released keys for keypad 1
        for key in pressed_keys_keypad1.copy():
            if key not in keys:

                if layer == 1:
                    if key in key_mappings_keypad1:
                        
                        kbd.release(key_mappings_keypad1[key])
                        pressed_keys_keypad1.remove(key)

                if layer == 2:
                    if key in key_mappings_keypad1_layer2:
                        # Check if it's a single keycode or a sequence of keycodes
                        if isinstance(key_mappings_keypad1_layer2[key], tuple):
                            # Iterate over the sequence of keycodes
                            for keycode in reversed(key_mappings_keypad1_layer2[key]):
                                kbd.release(keycode)
                        else:
                            # It's a single keycode
                            kbd.release(key_mappings_keypad1_layer2[key])
                        pressed_keys_keypad1.remove(key)

        last_key_press_time_keypad1 = time.monotonic()

    # Check if enough time has elapsed since the last key press for keypad 2
    if time.monotonic() - last_key_press_time_keypad2 >= DEBOUNCE_TIME_KEYPAD2:
        # Check keypad 2 for pressed keys
        keys1 = keypad1.pressed_keys
        for key in keys1:
            if key not in pressed_keys_keypad2:

                if layer == 1:
                    if key in key_mappings_keypad2:
                        
                        if key_mappings_keypad2[key] == "215":
                            layer = 2
                            pressed_keys_keypad2.append("215")
                            

                        else:
                            kbd.press(key_mappings_keypad2[key])
                            pressed_keys_keypad2.append(key)
                
                if layer == 2:
                    if key in key_mappings_keypad2_layer2:
                        if isinstance(key_mappings_keypad2_layer2[key], tuple):
                            # Iterate over the sequence of keycodes
                            for keycode in key_mappings_keypad2_layer2[key]:
                                kbd.press(keycode)
                        else:
                    
                            if key_mappings_keypad2_layer2[key] == "215":
                                pass
                            else:
                                kbd.press(key_mappings_keypad2_layer2[key])
                                pressed_keys_keypad2.append(key)    


            # Check for released keys for keypad
        for key in pressed_keys_keypad2.copy():
            if key not in keys1:

                if layer == 1:
                    if key in key_mappings_keypad2:
                        kbd.release(key_mappings_keypad2[key])
                        pressed_keys_keypad2.remove(key)
            
                if layer == 2:
                    if key_mappings_keypad2_layer2[key] == "215":
                            layer = 1
                            pressed_keys_keypad2.remove("215")
                            #Release all keys 
                            kbd.release_all()
                            
                    else:
                        kbd.release(key_mappings_keypad2_layer2[key])
                        pressed_keys_keypad2.remove(key)

        last_key_press_time_keypad2 = time.monotonic()
