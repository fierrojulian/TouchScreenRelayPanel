from guizero import App, PushButton, Window, Text, Box
import serial
import time
import subprocess
import sys

# ==========================
# Serial setup
# ==========================
SERIAL_PORT = "/dev/ttyACM0"
SERIAL_BAUD = 9600

ser = None
serial_ok = False
try:
    ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=0.1)
    time.sleep(2)
    serial_ok = True
except Exception as e:
    print(f"[WARN] Serial not available on {SERIAL_PORT}: {e}")
    serial_ok = False

def send(cmd: str) -> None:
    if not serial_ok or ser is None:
        return
    try:
        ser.write((cmd + "\n").encode("ascii"))
    except Exception as e:
        print(f"Serial send failed for {cmd!r}: {e}")

# ==========================
# Config
# ==========================
PIN_CODE = "804601"  # <-- your 6-digit PIN

# ==========================
# UPFITTER STYLE THEME
# ==========================
BG = "#07090c"
PANEL = "#0b0f14"

TXT = "#f2f4f7"
TXT_DIM = "#a7b0bb"
WARN = "#ff3b30"

OFF_RING = "#2b323b"
ON_RING  = "#00cc44"
AMBER_RING = "#ffb000"
LOCK_RING  = "#ff2a2a"
NEUTRAL_RING = "#5a616b"

RING_THICKNESS = 3

# Make layout hug screen edges
PAD_X = 0
PAD_Y = 0

BTN_W = 14
BTN_H = 3

BTN_FONT = ("DejaVu Sans", 16, "bold")
STATUS_FONT = ("DejaVu Sans", 12, "bold")

# ==========================
# Batch refresh (prevents stagger)
# ==========================
_BATCH_MODE = False
_NEEDS_REFRESH = False

def begin_batch():
    global _BATCH_MODE, _NEEDS_REFRESH
    _BATCH_MODE = True
    _NEEDS_REFRESH = False

def end_batch():
    global _BATCH_MODE, _NEEDS_REFRESH
    _BATCH_MODE = False
    if _NEEDS_REFRESH:
        refresh_all()

def request_refresh():
    global _NEEDS_REFRESH
    if _BATCH_MODE:
        _NEEDS_REFRESH = True
    else:
        refresh_all()

# ==========================
# States
# ==========================
Locked_State = 0

Fog_Lights_State = 0
Light_Bar_State = 0
Ditch_Lights_State = 0
Backup_Lights_State = 0
Truck_Bed_Lights_State = 0

Rock_Lights_State = 0
Chase_Lights_State = 0
Air_Compressor_State = 0
Winch_State = 0
VHF_UHF_Radio_State = 0

HF_Radio_State = 0
Scanner_State = 0
Computer_State = 0
AC_Power_State = 0
Truck_Bed_12VDC_State = 0

Button_16_State = 0
Trail_Lights_State = 0
Recovery_State = 0

# NEW group toggles
Comms_Group_State = 0
Power_Group_State = 0

Brightness_State = 100
Brightness_Auto = True

# Battery placeholder
Battery_Voltage = None

def battery_text():
    global Battery_Voltage
    if Battery_Voltage is None:
        return "BATT --.-V"
    try:
        return f"BATT {float(Battery_Voltage):.1f}V"
    except Exception:
        return "BATT --.-V"

# GUI handles
app = None
exit_popup = None
pin_popup = None

# Status text widgets
status_top_left = None
status_top_mid = None
status_top_right = None
status_bot_left = None
status_bot_mid = None
status_bot_right = None

# Buttons
buttons = {}
lockable_buttons = []
brightness_buttons = {}

# ==========================
# Styling
# ==========================
def _set_ring(btn, ring_color):
    try:
        btn.bg = PANEL
        btn.text_color = TXT
        btn.tk.configure(
            bd=0,
            relief="flat",
            highlightthickness=RING_THICKNESS,
            highlightbackground=ring_color,
            highlightcolor=ring_color,
            activebackground=PANEL,
            activeforeground=TXT,
            font=BTN_FONT,
            padx=10,
            pady=8,
        )
        btn.tk.grid_configure(padx=PAD_X, pady=PAD_Y, sticky="nsew")
    except Exception:
        pass

