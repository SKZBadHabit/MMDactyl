from adafruit_hid.keycode import Keycode

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