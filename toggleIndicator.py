"""
Self-visible on/off indicator for the autoaim toggle.

This draws a small always-on-top label on *your own* screen that reads
"AIMBOT: ON" / "AIMBOT: OFF" so you can see at a glance whether the autoaim
is currently active. It is a local Tkinter overlay: it only ever renders on
this machine's display. It does not change how the aimbot behaves, and it does
nothing to make the tool less noticeable to anyone else.

Note: like any desktop overlay, it will not draw over a game running in
exclusive fullscreen. Use borderless/windowed mode if you want to see it.
"""

import threading

try:
    import tkinter as tk
    _TK_AVAILABLE = True
except Exception:  # pragma: no cover - tkinter missing on some minimal installs
    _TK_AVAILABLE = False


class ToggleIndicator:
    def __init__(self, x: int = 20, y: int = 20):
        self._state = False
        self._running = True
        self._x = x
        self._y = y
        self._available = _TK_AVAILABLE
        if self._available:
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        else:
            print("ToggleIndicator: tkinter not available, falling back to console only.")

    def set(self, enabled: bool):
        """Update the displayed state. Thread-safe (simple flag write)."""
        self._state = bool(enabled)

    def stop(self):
        self._running = False

    def _run(self):
        self._root = tk.Tk()
        self._root.overrideredirect(True)          # no window chrome
        self._root.attributes("-topmost", True)    # stay above other windows
        try:
            self._root.attributes("-alpha", 0.80)  # slight transparency
        except Exception:
            pass
        self._root.configure(bg="black")
        self._root.geometry(f"+{self._x}+{self._y}")
        self._label = tk.Label(
            self._root,
            text="AIMBOT: OFF",
            font=("Consolas", 14, "bold"),
            fg="#ff5555",
            bg="black",
            padx=12,
            pady=5,
        )
        self._label.pack()
        self._tick()
        self._root.mainloop()

    def _tick(self):
        if not self._running:
            self._root.destroy()
            return
        if self._state:
            self._label.config(text="AIMBOT: ON", fg="#55ff55")
        else:
            self._label.config(text="AIMBOT: OFF", fg="#ff5555")
        self._root.after(50, self._tick)