def style_main_button(key, is_on):
    _set_ring(buttons[key], ON_RING if is_on else OFF_RING)

def style_neutral_button(key):
    _set_ring(buttons[key], NEUTRAL_RING)

status_top_mid = None
status_bot_mid = None

# ==========================
# Status bar
# ==========================
def update_status_bar():
    lock_txt = "LOCKED" if Locked_State else "UNLOCKED"
    ser_txt  = "MCU OK" if serial_ok else "MCU OFFLINE"

    now = time.strftime("%H:%M:%S")
    today = time.strftime("%a %b %d")

    status_top_left.value = f"{lock_txt} | {ser_txt}"
    status_top_mid.value = ""
    status_top_right.value = f"{today} | {now}"

    if Recovery_State == 1:
        mode_txt = "MODE: RECOVERY"
        mode_color = AMBER_RING
    elif Trail_Lights_State == 1:
        mode_txt = "MODE: TRAIL"
        mode_color = ON_RING
    else:
        mode_txt = "MODE: NONE"
        mode_color = TXT_DIM

    status_bot_left.value = mode_txt
    status_bot_mid.value = battery_text()

    mode = "AUTO" if Brightness_Auto else "MAN"
    status_bot_right.value = f"BRIGHT {Brightness_State}% {mode}"

    try:
        status_bot_left.tk.configure(fg=mode_color)
    except Exception:
        pass

# ==========================
# Brightness
# ==========================
def _run_backlight(pct: int):
    try:
        subprocess.run(["sudo", "rpi-backlight", "--set-brightness", str(int(pct))], check=False)
    except Exception as e:
        print(f"Brightness set failed: {e}")

def set_brightness(pct: int):
    global Brightness_State, Brightness_Auto
    Brightness_Auto = False
    try:
        pct = int(pct)
    except Exception:
        pct = 100
    pct = max(0, min(100, pct))
    Brightness_State = pct
    _run_backlight(Brightness_State)
    request_refresh()

def set_brightness_auto():
    global Brightness_Auto
    Brightness_Auto = True
    _run_backlight(Brightness_State)
    request_refresh()

def refresh_brightness_buttons():
    for name, btn in brightness_buttons.items():
        if name == "AUTO":
            ring = AMBER_RING if Brightness_Auto else OFF_RING
        else:
            active = (not Brightness_Auto) and (Brightness_State == name)
            ring = ON_RING if active else OFF_RING
        _set_ring(btn, ring)

# ==========================
# Lock
# ==========================
def _set_locked(locked: bool):
    global Locked_State
    Locked_State = 1 if locked else 0
    for b in lockable_buttons:
        try:
            b.enabled = not locked
        except Exception:
            pass
    request_refresh()

# ==========================
# Exit popup
# ==========================
def _do_exit():
    global exit_popup, app
    try:
        if exit_popup is not None:
            try:
                exit_popup.tk.grab_release()
            except Exception:
                pass
            exit_popup.destroy()
            exit_popup = None
    except Exception:
        pass

    try:
        if ser is not None:
            ser.close()
    except Exception:
        pass

    try:
        if app is not None:
            app.destroy()
    except Exception:
        pass

    sys.exit(0)

