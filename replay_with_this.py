# You can use this script to replay the keypressess that you've recorded
# Make sure that you run this as an Administrator or it might not work

import time
import pynput
import sys
import json

# Flag to control the loop
running = False
looping = True

# Load Json file
with open('key_log_hsr.json','r') as f:
    key_log_data = json.load(f)

# Function to handle key presses
def on_press(key, injected):
    global running
    global looping
    try:
        print('alphanumeric key {} pressed; it was {}'.format(
            key.char, 'faked' if injected else 'not faked'))
        print(key)
        if key.char == '+':
            print('Script activated, press backspace to stop')
            running = True
        
    except AttributeError:
        print('Special key {} pressed'.format(key))
        if key == pynput.keyboard.Key.backspace:
            print("Stopping script.")
            running = False
            looping = False
            sys.exit("EXIT")
            return False

def execute_key_log(data):
    #Sleep time
    previous = data.get("previous", None)
    print(f"Waiting {previous} seconds")
    time.sleep(previous)
    data_type = data.get("type", None)
    data_trigger = data.get("trigger", None)
    #Mouse press
    if data_type == "MousePress":
        if data_trigger == "LeftClick":
            print(f"Pressing {data_trigger} at {data['x']} {data['y']}")
            mouse.position = (data['x'], data['y'])
            mouse.press(pynput.mouse.Button.left)
            time.sleep(0.1)
            mouse.release(pynput.mouse.Button.left)
        else: 
            print(f"Pressing Other mouse press type {data_trigger}")
    #Special key press
    elif data_type == "SpecialKey":
        print(f"Pressing {data_type} {data_trigger}")
        try:
            # Dynamically get the special key from the pynput.keyboard.Key enum
            key_name = data_trigger.split(".")[1]
            special_key = getattr(pynput.keyboard.Key, key_name)
            keyboard.press(special_key)
            time.sleep(0.2)
            keyboard.release(special_key)
        except AttributeError:
            print(f"Unknown special key: {data_trigger}")
    #Basic Key press from A-Z
    else :
        print(f"Pressing Other data type {data_type} {data_trigger} , I'm too lazy to program this")


# Listener to detect key presses
listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

print('Press + on numpad to activate, press backspace to deactivate')

#Loop looping here
while looping == True:
    if running:
        current_number = 0
        all_number = len(key_log_data) - 1
        time.sleep(0.1)
        while current_number < all_number:
            execute_key_log(key_log_data[current_number])
            current_number = current_number + 1
            if running == False:
                break
else:
    print("Loop is disabled")