
import serial
import os
import json
import copy
import webbrowser
import pyautogui
import pydirectinput
import threading
import queue
import time

from gui import start_gui

SAVE_FILE = os.path.join(os.path.dirname(__file__), "layouts.json")

DEFAULT_LAYOUTS = {
    "Everyday": [
        ("WhatsApp", "WA", "whatsapp"),
        ("YouTube", "YT", "youtube"),
        ("Discord Mute", "MIC", "discord"),
        ("Play / Pause", "MEDIA", "playpause"),
        ("Copy", "COPY", "copy"),
        ("Paste", "PASTE", "paste")
    ],
    "Programming": [
        ("Copy", "COPY", "copy"),
        ("Paste", "PASTE", "paste"),
        ("Undo", "UNDO", "undo"),
        ("Redo", "REDO", "redo"),
        ("Save", "SAVE", "save"),
        ("Run", "RUN", "run")
    ],
    "Sim Racing": [
        ("Play / Pause", "MEDIA", "playpause"),
        ("Mute Discord", "MIC", "discord"),
        ("Screenshot", "SHOT", "screenshot"),
        ("Accept Call", "ACCEPT", "accept_call"),
        ("Decline Call", "DECLINE", "decline_call"),
        ("Mute Volume", "MUTE", "volumemute")
    ]
}


def load_layouts():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if (
                isinstance(data, dict)
                and data
                and all(
                    isinstance(buttons, list)
                    and len(buttons) == 6
                    and all(
                        isinstance(button, (list, tuple))
                        and len(button) == 3
                        and all(isinstance(x, str) for x in button)
                        for button in buttons
                    )
                    for buttons in data.values()
                )
            ):
                return data

        except (OSError, ValueError) as error:
            print("Could not load layouts:", error)

    return copy.deepcopy(DEFAULT_LAYOUTS)


LAYOUTS = load_layouts()
events = queue.Queue()
state_lock = threading.RLock()

current_layout = next(iter(LAYOUTS))
selected_macro = 1
button_switches_layout = False

try:
    arduino = serial.Serial("COM7", 9600, timeout=1)
except serial.SerialException as error:
    print("Arduino unavailable:", error)
    arduino = None


def save_layouts():
    temporary_file = SAVE_FILE + ".tmp"

    with state_lock:
        data = copy.deepcopy(LAYOUTS)

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    os.replace(temporary_file, SAVE_FILE)
    print("Layouts saved!")


def execute_macro(macro):
    if macro == "whatsapp":
        os.startfile("whatsapp:")

    elif macro == "youtube":
        webbrowser.open(
            "https://www.youtube.com/watch?v=Y-3pYLU17z0&list=RDY-3pYLU17z0&start_radio=1"
        )

    elif macro == "discord":
        pydirectinput.keyDown("ctrl")
        pydirectinput.keyDown("shift")
        try:
            pydirectinput.press("f9")
        finally:
            pydirectinput.keyUp("shift")
            pydirectinput.keyUp("ctrl")

    elif macro == "playpause":
        pyautogui.press("playpause")

    elif macro == "copy":
        pyautogui.hotkey("ctrl", "c")

    elif macro == "paste":
        pyautogui.hotkey("ctrl", "v")

    elif macro == "undo":
        pyautogui.hotkey("ctrl", "z")

    elif macro == "redo":
        pyautogui.hotkey("ctrl", "y")

    elif macro == "save":
        pyautogui.hotkey("ctrl", "s")

    elif macro == "run":
        pyautogui.hotkey("shift", "f10")

    elif macro == "screenshot":
        pyautogui.hotkey("win", "shift", "s")

    elif macro in ("volumeup", "volumedown", "volumemute"):
        pyautogui.press(macro)

    elif macro.startswith("hotkey:"):
        keys = [
            key.strip().lower()
            for key in macro[7:].split("+")
        ]
        if not keys or any(not key for key in keys):
            raise ValueError("Invalid keyboard shortcut")
        pyautogui.hotkey(*keys)

    elif macro.startswith("url:"):
        url = macro[4:].strip()
        if not url.startswith(("https://", "http://")):
            raise ValueError("URL must start with https:// or http://")
        webbrowser.open(url)

    else:
        print("Action not implemented:", macro)


def select_macro(number):
    global selected_macro
    with state_lock:
        selected_macro = number


def send_layout(name):
    if arduino is None:
        return

    try:
        arduino.write(f"LAYOUT:{name}\n".encode("utf-8"))
    except (serial.SerialException, OSError) as error:
        print("Failed to send layout:", error)
        events.put(("DISCONNECTED",))


def change_layout(name):
    global current_layout, selected_macro

    with state_lock:
        if name not in LAYOUTS:
            return

        current_layout = name
        selected_macro = 1

    send_layout(name)
    print("Current layout:", name)


def set_button_mode(enabled):
    global button_switches_layout
    with state_lock:
        button_switches_layout = enabled


def listen_to_arduino():
    if arduino is None:
        events.put(("DISCONNECTED",))
        return

    while True:
        try:
            message = arduino.readline().decode(
                errors="replace"
            ).strip()

            if message != "PRESSED":
                continue

            with state_lock:
                if button_switches_layout:
                    names = list(LAYOUTS)
                    index = names.index(current_layout)
                    next_layout = names[(index + 1) % len(names)]
                    macro = None
                else:
                    next_layout = None
                    macro = LAYOUTS[current_layout][selected_macro - 1]

            if next_layout is not None:
                change_layout(next_layout)
                events.put(("LAYOUT_CHANGED", next_layout))

            elif macro is not None:
                events.put(("PRESSED",))
                try:
                    execute_macro(macro[2])
                except Exception as error:
                    print("Macro failed:", error)

        except (serial.SerialException, OSError) as error:
            print("Arduino disconnected:", error)
            events.put(("DISCONNECTED",))
            break


threading.Thread(
    target=listen_to_arduino,
    daemon=True
).start()

try:
    time.sleep(2 if arduino is not None else 0)

    start_gui(
        LAYOUTS,
        select_macro,
        change_layout,
        set_button_mode,
        events,
        save_layouts
    )

finally:
    if arduino is not None:
        arduino.close()
