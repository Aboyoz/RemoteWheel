from collections import defaultdict
import uinput

"""
For Linux:
    OSError: [Errno 19] Failed to open the uinput device: No such device
    Bugfix: https://stackoverflow.com/questions/48640935/oserror-errno-19-failed-to-open-the-uinput-device-no-such-device
"""

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.ABS_Z + (0, 10, 0, 0),
    uinput.ABS_RZ + (0, 10, 0, 0),
    uinput.ABS_RUDDER + (0, 255, 0, 0),
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0),
    uinput.BTN_DPAD_UP,
    uinput.BTN_DPAD_DOWN,
    uinput.BTN_DPAD_LEFT,
    uinput.BTN_DPAD_RIGHT,
)

def XboxController():
    device = uinput.Device(
        events,
        vendor=0x045e,
        product=0x028e,
        version=0x110,
        name="Microsoft X-Box 360 pad",
    )

    device.emit(uinput.ABS_X, 128, syn=False)
    device.emit(uinput.ABS_Y, 128)

    return device