def _show_exit_confirmation():
    global exit_popup, app

    try:
        if exit_popup is not None:
            exit_popup.show()
            exit_popup.tk.attributes("-topmost", True)
            exit_popup.tk.attributes("-topmost", False)
            return
    except Exception:
        exit_popup = None

    exit_popup = Window(app, title="EXIT", width=800, height=480)
    exit_popup.bg = BG
    exit_popup.tk.attributes("-fullscreen", True)
    exit_popup.tk.config(cursor="none")
    exit_popup.tk.attributes("-topmost", True)
    exit_popup.tk.grab_set()

    def _hide_exit():
        try:
            exit_popup.tk.grab_release()
        except Exception:
            pass
        exit_popup.hide()

    outer = Box(exit_popup, layout="grid", width="fill", height="fill")
    outer.bg = BG
    outer.tk.grid_rowconfigure(0, weight=1)
    outer.tk.grid_rowconfigure(2, weight=1)
    outer.tk.grid_columnconfigure(0, weight=1)
    outer.tk.grid_columnconfigure(2, weight=1)

    center = Box(outer, layout="grid", grid=[1, 1])
    center.bg = BG

    msg = Text(center, text="EXIT CONTROL PANEL?", color=TXT, size=30, grid=[0, 0, 2, 1])
    msg.bg = BG

    yes_btn = PushButton(center, text="YES", grid=[0, 1], width=10, height=2, command=_do_exit)
    no_btn  = PushButton(center, text="NO",  grid=[1, 1], width=10, height=2, command=_hide_exit)
    yes_btn.text_color = TXT
    no_btn.text_color  = TXT
    yes_btn.bg = "#444b55"
    no_btn.bg  = "#2a2f36"

    try:
        yes_btn.tk.grid_configure(padx=12, pady=12, sticky="e")
        no_btn.tk.grid_configure(padx=12, pady=12, sticky="w")
    except Exception:
        pass

    exit_popup.when_closed = _hide_exit

# ==========================
# PIN keypad
# ==========================
def _show_pin_unlock():
    global pin_popup, app

    try:
        if pin_popup is not None:
            pin_popup.show()
            pin_popup.tk.attributes("-topmost", True)
            pin_popup.tk.attributes("-topmost", False)
            return
    except Exception:
        pin_popup = None

    pin_popup = Window(app, title="PIN", width=800, height=480)
    pin_popup.bg = BG
    pin_popup.tk.attributes("-fullscreen", True)
    pin_popup.tk.config(cursor="none")
    pin_popup.tk.attributes("-topmost", True)
    pin_popup.tk.grab_set()

    entered = {"v": ""}

    def _render(display):
        n = len(entered["v"])
        dots = ["●" if i < n else "○" for i in range(6)]
        display.value = " ".join(dots)

    def reset_pin(display, status):
        entered["v"] = ""
        status.value = ""
        _render(display)

    def _hide_pin(display, status):
        try:
            pin_popup.tk.grab_release()
        except Exception:
            pass
        reset_pin(display, status)
        pin_popup.hide()

    outer = Box(pin_popup, layout="grid", width="fill", height="fill")
    outer.bg = BG
    outer.tk.grid_rowconfigure(0, weight=1)
    outer.tk.grid_rowconfigure(2, weight=1)
    outer.tk.grid_columnconfigure(0, weight=1)
    outer.tk.grid_columnconfigure(2, weight=1)

    center = Box(outer, layout="grid", grid=[1, 1])
    center.bg = BG

    title = Text(center, text="ENTER 6-DIGIT PIN", color=TXT, size=26, grid=[0, 0, 3, 1])
    title.bg = BG
    display = Text(center, text="○ ○ ○ ○ ○ ○", color=TXT, size=30, grid=[0, 1, 3, 1])
    display.bg = BG
    status = Text(center, text="", color=WARN, size=16, grid=[0, 2, 3, 1])
    status.bg = BG

    def add_digit(d):
        if len(entered["v"]) < 6:
            entered["v"] += str(d)
            status.value = ""
            _render(display)

    def back():
        entered["v"] = entered["v"][:-1]
        _render(display)

    def clear():
        entered["v"] = ""
        _render(display)

    def enter():
        if entered["v"] == PIN_CODE:
            _hide_pin(display, status)
            _set_locked(False)
        else:
            status.value = "INCORRECT PIN"
            entered["v"] = ""
            _render(display)

    keypad = Box(center, layout="grid", grid=[0, 3, 3, 1])
    keypad.bg = BG
    try:
        keypad.tk.grid_columnconfigure(0, weight=1, uniform="k")
        keypad.tk.grid_columnconfigure(1, weight=1, uniform="k")
        keypad.tk.grid_columnconfigure(2, weight=1, uniform="k")
    except Exception:
        pass

    def mk_key(txt, gx, gy, cmd, bg="#2a2f36"):
        b = PushButton(keypad, text=txt, grid=[gx, gy], command=cmd, width=6, height=2)
        b.text_color = TXT
        b.bg = bg
        try:
            b.tk.grid_configure(padx=2, pady=2, sticky="nsew")
        except Exception:
            pass
        return b

    mk_key("1", 0, 0, lambda: add_digit(1))
    mk_key("2", 1, 0, lambda: add_digit(2))
    mk_key("3", 2, 0, lambda: add_digit(3))
    mk_key("4", 0, 1, lambda: add_digit(4))
    mk_key("5", 1, 1, lambda: add_digit(5))
    mk_key("6", 2, 1, lambda: add_digit(6))
    mk_key("7", 0, 2, lambda: add_digit(7))
    mk_key("8", 1, 2, lambda: add_digit(8))
    mk_key("9", 2, 2, lambda: add_digit(9))
    mk_key("CLR", 0, 3, clear, bg="#444b55")
    mk_key("0",   1, 3, lambda: add_digit(0))
    mk_key("⌫",   2, 3, back, bg="#444b55")

    actions = Box(center, layout="grid", grid=[0, 4, 3, 1])
    actions.bg = BG
    try:
        actions.tk.grid_columnconfigure(0, weight=1)
        actions.tk.grid_columnconfigure(1, weight=1)
    except Exception:
        pass

    cancel_btn = PushButton(actions, text="CANCEL", grid=[0, 0], command=lambda: _hide_pin(display, status),
                            width=10, height=2)
    enter_btn  = PushButton(actions, text="ENTER",  grid=[1, 0], command=enter, width=10, height=2)
    cancel_btn.text_color = TXT
    cancel_btn.bg = "#444b55"
    enter_btn.text_color = TXT
    enter_btn.bg = "#1f6bff"

    try:
        cancel_btn.tk.grid_configure(padx=10, pady=10, sticky="e")
        enter_btn.tk.grid_configure(padx=10, pady=10, sticky="w")
    except Exception:
        pass

    pin_popup.when_closed = lambda: _hide_pin(display, status)
    reset_pin(display, status)

