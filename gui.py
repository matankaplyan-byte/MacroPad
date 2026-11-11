
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import queue

BG = "#10141D"
PANEL = "#1B2433"
BUTTON = "#222D40"
ACCENT = "#4D9FFF"
TEXT = "#FFFFFF"
MUTED = "#9CA9BC"
GREEN = "#50D890"

ACTIONS = {
    "Copy": "copy",
    "Paste": "paste",
    "Undo": "undo",
    "Redo": "redo",
    "Save": "save",
    "Run": "run",
    "Screenshot": "screenshot",
    "Play / Pause": "playpause",
    "Volume Up": "volumeup",
    "Volume Down": "volumedown",
    "Mute Volume": "volumemute",
    "Discord Mute": "discord",
    "WhatsApp": "whatsapp",
    "YouTube": "youtube",
    "Accept Call (not implemented)": "accept_call",
    "Decline Call (not implemented)": "decline_call"
}


def record_shortcut(parent, result_variable):
    recorder = tk.Toplevel(parent)
    recorder.title("Record Shortcut")
    recorder.geometry("390x230")
    recorder.configure(bg=BG)
    recorder.transient(parent)
    recorder.grab_set()

    tk.Label(
        recorder,
        text="Press your shortcut...",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(22, 10))

    preview = tk.Label(
        recorder,
        text="Waiting for keys",
        bg=BG,
        fg=ACCENT,
        font=("Segoe UI", 14)
    )
    preview.pack(pady=8)

    modifiers = set()

    modifier_keys = {
        "Control_L": "ctrl",
        "Control_R": "ctrl",
        "Shift_L": "shift",
        "Shift_R": "shift",
        "Alt_L": "alt",
        "Alt_R": "alt",
        "Super_L": "win",
        "Super_R": "win",
        "Win_L": "win",
        "Win_R": "win"
    }

    def on_key_press(event):
        modifier = modifier_keys.get(event.keysym)

        if modifier:
            modifiers.add(modifier)
            preview.config(
                text="+".join(
                    m for m in ["ctrl", "alt", "shift", "win"]
                    if m in modifiers
                )
            )
            return "break"

        special_keys = {
            "Return": "enter",
            "Escape": "esc",
            "BackSpace": "backspace",
            "Delete": "delete",
            "space": "space",
            "Tab": "tab",
            "Prior": "pageup",
            "Next": "pagedown",
            "Up": "up",
            "Down": "down",
            "Left": "left",
            "Right": "right"
        }

        key = special_keys.get(event.keysym, event.keysym.lower())

        # Tkinter may report uppercase letters with Shift held.
        if len(key) == 1:
            key = key.lower()

        order = ["ctrl", "alt", "shift", "win"]
        active = [m for m in order if m in modifiers]

        shortcut = "+".join(active + [key])
        result_variable.set(shortcut)
        recorder.destroy()
        return "break"

    def on_key_release(event):
        modifier = modifier_keys.get(event.keysym)
        if modifier:
            modifiers.discard(modifier)

    recorder.bind("<KeyPress>", on_key_press)
    recorder.bind("<KeyRelease>", on_key_release)

    tk.Button(
        recorder,
        text="Cancel",
        command=recorder.destroy,
        bg=BUTTON,
        fg=TEXT,
        relief="flat",
        padx=20,
        pady=7
    ).pack(pady=10)

    recorder.after(100, recorder.focus_force)


