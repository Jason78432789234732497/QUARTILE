import tkinter as tk

APP_BG = "#54f458"
TEXT_FG = "#000000"
BTN_CLEAR = "#a0ff5c"
BTN_MATH = "#41ff36"
BTN_CLOSE_TOP = "#ff6d6d"
BTN_CLOSE_BOTTOM = "#ff4b5d"
ICON_FG = "#ffffff"

BASE_FONT = ("Lucida Grande", 11)
TITLE_FONT = ("Lucida Grande", 11, "bold")


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.resizable(False, False)
        self.configure(bg=APP_BG)
        self.geometry("320x420")

        self.expr = ""
        self._drag_x = 0
        self._drag_y = 0

        self._build_titlebar()
        self._build_ui()

        # Keyboard bindings
        self.bind("<Key>", self._key_press)
        self.bind("<Return>", lambda e: self._press("="))
        self.bind("<BackSpace>", lambda e: self._backspace())

    # ----- titlebar -----

    def _build_titlebar(self):
        bar = tk.Frame(self, bg=APP_BG, height=30)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        title = tk.Label(bar, text="Quartile Calc", bg=APP_BG,
                         fg=TEXT_FG, font=TITLE_FONT)
        title.pack(side="left", padx=10)

        close = self._stacked_button(bar, BTN_CLOSE_TOP, BTN_CLOSE_BOTTOM, "✕",
                                     command=self.destroy)
        close.pack(side="right", padx=10, pady=5)

        for w in (bar, title):
            w.bind("<Button-1>", self._start_move)
            w.bind("<B1-Motion>", self._on_move)

    def _stacked_button(self, parent, top_color, bottom_color, text, command):
        canvas = tk.Canvas(parent, width=40, height=20,
                           highlightthickness=0, bd=0, bg=APP_BG)
        canvas.create_rectangle(0, 0, 40, 10, fill=top_color, outline=top_color)
        canvas.create_rectangle(0, 10, 40, 20, fill=bottom_color, outline=bottom_color)
        canvas.create_text(20, 10, text=text, fill=ICON_FG, font=BASE_FONT)
        canvas.bind("<Button-1>", lambda e: command())
        return canvas

    def _start_move(self, e):
        self._drag_x = e.x
        self._drag_y = e.y

    def _on_move(self, e):
        self.geometry(f"+{e.x_root - self._drag_x}+{e.y_root - self._drag_y}")

    # ----- UI -----

    def _build_ui(self):
        self.display = tk.Entry(self, bg="#ffffff", fg=TEXT_FG,
                                insertbackground=TEXT_FG, bd=0,
                                font=("Lucida Grande", 18), justify="right")
        self.display.pack(fill="x", padx=10, pady=10, ipady=10)

        frame = tk.Frame(self, bg=APP_BG)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        buttons = [
            ("C", BTN_CLEAR), ("±", BTN_MATH), ("%", BTN_MATH), ("÷", BTN_MATH),
            ("7", BTN_MATH), ("8", BTN_MATH), ("9", BTN_MATH), ("×", BTN_MATH),
            ("4", BTN_MATH), ("5", BTN_MATH), ("6", BTN_MATH), ("−", BTN_MATH),
            ("1", BTN_MATH), ("2", BTN_MATH), ("3", BTN_MATH), ("+", BTN_MATH),
            ("0", BTN_MATH), (".", BTN_MATH), ("π", BTN_MATH), ("=", BTN_MATH),
        ]

        for i, (txt, bg) in enumerate(buttons):
            r, c = divmod(i, 4)
            b = tk.Button(frame, text=txt, bg=bg, fg=TEXT_FG,
                          bd=0, font=BASE_FONT, width=4, height=2,
                          command=lambda t=txt: self._press(t))
            b.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            frame.grid_rowconfigure(i, weight=1)

    # ----- logic -----

    def _press(self, char):
        if char == "C":
            self.expr = ""
        elif char == "=":
            try:
                e = (self.expr
                     .replace("×", "*")
                     .replace("÷", "/")
                     .replace("−", "-")
                     .replace("π", "3.1415926535"))
                self.expr = str(eval(e))
            except Exception:
                self.expr = ">:/ nuh uh"
        elif char == "±":
            if self.expr.startswith("-"):
                self.expr = self.expr[1:]
            elif self.expr:
                self.expr = "-" + self.expr
        else:
            self.expr += char

        self.display.delete(0, "end")
        self.display.insert(0, self.expr)

    def _backspace(self):
        self.expr = self.expr[:-1]
        self.display.delete(0, "end")
        self.display.insert(0, self.expr)

    def _key_press(self, event):
        key = event.char

        # Numbers and normal operators
        if key.isdigit() or key in "+-*/.%":
            self._press(key)

        # P = π
        elif key.lower() == "p":
            self._press("π")

        # C = clear
        elif key.lower() == "c":
            self._press("C")

        # Enter handled separately
        # Backspace handled separately


if __name__ == "__main__":
    Calculator().mainloop()