def Lock_Callback():
    if Locked_State == 0:
        _set_locked(True)
    else:
        _show_pin_unlock()

# ==========================
# Setters
# ==========================
def Fog_Lights_Set(on: bool):
    global Fog_Lights_State
    if on and Fog_Lights_State == 0:
        Fog_Lights_State = 1; send("0")
    elif (not on) and Fog_Lights_State == 1:
        Fog_Lights_State = 0; send("1")
    request_refresh()

def Light_Bar_Set(on: bool):
    global Light_Bar_State
    if on and Light_Bar_State == 0:
        Light_Bar_State = 1; send("2")
    elif (not on) and Light_Bar_State == 1:
        Light_Bar_State = 0; send("3")
    request_refresh()

def Ditch_Lights_Set(on: bool):
    global Ditch_Lights_State
    if on and Ditch_Lights_State == 0:
        Ditch_Lights_State = 1; send("4")
    elif (not on) and Ditch_Lights_State == 1:
        Ditch_Lights_State = 0; send("5")
    request_refresh()

def Backup_Lights_Set(on: bool):
    global Backup_Lights_State
    if on and Backup_Lights_State == 0:
        Backup_Lights_State = 1; send("6")
    elif (not on) and Backup_Lights_State == 1:
        Backup_Lights_State = 0; send("7")
    request_refresh()

def Truck_Bed_Lights_Set(on: bool):
    global Truck_Bed_Lights_State
    if on and Truck_Bed_Lights_State == 0:
        Truck_Bed_Lights_State = 1; send("8")
    elif (not on) and Truck_Bed_Lights_State == 1:
        Truck_Bed_Lights_State = 0; send("9")
    request_refresh()

def Rock_Lights_Set(on: bool):
    global Rock_Lights_State
    if on and Rock_Lights_State == 0:
        Rock_Lights_State = 1; send("A")
    elif (not on) and Rock_Lights_State == 1:
        Rock_Lights_State = 0; send("B")
    request_refresh()

