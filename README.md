
# MacroPad

A fully customizable 6-key macro pad powered by a custom RP2040 PCB, featuring a rotary encoder, a 1.3-inch display, and a Python desktop application.

<img width="2560" height="1440" alt="Screenshot (862)" src="https://github.com/user-attachments/assets/53ceb863-d34f-47a9-a3cf-e2365d863bde" />


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

### PCB Design

I designed the custom PCB in KiCad, including the RP2040 microcontroller, USB-C connection, mechanical switches, rotary encoder, and display connector.

**Circuit schematic:**

<img width="2048" height="1152" alt="ChatGPT Image Nov 14, 2026, 02_33_19 PM" src="https://github.com/user-attachments/assets/96a21146-3a39-4d87-94cd-72305d37074b" />


**PCB layout:**

<img width="2048" height="1152" alt="ChatGPT Image Nov 14, 2026, 02_33_54 PM" src="https://github.com/user-attachments/assets/39333f33-181f-44fd-bd36-0da20be7a5ad" />


**PCB 3D preview:**

<img width="2048" height="1152" alt="ChatGPT Image Nov 14, 2026, 02_34_36 PM" src="https://github.com/user-attachments/assets/893e9ace-3557-45fd-a1e5-424b60782e8c" />
<img width="2048" height="1152" alt="ChatGPT Image Nov 14, 2026, 02_34_24 PM" src="https://github.com/user-attachments/assets/ec0f9678-161c-4047-8b42-18b7e6d6c628" />



### 3D Modeling

I used Fusion 360 to design the enclosure and check how the components would fit together.

I imported models of the PCB components, including the switches, screen, and rotary encoder, to help position everything correctly.

**Component assembly in Fusion 360:**
<img width="2560" height="1440" alt="Screenshot (934)" src="https://github.com/user-attachments/assets/ddf61ac4-3469-4357-9b97-b7aec4beacab" />
<img width="2560" height="1440" alt="Screenshot (935)" src="https://github.com/user-attachments/assets/5e7e5fa4-000b-40ba-ab80-7eddfe728958" />
<img width="2560" height="1440" alt="Screenshot (936)" src="https://github.com/user-attachments/assets/0114df5d-88f7-431b-8dab-e2a3d04ae7cd" />


The enclosure was designed as two separate pieces, with holes for heat-set inserts and screws to hold them together.

The first print still needs some improvements because the supports damaged the top part, but the bottom part printed successfully.

## Desktop Software

The controller is being developed in Python using Tkinter.

### Currently implemented

- Dark-themed desktop GUI
- Six selectable macro slots
- Arduino serial communication
- WhatsApp and YouTube launching
- Discord mute/unmute
- Media play/pause
- Custom macro editing
- Support for keyboard shortcuts, websites, and launching applications
- Creating and deleting custom layouts
- Saving layouts and macros using JSON
- Rotary encoder volume control in the Arduino prototype
- OLED display support in the Arduino prototype

### Planned features

- Expanding the physical button support from one to six buttons
- Adapting the Arduino Pro Micro code to the custom RP2040 PCB
- Updating the GPIO assignments
- Integrating the final ST7789 display
- Testing communication with the final hardware

## Current Prototype

An **Arduino Pro Micro with a single push button** is being used to test the software.

The Arduino sends button-press events to Python over USB Serial, allowing the desktop application to execute macros.

I also connected a 0.96-inch OLED display and rotary encoder to test the display functionality and volume controls.

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
- [x] Add custom macro editing
- [x] Implement JSON configuration saving
- [x] Implement unlimited custom layouts
- [x] Add rotary encoder controls
- [x] Finish the 3D-printed enclosure design
- [ ] Fix the enclosure print
- [ ] Manufacture and assemble the custom PCB
- [ ] Integrate the ST7789 display
- [ ] Test the final hardware

## Bill of Materials (BOM)

The complete Bill of Materials for the MacroPad, including component quantities, values, and LCSC part numbers, is available here:

[View the MacroPad BOM](macropad/macro_pad_BOM.csv)

## Hack Club Forge

This project is being developed for Hack Club Forge.

[View the project on Forge](https://forge.hackclub.com/projects/4199)
