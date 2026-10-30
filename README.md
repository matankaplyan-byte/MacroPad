# MacroPad

A fully customizable 6-key macro pad powered by a custom RP2040 PCB, featuring a rotary encoder, a 1.3-inch display, and a Python desktop application.

## The Idea

The goal is to create a macro pad with **unlimited custom layouts**.

Each layout contains six customizable macros. By pressing the rotary encoder's built-in button, users will be able to switch between layouts without opening the desktop application.

For example:

- **Layout 1 — Everyday:** WhatsApp, YouTube, Discord mute, media controls, etc.
- **Layout 2 — Programming:** Copy, paste, run code, open applications, and shortcuts.
- **Layout 3 — Sim Racing:** Game shortcuts and other racing-related controls.

Users will be able to create as many layouts as they want and customize the actions assigned to each key.

## Planned Hardware

- Custom RP2040-based PCB
- 6 mechanical keyboard switches
- EC11 rotary encoder with push button
- 1.3-inch ST7789 240×240 display
- USB-C connection
- Custom 3D-printed enclosure

The rotary encoder will control volume when rotated and switch between macro layouts when pressed.

The display is intended to show useful information about the currently selected layout and macros.

## Desktop Software

The controller is being developed in Python using Tkinter.

### Currently implemented

- Dark-themed desktop GUI
- Six selectable macro slots
- Arduino serial communication
- WhatsApp and YouTube launching
- Discord mute/unmute
- Media play/pause
- Custom macro editor for slots 5 and 6
- Support for keyboard shortcuts, websites, and launching applications

### Planned features

- Unlimited customizable macro layouts
- Switching layouts using the rotary encoder button
- Saving layouts and macros using JSON
- Display integration
- Communication with the final RP2040 hardware

## Current Prototype

An **Arduino Pro Micro with a single push button** is being used to test the software.

The Arduino sends button-press events to Python over USB Serial, allowing the desktop application to execute macros.

**The Arduino Pro Micro is not part of the final hardware design.** It is only being used for development and testing while the custom PCB is being manufactured.

## Installation (Current Prototype)

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Connect the Arduino prototype, configure the correct COM port in `main.py`, and run:

```bash
python main.py
```

## Development Roadmap

- [x] Design custom RP2040 PCB
- [x] Create initial Python macro controller
- [x] Build Arduino button prototype
- [x] Create dark-themed GUI
- [x] Add basic custom macro editing
- [ ] Implement JSON configuration saving
- [ ] Implement unlimited custom layouts
- [ ] Add rotary encoder controls
- [ ] Finish the 3D-printed enclosure
- [ ] Manufacture and assemble the custom PCB
- [ ] Integrate the ST7789 display
- [ ] Test the final hardware

## Hack Club Forge

This project is being developed for Hack Club Forge.

[View the project on Forge](https://forge.hackclub.com/projects/4199)