def Chase_Lights_Set(on: bool):
    global Chase_Lights_State
    if on and Chase_Lights_State == 0:
        Chase_Lights_State = 1; send("C")
    elif (not on) and Chase_Lights_State == 1:
        Chase_Lights_State = 0; send("D")
    request_refresh()

def Air_Compressor_Set(on: bool):
    global Air_Compressor_State
    if on and Air_Compressor_State == 0:
        Air_Compressor_State = 1; send("E")
    elif (not on) and Air_Compressor_State == 1:
        Air_Compressor_State = 0; send("F")
    request_refresh()

def Winch_Set(on: bool):
    global Winch_State
    if on and Winch_State == 0:
        Winch_State = 1; send("G")
    elif (not on) and Winch_State == 1:
        Winch_State = 0; send("H")
    request_refresh()

def VHF_UHF_Radio_Set(on: bool):
    global VHF_UHF_Radio_State
    if on and VHF_UHF_Radio_State == 0:
        VHF_UHF_Radio_State = 1; send("I")
    elif (not on) and VHF_UHF_Radio_State == 1:
        VHF_UHF_Radio_State = 0; send("J")
    request_refresh()

def HF_Radio_Set(on: bool):
    global HF_Radio_State
    if on and HF_Radio_State == 0:
        HF_Radio_State = 1; send("K")
    elif (not on) and HF_Radio_State == 1:
        HF_Radio_State = 0; send("L")
    request_refresh()

def Scanner_Set(on: bool):
    global Scanner_State
    if on and Scanner_State == 0:
        Scanner_State = 1; send("M")
    elif (not on) and Scanner_State == 1:
        Scanner_State = 0; send("N")
    request_refresh()

def Computer_Set(on: bool):
    global Computer_State
    if on and Computer_State == 0:
        Computer_State = 1; send("O")
    elif (not on) and Computer_State == 1:
        Computer_State = 0; send("P")
    request_refresh()

def AC_Power_Set(on: bool):
    global AC_Power_State
    if on and AC_Power_State == 0:
        AC_Power_State = 1; send("Q")
    elif (not on) and AC_Power_State == 1:
        AC_Power_State = 0; send("R")
    request_refresh()

def Truck_Bed_12VDC_Set(on: bool):
    global Truck_Bed_12VDC_State
    if on and Truck_Bed_12VDC_State == 0:
        Truck_Bed_12VDC_State = 1; send("S")
    elif (not on) and Truck_Bed_12VDC_State == 1:
        Truck_Bed_12VDC_State = 0; send("T")
    request_refresh()

def Button_16_Set(on: bool):
    global Button_16_State
    if on and Button_16_State == 0:
        Button_16_State = 1; send("U")
    elif (not on) and Button_16_State == 1:
        Button_16_State = 0; send("V")
    request_refresh()

# ==========================
# modes + NEW group toggles
# ==========================
def apply_modes():
    begin_batch()
    try:
        if Recovery_State == 1:
            Fog_Lights_Set(True); Light_Bar_Set(True); Ditch_Lights_Set(True)
            Backup_Lights_Set(True); Truck_Bed_Lights_Set(True)
            Rock_Lights_Set(True); Chase_Lights_Set(True)
            Air_Compressor_Set(True); Winch_Set(True)
            return

        if Trail_Lights_State == 1:
            Fog_Lights_Set(True); Light_Bar_Set(True); Ditch_Lights_Set(True)
            Rock_Lights_Set(True); Chase_Lights_Set(True)
            Backup_Lights_Set(False); Truck_Bed_Lights_Set(False)
            Air_Compressor_Set(False); Winch_Set(False)
            return

        Fog_Lights_Set(False); Light_Bar_Set(False); Ditch_Lights_Set(False)
        Rock_Lights_Set(False); Chase_Lights_Set(False)
        Backup_Lights_Set(False); Truck_Bed_Lights_Set(False)
        Air_Compressor_Set(False); Winch_Set(False)
    finally:
        end_batch()

def Comms_Group_Toggle():
    global Comms_Group_State
    if Locked_State == 1:
        return

    Comms_Group_State ^= 1
    begin_batch()
    try:
        VHF_UHF_Radio_Set(bool(Comms_Group_State))
        HF_Radio_Set(bool(Comms_Group_State))
        Scanner_Set(bool(Comms_Group_State))
        Computer_Set(bool(Comms_Group_State))
    finally:
        end_batch()
    request_refresh()

