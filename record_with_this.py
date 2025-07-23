# You can use this script to record your button pressess and mouse clicks.
# Make sure that you run this as an Administrator or it might not work

import json
import os
from pynput import mouse, keyboard
from datetime import datetime

LOG_FILE = "key_log_hsr.json"

# Global flag to toggle logging
logging_active = False
listener_running = True

mouse_controller = mouse.Controller()

last_timestamp = None

# Log the coordinates here
def log_coordinates(x, y, type, trigger):
    global last_timestamp
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    # Calculate time difference from previous log
    if last_timestamp:
        delta = (timestamp - last_timestamp).total_seconds()
    else:
        delta = None

    last_timestamp = timestamp

    entry = {
        "timestamp": timestamp_str,
        "x": x,
        "y": y,
        "type": type,
        "trigger": str(trigger),
        "previous": delta
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# On Key press do this
def on_press(key):
    global logging_active, listener_running

    try:
        if key.char == '+':
            logging_active = True
            print("[+] Logging activated.")
        elif key.char == '-':
            print("[-] Stopping program.")
            listener_running = False
            return False  # Stop the listener
        elif logging_active:
            x, y = mouse_controller.position
            print(f"[LOGGED] Key: {key}, Mouse: ({x}, {y})")
            log_coordinates(x, y, "KeyPress", key)
    except AttributeError:
        if logging_active:
            x, y = mouse_controller.position
            print(f"[LOGGED] Special Key: {key}, Mouse: ({x}, {y})")
            log_coordinates(x, y, "SpecialKey", key)

# On mouse click do this
def on_click(x, y, button, pressed):
    if logging_active and pressed and button == mouse.Button.left:
        print(f"[LOGGED] Left Click at ({x}, {y})")
        log_coordinates(x, y, "MousePress", "LeftClick")

def main():
    print("Press '+' to start logging key presses and mouse coordinates.")
    print("Press '-' to stop the script.")

    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.stop()

if __name__ == "__main__":
    main()