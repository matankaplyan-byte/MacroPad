
import serial
import os
import webbrowser
import pyautogui
import pydirectinput
import threading
import queue

from gui import start_gui

arduino = serial.Serial("COM5", 9600, timeout=1)

events = queue.Queue()
action = 1


def open_whatsapp():
    os.startfile("whatsapp:")


def open_yt():
    webbrowser.open(
        "https://www.youtube.com/watch?v=Y-3pYLU17z0&list=RDY-3pYLU17z0&start_radio=1"
    )


def mute_discord():
    pydirectinput.keyDown("ctrl")
    pydirectinput.keyDown("shift")

    try:
        pydirectinput.press("f9")
    finally:
        pydirectinput.keyUp("shift")
        pydirectinput.keyUp("ctrl")


def play_pause():
    pyautogui.press("playpause")


def copy_text():
    pyautogui.hotkey("ctrl", "c")


def paste_text():
    pyautogui.hotkey("ctrl", "v")


actions = {
    1: open_whatsapp,
    2: open_yt,
    3: mute_discord,
    4: play_pause,
    5: copy_text,
    6: paste_text
}


def select_action(number):
    global action

    action = number
    print(f"Selected macro: {number}")


def listen_to_arduino():
    while True:
        try:
            message = arduino.readline().decode(
                errors="replace"
            ).strip()

            if message == "PRESSED":
                selected_action = action

                if selected_action in actions:
                    events.put("PRESSED")
                    print(f"Executing macro {selected_action}")

                    try:
                        actions[selected_action]()
                    except Exception as error:
                        print(f"Macro failed: {error}")

        except serial.SerialException as error:
            print(f"Arduino disconnected: {error}")
            events.put("DISCONNECTED")
            break


thread = threading.Thread(
    target=listen_to_arduino,
    daemon=True
)
thread.start()

try:
    start_gui(select_action, events)
finally:
    arduino.close()