def Power_Group_Toggle():
    global Power_Group_State
    if Locked_State == 1:
        return

    Power_Group_State ^= 1
    begin_batch()
    try:
        AC_Power_Set(bool(Power_Group_State))
        Truck_Bed_12VDC_Set(bool(Power_Group_State))
    finally:
        end_batch()
    request_refresh()

# ==========================
# Callbacks (guarded)
# ==========================
def _if_unlocked(fn):
    def wrapper():
        if Locked_State == 1:
            return
        fn()
    return wrapper

def Trail_Lights_Callback():
    global Trail_Lights_State
    if Locked_State == 1:
        return
    Trail_Lights_State ^= 1
    apply_modes()
    request_refresh()

def Recovery_Callback():
    global Recovery_State
    if Locked_State == 1:
        return
    Recovery_State ^= 1
    apply_modes()
    request_refresh()

# ==========================
# Build GUI
# ==========================
app = App(title="CONTROL PANEL", width=800, height=480, layout="grid")
app.bg = BG

# IMPORTANT: Make main grid columns equal width (prevents top-row widgets from resizing columns)
for c in range(5):
    try:
        app.tk.grid_columnconfigure(c, weight=1)
    except Exception:
        pass

try:
    app.tk.grid_rowconfigure(0, weight=0)  # top bar
    app.tk.grid_rowconfigure(1, weight=1)
    app.tk.grid_rowconfigure(2, weight=1)
    app.tk.grid_rowconfigure(3, weight=1)
    app.tk.grid_rowconfigure(4, weight=1)
    app.tk.grid_rowconfigure(5, weight=0)  # brightness
except Exception:
    pass

def make_btn(label, r, c, cb, lockable=True):
    b = PushButton(app, text=label, grid=[c, r], command=cb, width=BTN_W, height=BTN_H)
    b.text_color = TXT
    b.bg = PANEL
    buttons[label] = b
    if lockable:
        lockable_buttons.append(b)
    return b

# ==========================
# TOP BAR (LOCK/EXIT fixed pixel width, status fills)
# ==========================
TOP_FIXED_W = 130  # pixels
TOP_FIXED_H = 90   # pixels

topbar = Box(app, layout="grid", grid=[0, 0, 5, 1], width="fill", height=TOP_FIXED_H)
topbar.bg = BG

try:
    # lock topbar height
    topbar.tk.grid_propagate(False)
    topbar.tk.grid_configure(sticky="nsew", padx=0, pady=0)
    app.tk.grid_rowconfigure(0, minsize=TOP_FIXED_H, weight=0)

    # 3-column topbar: LOCK | STATUS | EXIT
    topbar.tk.grid_columnconfigure(0, minsize=TOP_FIXED_W, weight=0)
    topbar.tk.grid_columnconfigure(1, weight=1)
    topbar.tk.grid_columnconfigure(2, minsize=TOP_FIXED_W, weight=0)

    topbar.tk.grid_rowconfigure(0, weight=1)
except Exception:
    pass

# ---- LOCK (fixed column width) ----
lock_top = PushButton(topbar, text="LOCK", grid=[0, 0], command=Lock_Callback)
lock_top.text_color = TXT
lock_top.bg = PANEL
buttons["LOCK"] = lock_top
try:
    lock_top.tk.grid_configure(sticky="nsew")
except Exception:
    pass

# ---- STATUS (fills) ----
status_bar = Box(topbar, layout="grid", grid=[1, 0], width="fill", height=TOP_FIXED_H)
status_bar.bg = BG
try:
    status_bar.tk.grid_configure(sticky="nsew", padx=0, pady=0)

    # give left more room than mid/right
    status_bar.tk.grid_columnconfigure(0, weight=6)
    status_bar.tk.grid_columnconfigure(1, weight=0)
    status_bar.tk.grid_columnconfigure(2, weight=4)

    status_bar.tk.grid_rowconfigure(0, weight=1)
    status_bar.tk.grid_rowconfigure(1, weight=1)
