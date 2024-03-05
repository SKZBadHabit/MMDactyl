import digitalio
import board
import storage
import usb_cdc
import usb_hid

switch = digitalio.DigitalInOut(board.GP18)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

if not switch.value:
    storage.disable_usb_drive()
    usb_cdc.enable(console=False)
    usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     USB_hid.Device.CONSUMER_CONTROL))