def start_gui(
    layouts,
    on_select,
    on_layout_change,
    on_mode_change,
    events,
    on_save
):
    root = tk.Tk()
    root.title("MacroPad Controller")
    root.geometry("620x690")
    root.minsize(540, 620)
    root.configure(bg=BG)

    current_layout = tk.StringVar(value=next(iter(layouts)))
    switch_mode = tk.BooleanVar(value=False)
    selected = 1
    buttons = {}

    def label(parent, text, size=10, color=TEXT, bold=False):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal")
        )

    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=25, pady=(20, 12))

    label(header, "MACROPAD", 22, bold=True).pack(side="left")

    connection_label = label(
        header, "● CONNECTED", 10, GREEN, True
    )
    connection_label.pack(side="right")

    active_panel = tk.Frame(root, bg=PANEL)
    active_panel.pack(fill="x", padx=25, pady=(0, 15))

    label(
        active_panel, "ACTIVE MACRO", 10, MUTED, True
    ).pack(pady=(15, 3))

    active_label = label(
        active_panel, "", 21, TEXT, True
    )
    active_label.pack()

    status_label = label(
        active_panel,
        "Press the physical button to execute",
        10,
        MUTED
    )
    status_label.pack(pady=(5, 16))

    layout_frame = tk.Frame(root, bg=BG)
    layout_frame.pack(fill="x", padx=25, pady=(0, 10))

    label(layout_frame, "LAYOUT:", 10, MUTED, True).pack(
        side="left"
    )

    layout_menu = tk.OptionMenu(
        layout_frame,
        current_layout,
        next(iter(layouts))
    )
    layout_menu.config(
        bg=BUTTON,
        fg=TEXT,
        activebackground=ACCENT,
        activeforeground=TEXT,
        relief="flat",
        highlightthickness=0
    )
    layout_menu["menu"].config(
        bg=BUTTON,
        fg=TEXT,
        activebackground=ACCENT,
        activeforeground=TEXT
    )
    layout_menu.pack(side="left", padx=10)

    def styled_button(parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=BUTTON,
            fg=TEXT,
            activebackground=ACCENT,
            activeforeground=TEXT,
            relief="flat",
            padx=10,
            pady=7,
            cursor="hand2"
        )

    def select_macro(number):
        nonlocal selected
        selected = number

        name = layouts[current_layout.get()][number - 1][0]
        active_label.config(text=name)
        on_select(number)

        for index, button in buttons.items():
            button.config(
                bg=ACCENT if index == selected else BUTTON
            )

    def update_layout(name):
        if name not in layouts:
            return

        current_layout.set(name)

        for index, button in buttons.items():
            macro_name, short_name, _ = layouts[name][index - 1]
            button.config(text=f"{short_name}\n{macro_name}")

        select_macro(1)

    def choose_layout(name):
        on_layout_change(name)
        update_layout(name)

    def refresh_menu():
        menu = layout_menu["menu"]
        menu.delete(0, "end")

        for name in layouts:
            menu.add_command(
                label=name,
                command=lambda n=name: choose_layout(n)
            )

    def create_layout():
        name = simpledialog.askstring(
            "New Layout",
            "Enter layout name:",
            parent=root
        )

        if name is None:
            return

        name = name.strip()

        if not name or "\n" in name or "\r" in name:
            messagebox.showerror(
                "Invalid name", "Enter a valid layout name."
            )
            return

        if name in layouts:
            messagebox.showerror(
                "Already exists", "This layout already exists."
            )
            return

        layouts[name] = [
            ("Empty", "---", "none") for _ in range(6)
        ]

        on_save()
        refresh_menu()
        choose_layout(name)

    def rename_layout():
        old_name = current_layout.get()

        name = simpledialog.askstring(
            "Rename Layout",
            "New layout name:",
            initialvalue=old_name,
            parent=root
        )

        if name is None:
            return

        name = name.strip()

        if (
            not name
            or "\n" in name
            or "\r" in name
            or (name in layouts and name != old_name)
        ):
            messagebox.showerror(
                "Invalid name", "Choose a different valid name."
            )
            return

        if name == old_name:
            return

        updated = {}
        for key, value in layouts.items():
            updated[name if key == old_name else key] = value

        layouts.clear()
        layouts.update(updated)

        on_save()
        refresh_menu()
        choose_layout(name)

    def delete_layout():
        name = current_layout.get()

        if len(layouts) <= 1:
            messagebox.showwarning(
                "Cannot delete",
                "You must keep at least one layout."
            )
            return

        if not messagebox.askyesno(
            "Delete Layout",
            f"Delete '{name}'?"
        ):
            return

        del layouts[name]
        on_save()
        refresh_menu()
        choose_layout(next(iter(layouts)))

    def edit_macro():
        layout_name = current_layout.get()
        button_number = selected

        old_name, old_short, old_action = (
            layouts[layout_name][button_number - 1]
        )

        window = tk.Toplevel(root)
        window.title(f"Edit Button {button_number}")
        window.geometry("440x510")
        window.configure(bg=BG)
        window.transient(root)
        window.grab_set()

        form = tk.Frame(window, bg=BG)
        form.pack(fill="both", expand=True, padx=25, pady=20)

        label(
            form, f"EDIT BUTTON {button_number}", 17, bold=True
        ).pack(anchor="w", pady=(0, 15))

        def entry_field(title, value):
            label(form, title, 10, MUTED).pack(
                anchor="w", pady=(8, 3)
            )

            entry = tk.Entry(
                form,
                bg=BUTTON,
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat",
                font=("Segoe UI", 11)
            )
            entry.insert(0, value)
            entry.pack(fill="x", ipady=7)
            return entry

        name_entry = entry_field("Button name", old_name)
        short_entry = entry_field(
            "Short display label", old_short
        )

        label(form, "Action type", 10, MUTED).pack(
            anchor="w", pady=(14, 3)
        )

        if old_action.startswith("hotkey:"):
            initial_type = "Keyboard Shortcut"
            initial_value = old_action[7:]
        elif old_action.startswith("url:"):
            initial_type = "Website URL"
            initial_value = old_action[4:]
        else:
            initial_type = "Built-in Action"
            initial_value = old_action

        action_type = tk.StringVar(value=initial_type)

        action_menu = ttk.Combobox(
            form,
            textvariable=action_type,
            values=[
                "Built-in Action",
                "Keyboard Shortcut",
                "Website URL"
            ],
            state="readonly"
        )
        action_menu.pack(fill="x")

        label(
            form, "Action / shortcut / URL", 10, MUTED
        ).pack(anchor="w", pady=(14, 3))

        action_value = tk.StringVar(value=initial_value)

        action_entry = tk.Entry(
            form,
            textvariable=action_value,
            bg=BUTTON,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )

        record_button = tk.Button(
            form,
            text="● Record Shortcut",
            bg=ACCENT,
            fg=TEXT,
            activebackground=BUTTON,
            activeforeground=TEXT,
            relief="flat",
            cursor="hand2",
            command=lambda: record_shortcut(
                window, action_value
            )
        )

        built_in_menu = ttk.Combobox(
            form,
            values=list(ACTIONS),
            state="readonly"
        )

        def update_action_fields(event=None):
            kind = action_type.get()

            built_in_menu.pack_forget()
            action_entry.pack_forget()
            record_button.pack_forget()

            if kind == "Built-in Action":
                built_in_menu.pack(fill="x", pady=5)

                match = next(
                    (
                        name for name, code in ACTIONS.items()
                        if code == action_value.get()
                    ),
                    list(ACTIONS)[0]
                )
                built_in_menu.set(match)

            elif kind == "Keyboard Shortcut":
                action_entry.pack(fill="x", ipady=7)
                record_button.pack(fill="x", pady=(8, 0))

            else:
                action_entry.pack(fill="x", ipady=7)

        def save_macro():
            name = name_entry.get().strip()
            short = short_entry.get().strip()

            if not name or not short:
                messagebox.showerror(
                    "Missing information",
                    "Enter a name and short label.",
                    parent=window
                )
                return

            kind = action_type.get()

            if kind == "Built-in Action":
                action = ACTIONS[built_in_menu.get()]

            elif kind == "Keyboard Shortcut":
                shortcut = action_value.get().strip().lower()
                keys = [
                    x.strip() for x in shortcut.split("+")
                ]

                if not shortcut or any(not x for x in keys):
                    messagebox.showerror(
                        "Invalid shortcut",
                        "Example: ctrl+shift+s",
                        parent=window
                    )
                    return

                action = "hotkey:" + "+".join(keys)

            else:
                url = action_value.get().strip()

                if not url.startswith(
                    ("https://", "http://")
                ):
                    messagebox.showerror(
                        "Invalid URL",
                        "URL must start with https:// or http://",
                        parent=window
                    )
                    return

                action = "url:" + url

            layouts[layout_name][button_number - 1] = (
                name, short, action
            )

            on_save()
            update_layout(layout_name)
            window.destroy()

        action_menu.bind(
            "<<ComboboxSelected>>",
            update_action_fields
        )
        update_action_fields()

        styled_button(
            form, "SAVE MACRO", save_macro
        ).pack(fill="x", pady=(25, 0))

    manage_frame = tk.Frame(root, bg=BG)
    manage_frame.pack(fill="x", padx=25, pady=(0, 10))

    for text, command in [
        ("+ New", create_layout),
        ("Rename", rename_layout),
        ("Delete", delete_layout)
    ]:
        styled_button(
            manage_frame, text, command
        ).pack(side="left", padx=(0, 7))

    toggle = tk.Checkbutton(
        root,
        text="Button switches layouts",
        variable=switch_mode,
        command=lambda: on_mode_change(
            switch_mode.get()
        ),
        bg=BG,
        fg=TEXT,
        selectcolor=PANEL,
        activebackground=BG,
        activeforeground=TEXT
    )
    toggle.pack(anchor="w", padx=25, pady=(0, 10))

    grid_frame = tk.Frame(root, bg=BG)
    grid_frame.pack(
        fill="both", expand=True, padx=25
    )

    for column in range(3):
        grid_frame.columnconfigure(column, weight=1)

    for row in range(2):
        grid_frame.rowconfigure(row, weight=1)

    for i in range(1, 7):
        button = tk.Button(
            grid_frame,
            font=("Segoe UI", 11, "bold"),
            bg=BUTTON,
            fg=TEXT,
            activeforeground=TEXT,
            activebackground=PANEL,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda number=i: select_macro(number)
        )

        button.grid(
            row=(i - 1) // 3,
            column=(i - 1) % 3,
            sticky="nsew",
            padx=5,
            pady=5
        )

        buttons[i] = button

    styled_button(
        root,
        "✎ EDIT SELECTED BUTTON",
        edit_macro
    ).pack(fill="x", padx=30, pady=(12, 5))

    label(
        root,
        "6 MACROS  •  ARDUINO PRO MICRO  •  V1.5",
        9,
        MUTED
    ).pack(pady=12)

    flash_id = None

    def restore_status():
        status_label.config(
            text="Press the physical button to execute",
            fg=MUTED
        )

    def check_events():
        nonlocal flash_id

        try:
            while True:
                event = events.get_nowait()
                kind = event[0]

                if kind == "PRESSED":
                    status_label.config(
                        text="● MACRO TRIGGERED!",
                        fg=GREEN
                    )

                    if flash_id is not None:
                        root.after_cancel(flash_id)

                    flash_id = root.after(
                        450, restore_status
                    )

                elif kind == "LAYOUT_CHANGED":
                    update_layout(event[1])

                elif kind == "DISCONNECTED":
                    connection_label.config(
                        text="● DISCONNECTED",
                        fg="#FF6666"
                    )

        except queue.Empty:
            pass

        root.after(50, check_events)

    refresh_menu()
    update_layout(next(iter(layouts)))
    on_layout_change(current_layout.get())
    check_events()
    root.mainloop()