except Exception:
    pass

status_top_left  = Text(status_bar, text="", grid=[0, 0], color=TXT, size=14)
status_top_mid   = Text(status_bar, text="", grid=[1, 0], color=TXT_DIM, size=14)
status_top_right = Text(status_bar, text="", grid=[2, 0], color=TXT_DIM, size=14)

status_bot_left  = Text(status_bar, text="", grid=[0, 1], color=TXT_DIM, size=12)
status_bot_mid   = Text(status_bar, text="", grid=[1, 1], color=TXT_DIM, size=12)
status_bot_right = Text(status_bar, text="", grid=[2, 1], color=TXT_DIM, size=12)

for t in (status_top_left, status_top_mid, status_top_right,
          status_bot_left, status_bot_mid, status_bot_right):
    t.bg = BG
    try:
        t.tk.configure(font=STATUS_FONT)
    except Exception:
        pass

try:
    status_top_left.tk.configure(anchor="w")
    status_bot_left.tk.configure(anchor="w")
    status_top_mid.tk.configure(anchor="center")
    status_bot_mid.tk.configure(anchor="center")
    status_top_right.tk.configure(anchor="e")
    status_bot_right.tk.configure(anchor="e")
except Exception:
    pass

EDGE_PAD = 12
try:
    status_top_left.tk.grid_configure(sticky="ew", padx=(EDGE_PAD, 0), pady=(6, 0))
    status_top_mid.tk.grid_configure(sticky="ew", pady=(6, 0))
    status_top_right.tk.grid_configure(sticky="ew", padx=(0, EDGE_PAD), pady=(6, 0))

    status_bot_left.tk.grid_configure(sticky="ew", padx=(EDGE_PAD, 0), pady=(0, 6))
    status_bot_mid.tk.grid_configure(sticky="ew", pady=(0, 6))
    status_bot_right.tk.grid_configure(sticky="ew", padx=(0, EDGE_PAD), pady=(0, 6))
except Exception:
    pass

# ---- EXIT (fixed column width) ----
exit_top = PushButton(topbar, text="EXIT", grid=[2, 0], command=_show_exit_confirmation)
exit_top.text_color = TXT
exit_top.bg = PANEL
buttons["EXIT"] = exit_top
try:
    exit_top.tk.grid_configure(sticky="nsew")
except Exception:
    pass

# ---- MAIN GRID rows 1-4 ----
make_btn("FOG\nLIGHTS",        1, 0, _if_unlocked(lambda: Fog_Lights_Set(not bool(Fog_Lights_State))))
make_btn("LIGHT\nBAR",         1, 1, _if_unlocked(lambda: Light_Bar_Set(not bool(Light_Bar_State))))
make_btn("DITCH\nLIGHTS",      1, 2, _if_unlocked(lambda: Ditch_Lights_Set(not bool(Ditch_Lights_State))))
make_btn("BACKUP\nLIGHTS",     1, 3, _if_unlocked(lambda: Backup_Lights_Set(not bool(Backup_Lights_State))))
make_btn("BED\nLIGHTS",        1, 4, _if_unlocked(lambda: Truck_Bed_Lights_Set(not bool(Truck_Bed_Lights_State))))

make_btn("ROCK\nLIGHTS",       2, 0, _if_unlocked(lambda: Rock_Lights_Set(not bool(Rock_Lights_State))))
make_btn("CHASE\nLIGHTS",      2, 1, _if_unlocked(lambda: Chase_Lights_Set(not bool(Chase_Lights_State))))
make_btn("AIR\nCOMP",          2, 2, _if_unlocked(lambda: Air_Compressor_Set(not bool(Air_Compressor_State))))
make_btn("WINCH",              2, 3, _if_unlocked(lambda: Winch_Set(not bool(Winch_State))))
make_btn("VHF/UHF\nRADIO",     2, 4, _if_unlocked(lambda: VHF_UHF_Radio_Set(not bool(VHF_UHF_Radio_State))))

