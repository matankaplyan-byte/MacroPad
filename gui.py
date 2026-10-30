
import tkinter as tk

BG = "#10141D"
PANEL = "#1B2433"
BUTTON = "#222D40"
ACCENT = "#4D9FFF"
TEXT = "#FFFFFF"
MUTED = "#9CA9BC"

MACROS = [
    ("WhatsApp", "WA"),
    ("YouTube", "YT"),
    ("Discord Mute", "MIC"),
    ("Play / Pause", "MEDIA"),
    ("Copy", "COPY"),
    ("Paste", "PASTE")
]


def start_gui(on_select, events):
    root = tk.Tk()
    root.title("MacroPad Controller")
    root.geometry("540x470")
    root.minsize(480, 430)
    root.configure(bg=BG)

    selected = 1
    buttons = {}

    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=25, pady=(22, 15))

    tk.Label(
        header,
        text="MACROPAD",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 22, "bold")
    ).pack(side="left")

    connection_label = tk.Label(
        header,
        text="● CONNECTED",
        bg=BG,
        fg="#50D890",
        font=("Segoe UI", 10, "bold")
    )
    connection_label.pack(side="right")

    active_panel = tk.Frame(root, bg=PANEL)
    active_panel.pack(fill="x", padx=25, pady=(0, 20))

    tk.Label(
        active_panel,
        text="ACTIVE MACRO",
        bg=PANEL,
        fg=MUTED,
        font=("Segoe UI", 10, "bold")
    ).pack(pady=(15, 3))

    active_label = tk.Label(
        active_panel,
        text="WhatsApp",
        bg=PANEL,
        fg=TEXT,
        font=("Segoe UI", 21, "bold")
    )
    active_label.pack()

    status_label = tk.Label(
        active_panel,
        text="Press the physical button to execute",
        bg=PANEL,
        fg=MUTED,
        font=("Segoe UI", 10)
    )
    status_label.pack(pady=(5, 16))

    grid_frame = tk.Frame(root, bg=BG)
    grid_frame.pack(fill="both", expand=True, padx=25)

    for column in range(3):
        grid_frame.columnconfigure(column, weight=1)

    for row in range(2):
        grid_frame.rowconfigure(row, weight=1)

    def select_macro(number):
        nonlocal selected

        selected = number
        name = MACROS[number - 1][0]

        active_label.config(text=name)
        on_select(number)

        for index, button in buttons.items():
            if index == selected:
                button.config(
                    bg=ACCENT,
                    activebackground=ACCENT
                )
            else:
                button.config(
                    bg=BUTTON,
                    activebackground=PANEL
                )

    for i, (name, short_name) in enumerate(MACROS, start=1):
        button = tk.Button(
            grid_frame,
            text=f"{short_name}\n{name}",
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

    footer = tk.Label(
        root,
        text="6 MACROS  •  ARDUINO PRO MICRO  •  V1.1",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 9)
    )
    footer.pack(pady=15)

    select_macro(1)

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

                if event == "PRESSED":
                    status_label.config(
                        text="● MACRO EXECUTED!",
                        fg="#50D890"
                    )

                    if flash_id is not None:
                        root.after_cancel(flash_id)

                    flash_id = root.after(450, restore_status)

                elif event == "DISCONNECTED":
                    connection_label.config(
                        text="● DISCONNECTED",
                        fg="#FF6666"
                    )

        except __import__("queue").Empty:
            pass

        root.after(50, check_events)

    check_events()
    root.mainloop()