make_btn("HF\nRADIO",          3, 0, _if_unlocked(lambda: HF_Radio_Set(not bool(HF_Radio_State))))
make_btn("SCANNER",            3, 1, _if_unlocked(lambda: Scanner_Set(not bool(Scanner_State))))
make_btn("PC\nACCS",           3, 2, _if_unlocked(lambda: Computer_Set(not bool(Computer_State))))
make_btn("120VAC\nPOWER",      3, 3, _if_unlocked(lambda: AC_Power_Set(not bool(AC_Power_State))))
make_btn("12VDC\nPOWER",       3, 4, _if_unlocked(lambda: Truck_Bed_12VDC_Set(not bool(Truck_Bed_12VDC_State))))

make_btn("SPARE",              4, 0, _if_unlocked(lambda: Button_16_Set(not bool(Button_16_State))))
make_btn("TRAIL\nLIGHTS",      4, 1, Trail_Lights_Callback)
make_btn("TRAIL\nRECOVERY",    4, 2, Recovery_Callback)

# group buttons
make_btn("COMMS",              4, 3, Comms_Group_Toggle, lockable=True)
make_btn("POWER",              4, 4, Power_Group_Toggle, lockable=True)

# ---- BRIGHTNESS ROW ----
def make_bright(name, col, cb):
    b = PushButton(app, text=str(name), grid=[col, 5], command=cb, width=BTN_W, height=2)
    b.text_color = TXT
    b.bg = PANEL
    try:
        b.tk.grid_configure(padx=PAD_X, pady=PAD_Y, sticky="nsew")
    except Exception:
        pass
    return b

brightness_buttons[25]     = make_bright("25%", 0, lambda: set_brightness(25))
brightness_buttons[50]     = make_bright("50%", 1, lambda: set_brightness(50))
brightness_buttons[75]     = make_bright("75%", 2, lambda: set_brightness(75))
brightness_buttons[100]    = make_bright("100%", 3, lambda: set_brightness(100))
brightness_buttons["AUTO"] = make_bright("AUTO", 4, set_brightness_auto)

# ==========================
# Refresh
# ==========================
def refresh_all():
    style_main_button("FOG\nLIGHTS", Fog_Lights_State)
    style_main_button("LIGHT\nBAR", Light_Bar_State)
    style_main_button("DITCH\nLIGHTS", Ditch_Lights_State)
    style_main_button("BACKUP\nLIGHTS", Backup_Lights_State)
    style_main_button("BED\nLIGHTS", Truck_Bed_Lights_State)

    style_main_button("ROCK\nLIGHTS", Rock_Lights_State)
    style_main_button("CHASE\nLIGHTS", Chase_Lights_State)
    style_main_button("AIR\nCOMP", Air_Compressor_State)
    style_main_button("WINCH", Winch_State)
    style_main_button("VHF/UHF\nRADIO", VHF_UHF_Radio_State)

    style_main_button("HF\nRADIO", HF_Radio_State)
    style_main_button("SCANNER", Scanner_State)
    style_main_button("PC\nACCS", Computer_State)
    style_main_button("120VAC\nPOWER", AC_Power_State)
    style_main_button("12VDC\nPOWER", Truck_Bed_12VDC_State)

    style_main_button("SPARE", Button_16_State)
    style_main_button("TRAIL\nLIGHTS", Trail_Lights_State)
    style_main_button("TRAIL\nRECOVERY", Recovery_State)

    style_main_button("COMMS", Comms_Group_State)
    style_main_button("POWER", Power_Group_State)

    # Lock/Exit (top bar)
    if Locked_State == 1:
        _set_ring(buttons["LOCK"], LOCK_RING)
    else:
        _set_ring(buttons["LOCK"], OFF_RING)
    _set_ring(buttons["EXIT"], NEUTRAL_RING)

    refresh_brightness_buttons()
    update_status_bar()

# ==========================
# Boot
# ==========================
def main():
    app.tk.attributes("-fullscreen", True)
    app.tk.config(cursor="none")

    set_brightness_auto()
    refresh_all()

    def tick():
        update_status_bar()

    app.repeat(1000, tick)
    app.display()

if __name__ == "__main__":
    main()