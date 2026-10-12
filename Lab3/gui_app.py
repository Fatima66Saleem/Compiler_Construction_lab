"""
Lexical Analyzer - Fatima
Compiler Construction Assignment
An attractive, elegant 2-page Tkinter GUI: rounded cards, soft shadows,
pill buttons and a donut chart — all hand-drawn on Canvas (no extra
libraries needed, works with plain tkinter).

Page 1 : Input Code
Page 2 : Analysis Result (tokens + stats + donut chart)
"""

import json # 
import math
import os
import random
from datetime import datetime

import ply.lex as lex
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


# ============================================================
# BACKEND: LEXER (PLY)
# ============================================================

reserved = {
    "if": "IF", "else": "ELSE", "while": "WHILE", "for": "FOR",
    "int": "INT", "float": "FLOAT", "char": "CHAR",
    "return": "RETURN", "void": "VOID",
}

tokens = (
    "Number", "ID", "PLUS", "MINUS", "MULT", "DIV", "LPAREN", "RPAREN",
    "EQUALS", "SEMICOLON", "LB", "RB", "LC", "RC", "COMMA",
    "GE", "LE", "EQ", "NE", "GT", "LT",
) + tuple(reserved.values())

t_GE = r">="
t_LE = r"<="
t_EQ = r"=="
t_NE = r"!="
t_PLUS = r"\+"
t_MINUS = r"-"
t_MULT = r"\*"
t_DIV = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_EQUALS = r"="
t_SEMICOLON = r";"
t_LB = r"\["
t_RB = r"\]"
t_LC = r"\{"
t_RC = r"\}"
t_COMMA = r","
t_GT = r">"
t_LT = r"<"
t_ignore = " \t\r"


def t_comment(t):
    r"\#.*"
    pass


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_Number(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value) if "." in t.value else int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


lex_errors = []


def t_error(t):
    lex_errors.append(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()

HISTORY_FILE = "lexer_history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_history_entry(code, token_list, error_list):
    history = load_history()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "code": code,
        "tokens": token_list,
        "errors": error_list,
    }
    history.insert(0, entry)
    history = history[:30]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


OPERATORS = {"PLUS", "MINUS", "MULT", "DIV", "EQUALS", "GE", "LE", "EQ", "NE", "GT", "LT"}
SEPARATORS = {"LPAREN", "RPAREN", "SEMICOLON", "LB", "RB", "LC", "RC", "COMMA"}


def get_tag(token_type):
    if token_type in reserved.values():
        return "keyword"
    if token_type == "ID":
        return "identifier"
    if token_type == "Number":
        return "number"
    if token_type in OPERATORS:
        return "operator"
    if token_type in SEPARATORS:
        return "separator"
    return ""


# ============================================================
# PALETTE
# ============================================================

LIGHT_PALETTE = {
    "bg": "#FBF9FF",
    "card": "#FFFFFF",
    "shadow": "#E8E2F7",
    "border": "#ECE7FA",
    "editor_bg": "#F5F2FF",
    "text": "#3A3A4D",
    "muted": "#9693AA",
    "accent": "#A78BFA",
    "accent_hover": "#8B5CF6",
    "accent_text": "#6D28D9",
    "success": "#2FAE79",
    "error": "#E4577E",
    "purple": "#8B5CF6",
    "green": "#34D399",
    "blue": "#60A5FA",
    "yellow": "#FBBF24",
    "pink": "#F472B6",
    "soft_purple": "#EDE9FE",
    "soft_green": "#D9F6E7",
    "soft_blue": "#E0EEFF",
    "soft_yellow": "#FDF1D6",
    "soft_pink": "#FCE7F3",
}

DARK_PALETTE = {
    "bg": "#1E1B2E",
    "card": "#2A2640",
    "shadow": "#171428",
    "border": "#3D3760",
    "editor_bg": "#241F38",
    "text": "#EDEBFA",
    "muted": "#9C97B8",
    "accent": "#A78BFA",
    "accent_hover": "#8B5CF6",
    "accent_text": "#C4B5FD",
    "success": "#34D399",
    "error": "#F472B6",
    "purple": "#A78BFA",
    "green": "#34D399",
    "blue": "#60A5FA",
    "yellow": "#FBBF24",
    "pink": "#F472B6",
    "soft_purple": "#3D3560",
    "soft_green": "#1F3B34",
    "soft_blue": "#22314D",
    "soft_yellow": "#3D341C",
    "soft_pink": "#3D2436",
}

# P is a plain dict (not reassigned) so that every `P["..."]` lookup made
# *inside a method body* automatically sees the live theme after a toggle.
P = dict(LIGHT_PALETTE)

F_TITLE = ("Georgia", 28, "bold")
F_SUBTITLE = ("Segoe UI", 11)
F_SECTION = ("Segoe UI", 13, "bold")
F_MAIN = ("Segoe UI", 10)
F_SMALL = ("Segoe UI", 9)
F_MONO = ("Consolas", 11)


# ============================================================
# REUSABLE VISUAL WIDGETS
# ============================================================

def round_points(x1, y1, x2, y2, r):
    r = min(r, (x2 - x1) / 2, (y2 - y1) / 2)
    return [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]


class RoundedCard(tk.Frame):
    """A card with real rounded corners + a soft flat shadow, that resizes
    with its parent. Put your widgets inside `.inner`."""

    def __init__(self, parent, bg=None, radius=20, shadow=True, border=None):
        # bg/border resolved at *construction* time (not def time) so a
        # theme toggle that rebuilds these cards picks up fresh colors.
        bg = bg if bg is not None else P["card"]
        border = border if border is not None else P["border"]
        super().__init__(parent, bg=P["bg"])
        self.canvas = tk.Canvas(self, bg=P["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.bg_color = bg
        self.radius = radius
        self.shadow = shadow
        self.border = border
        self._win = None
        self.canvas.bind("<Configure>", self._redraw)

    def _redraw(self, event):
        w, h = event.width, event.height
        if w < 10 or h < 10:
            return
        self.canvas.delete("card")
        if self.shadow:
            pts = round_points(7, 9, w - 1, h, self.radius)
            self.canvas.create_polygon(pts, smooth=True, fill=P["shadow"], outline="", tags="card")
        pts = round_points(1, 1, w - 8, h - 8, self.radius)
        self.canvas.create_polygon(pts, smooth=True, fill=self.bg_color, outline=self.border, tags="card")
        if self._win:
            self.canvas.delete(self._win)
        pad = 12
        self._win = self.canvas.create_window(pad, pad, window=self.inner, anchor="nw",
                                                width=max(w - 8 - 2 * pad, 10),
                                                height=max(h - 8 - 2 * pad, 10))


class PillButton(tk.Canvas):
    """A rounded, pill-shaped button drawn on canvas — no extra libraries needed."""

    def __init__(self, parent, text, command, bg=None, hover=None,
                 fg="white", width=150, height=46, font=("Segoe UI", 11, "bold"),
                 outline=None):
        # Resolved at construction time (not def time) so buttons rebuilt
        # after a theme toggle use the *current* palette, not the old one.
        bg = bg if bg is not None else P["accent"]
        hover = hover if hover is not None else P["accent_hover"]
        super().__init__(parent, width=width, height=height, bg=P["bg"],
                          highlightthickness=0, cursor="hand2")
        self.command = command
        self.bg_color = bg
        self.hover_color = hover
        self.outline = outline
        self.w, self.h = width, height
        pts = round_points(1, 1, width - 1, height - 1, height / 2)
        self.rect = self.create_polygon(pts, smooth=True, fill=bg,
                                         outline=outline or "", width=2 if outline else 0)
        self.label = self.create_text(width / 2, height / 2, text=text, fill=fg, font=font)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", lambda e: self.command())

    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)


def draw_blob_pattern(canvas, w, h, color):
    """Soft decorative circles in the header for a modern 'hero' feel."""
    canvas.create_oval(w - 160, -60, w + 40, 140, fill=color, outline="")
    canvas.create_oval(w - 70, 40, w + 90, 200, fill=color, outline="")


def draw_arrow(canvas, x1, y, x2, color):
    """A simple thick right-pointing arrow between two x positions on a canvas."""
    canvas.create_line(x1, y, x2 - 14, y, fill=color, width=5, capstyle="round")
    canvas.create_polygon(x2 - 18, y - 12, x2, y, x2 - 18, y + 12, fill=color, outline="")


def draw_donut(canvas, cx, cy, r_out, r_in, data, colors, center_text, center_sub):
    total = sum(data.values())
    if total == 0:
        canvas.create_oval(cx - r_out, cy - r_out, cx + r_out, cy + r_out,
                            fill="#EEEAF9", outline="")
    else:
        start = 90
        for (label, val), color in zip(data.items(), colors):
            if val == 0:
                continue
            extent = -360 * (val / total)
            canvas.create_arc(cx - r_out, cy - r_out, cx + r_out, cy + r_out,
                               start=start, extent=extent, fill=color, outline="", style="pieslice")
            start += extent
    canvas.create_oval(cx - r_in, cy - r_in, cx + r_in, cy + r_in, fill=P["card"], outline="")
    canvas.create_text(cx, cy - 8, text=center_text, font=("Segoe UI", 20, "bold"), fill=P["text"])
    canvas.create_text(cx, cy + 14, text=center_sub, font=F_SMALL, fill=P["muted"])


# ============================================================
# MAIN APPLICATION
# ============================================================

class LexerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer")
        self.root.geometry("1040x720")
        self.root.minsize(880, 640)
        self.root.configure(bg=P["bg"])

        self.last_tokens = []
        self.dark_mode = False
        self.active_page_name = "input"

        self.setup_ttk_style()

        self.container = tk.Frame(self.root, bg=P["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.page_input = tk.Frame(self.container, bg=P["bg"])
        self.page_result = tk.Frame(self.container, bg=P["bg"])
        for pg in (self.page_input, self.page_result):
            pg.grid(row=0, column=0, sticky="nsew")

        self.build_input_page()
        self.build_result_page()
        self.show_page(self.page_input)

    def setup_ttk_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=P["card"], fieldbackground=P["card"],
                         foreground=P["text"], rowheight=30, font=F_MONO, borderwidth=0)
        style.configure("Treeview.Heading", background=P["soft_purple"], foreground=P["accent_text"],
                         font=("Segoe UI", 10, "bold"), borderwidth=0, padding=6)
        style.map("Treeview", background=[("selected", P["soft_purple"])])

    def show_page(self, page):
        page.tkraise()
        self.active_page_name = "input" if page is self.page_input else "result"

    # ==========================================================
    # DARK MODE
    # ==========================================================
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        P.clear()
        P.update(DARK_PALETTE if self.dark_mode else LIGHT_PALETTE)
        self.rebuild_ui()

    def rebuild_ui(self):
        current_code = self.input_text.get("1.0", "end-1c") if hasattr(self, "input_text") else None
        had_results = bool(self.last_tokens)
        prev_active = self.active_page_name

        for w in self.page_input.winfo_children():
            w.destroy()
        for w in self.page_result.winfo_children():
            w.destroy()

        self.root.configure(bg=P["bg"])
        self.container.configure(bg=P["bg"])
        self.setup_ttk_style()
        self.build_input_page()
        self.build_result_page()

        if current_code is not None:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", current_code)
            self.highlight_code()

        if had_results:
            self.analyze(silent=True)

        if prev_active == "input":
            self.show_page(self.page_input)

    # ==========================================================
    # HERO HEADER (shared style, used on both pages)
    # ==========================================================
    def build_hero(self, parent, title, subtitle, height=120, title_x=34):
        hero = tk.Canvas(parent, height=height, bg=P["bg"], highlightthickness=0)
        hero.pack(fill="x", side="top")

        def redraw(event=None):
            hero.delete("all")
            w = hero.winfo_width()
            hero.create_rectangle(0, 0, w, height, fill=P["soft_purple"], outline="")
            blob_color = "#342B57" if self.dark_mode else "#E3D9FB"
            draw_blob_pattern(hero, w, height, blob_color)
            hero.create_text(title_x, height / 2 - 10, text=title, font=F_TITLE,
                              fill=P["accent_text"], anchor="w")
            hero.create_text(title_x, height / 2 + 26, text=subtitle, font=F_SUBTITLE,
                              fill=P["muted"], anchor="w")

        hero.bind("<Configure>", redraw)

        toggle_text = "\u2600  Light" if self.dark_mode else "\U0001F319  Dark"
        toggle = tk.Label(parent, text=toggle_text, font=F_SMALL, bg=P["card"],
                           fg=P["accent_text"], cursor="hand2", padx=10, pady=4)
        toggle.place(relx=1.0, x=-24, y=18, anchor="ne")
        toggle.bind("<Button-1>", lambda e: self.toggle_theme())

        return hero

    # ==========================================================
    # PAGE 1 : INPUT
    # ==========================================================
    def build_input_page(self):
        page = self.page_input

        self.build_hero(page, "Lexical Analyzer",
                         "Compiler Construction  •  turn your source code into tokens")

        body = tk.Frame(page, bg=P["bg"])
        body.pack(fill="both", expand=True, padx=36, pady=22)
        body.grid_rowconfigure(1, weight=1)
        body.grid_columnconfigure(0, weight=1)

        ex_row = tk.Frame(body, bg=P["bg"])
        ex_row.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.example_btn = tk.Label(ex_row, text="✎  Load Example  ▾", font=F_SMALL,
                                     bg=P["bg"], fg=P["accent_text"], cursor="hand2")
        self.example_btn.pack(side="right")
        self.example_btn.bind("<Button-1>", lambda e: self.show_examples())

        info_btn = tk.Label(ex_row, text="ⓘ  How it works", font=F_SMALL,
                             bg=P["bg"], fg=P["accent_text"], cursor="hand2")
        info_btn.pack(side="right", padx=(0, 20))
        info_btn.bind("<Button-1>", lambda e: self.open_how_it_works())

        history_btn = tk.Label(ex_row, text="🕓  History", font=F_SMALL,
                                bg=P["bg"], fg=P["accent_text"], cursor="hand2")
        history_btn.pack(side="right", padx=(0, 20))
        history_btn.bind("<Button-1>", lambda e: self.open_history())

        card = RoundedCard(body)
        card.grid(row=1, column=0, sticky="nsew")
        card.inner.grid_rowconfigure(1, weight=1)
        card.inner.grid_columnconfigure(0, weight=1)

        tk.Label(card.inner, text="Your Code", font=F_SECTION,
                 bg=P["card"], fg=P["text"]).grid(row=0, column=0, sticky="w", pady=(0, 10))

        editor_wrap = tk.Frame(card.inner, bg=P["editor_bg"], highlightthickness=1,
                                highlightbackground=P["border"])
        editor_wrap.grid(row=1, column=0, sticky="nsew")

        self.input_text = scrolledtext.ScrolledText(
            editor_wrap, font=F_MONO, bg=P["editor_bg"], fg=P["text"],
            insertbackground=P["accent_text"], relief="flat", bd=0,
            padx=16, pady=14, wrap="none", undo=True,
        )
        self.input_text.pack(fill="both", expand=True)
        self.input_text.insert("1.0", "int x = 10 + 5;\nif (x >= 10) {\n    return x;\n}")

        self.input_text.tag_configure("kw", foreground=P["purple"])
        self.input_text.tag_configure("num", foreground=P["success"])
        self.input_text.tag_configure("op", foreground="#B45309")
        self.input_text.tag_configure("cmt", foreground="#9AA0A6")
        self.input_text.bind("<KeyRelease>", lambda e: self.highlight_code())
        self.highlight_code()

        tk.Label(card.inner, text="Tip: write any small C-style snippet, then press Analyze.",
                 font=F_SMALL, bg=P["card"], fg=P["muted"], anchor="w").grid(
            row=2, column=0, sticky="w", pady=(8, 0))

        actions = tk.Frame(body, bg=P["bg"])
        actions.grid(row=2, column=0, sticky="ew", pady=(18, 0))
        PillButton(actions, "Analyze  →", self.analyze, width=170).pack(side="left")
        PillButton(actions, "Clear", self.clear_input, bg=P["card"], hover=P["soft_purple"],
                   fg=P["accent_text"], outline=P["accent"], width=110).pack(side="left", padx=12)

    def show_examples(self):
        menu = tk.Menu(self.root, tearoff=0, bg=P["card"], fg=P["text"],
                        activebackground=P["soft_purple"], font=F_SMALL)
        examples = {
            "Basic Arithmetic": "int x = 10 + 5;\n",
            "If Statement": "int x = 10;\nif (x >= 10) {\n    return x;\n}",
            "Loop Example": "int i = 0;\nwhile (i < 5) {\n    i = i + 1;\n}",
        }
        for name, code in examples.items():
            menu.add_command(label=name, command=lambda c=code: self.set_example(c))
        x = self.example_btn.winfo_rootx()
        y = self.example_btn.winfo_rooty() + self.example_btn.winfo_height()
        try:
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    def set_example(self, code):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", code)
        self.highlight_code()

    def clear_input(self):
        self.input_text.delete("1.0", "end")
        self.highlight_code()

    def highlight_code(self):
        """Live syntax highlighting: colors keywords, numbers, operators and
        comments as you type. Purely visual - does not affect the real PLY lexer."""
        code = self.input_text.get("1.0", "end-1c")
        for tag in ("kw", "num", "op", "cmt"):
            self.input_text.tag_remove(tag, "1.0", "end")

        keyword_set = set(reserved.keys())
        operator_chars = ["==", "!=", ">=", "<=", "+", "-", "*", "/", "=", ">", "<"]

        for line_no, line in enumerate(code.splitlines(), start=1):
            # keywords (whole-word match only)
            for word in keyword_set:
                start = 0
                while True:
                    pos = line.find(word, start)
                    if pos == -1:
                        break
                    before_ok = pos == 0 or not (line[pos - 1].isalnum() or line[pos - 1] == "_")
                    end = pos + len(word)
                    after_ok = end == len(line) or not (line[end].isalnum() or line[end] == "_")
                    if before_ok and after_ok:
                        self.input_text.tag_add("kw", f"{line_no}.{pos}", f"{line_no}.{end}")
                    start = end

            # numbers
            i = 0
            while i < len(line):
                if line[i].isdigit():
                    j = i + 1
                    while j < len(line) and (line[j].isdigit() or line[j] == "."):
                        j += 1
                    self.input_text.tag_add("num", f"{line_no}.{i}", f"{line_no}.{j}")
                    i = j
                else:
                    i += 1

            # operators
            for op in operator_chars:
                start = 0
                while True:
                    pos = line.find(op, start)
                    if pos == -1:
                        break
                    self.input_text.tag_add("op", f"{line_no}.{pos}", f"{line_no}.{pos + len(op)}")
                    start = pos + len(op)

            # comments
            cpos = line.find("#")
            if cpos != -1:
                self.input_text.tag_add("cmt", f"{line_no}.{cpos}", f"{line_no}.end")

    # ==========================================================
    # PAGE 2 : RESULT
    # ==========================================================
    def build_result_page(self):
        page = self.page_result

        hero = self.build_hero(page, "Analysis Result", "Here's what your code is made of",
                                height=110, title_x=160)

        back_holder = tk.Frame(page, bg=P["bg"])
        back_holder.place(x=26, y=32)
        PillButton(back_holder, "←  Back", lambda: self.show_page(self.page_input),
                   bg=P["card"], hover=P["soft_purple"], fg=P["accent_text"],
                   outline=P["accent"], width=110, height=40).pack()

        # A dedicated, always-present strip for the confetti celebration.
        # It sits BELOW the hero/back button so the animation never covers
        # them, and it's blank (matches page bg) when nothing is playing.
        self.celebrate_canvas = tk.Canvas(page, height=54, bg=P["bg"], highlightthickness=0)
        self.celebrate_canvas.pack(fill="x")

        body = tk.Frame(page, bg=P["bg"])
        body.pack(fill="both", expand=True, padx=36, pady=(14, 22))
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(1, weight=1)

        self.result_status = tk.Label(body, text="", font=F_MAIN, bg=P["bg"],
                                       fg=P["success"], anchor="w")
        self.result_status.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # ---- LEFT: token table ----
        table_card = RoundedCard(body)
        table_card.grid(row=1, column=0, sticky="nsew", padx=(0, 14))
        table_card.inner.grid_rowconfigure(1, weight=1)
        table_card.inner.grid_columnconfigure(0, weight=1)

        tk.Label(table_card.inner, text="Tokens", font=F_SECTION,
                 bg=P["card"], fg=P["text"]).grid(row=0, column=0, sticky="w", pady=(0, 8))

        tree_wrap = tk.Frame(table_card.inner, bg=P["card"])
        tree_wrap.grid(row=1, column=0, sticky="nsew")

        columns = ("#", "Type", "Value", "Line", "Column")
        self.tree = ttk.Treeview(tree_wrap, columns=columns, show="headings")
        widths = {"#": 36, "Type": 110, "Value": 130, "Line": 55, "Column": 65}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=widths[col],
                              stretch=col in ("Type", "Value"))
        self.tree.tag_configure("keyword", foreground=P["purple"])
        self.tree.tag_configure("identifier", foreground="#2563EB")
        self.tree.tag_configure("operator", foreground="#B45309")
        self.tree.tag_configure("number", foreground=P["success"])
        self.tree.tag_configure("separator", foreground="#0891B2")

        scroll = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.error_label = tk.Label(table_card.inner, text="", font=F_SMALL, bg=P["card"],
                                     fg=P["error"], anchor="w", wraplength=460, justify="left")
        self.error_label.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        # ---- RIGHT: donut chart + stat pills ----
        right = tk.Frame(body, bg=P["bg"])
        right.grid(row=1, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=0)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        donut_card = RoundedCard(right)
        donut_card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        donut_card.configure(height=260)
        donut_card.pack_propagate(False)

        tk.Label(donut_card.inner, text="Token Breakdown", font=F_SECTION,
                 bg=P["card"], fg=P["text"]).pack(anchor="w")

        self.donut_canvas = tk.Canvas(donut_card.inner, bg=P["card"], highlightthickness=0, height=210)
        self.donut_canvas.pack(fill="both", expand=True)
        self.donut_canvas.bind("<Motion>", self._on_donut_motion)
        self.donut_canvas.bind("<Leave>", self._on_donut_leave)
        self._current_hover = None

        legend_card = RoundedCard(right)
        legend_card.grid(row=1, column=0, sticky="nsew")

        tk.Label(legend_card.inner, text="Legend", font=F_SECTION,
                 bg=P["card"], fg=P["text"]).pack(anchor="w", pady=(0, 8))

        self.legend_rows = {}
        legend_defs = [
            ("Keywords", P["purple"]),
            ("Identifiers", P["blue"]),
            ("Operators", P["yellow"]),
            ("Numbers", P["green"]),
            ("Separators", "#0891B2"),
        ]
        for name, color in legend_defs:
            row = tk.Frame(legend_card.inner, bg=P["card"])
            row.pack(fill="x", pady=4)
            dot = tk.Canvas(row, width=14, height=14, bg=P["card"], highlightthickness=0)
            dot.create_oval(2, 2, 12, 12, fill=color, outline="")
            dot.pack(side="left")
            tk.Label(row, text=name, font=F_MAIN, bg=P["card"], fg=P["text"],
                     anchor="w").pack(side="left", padx=8)
            count_lbl = tk.Label(row, text="0", font=("Segoe UI", 10, "bold"),
                                  bg=P["card"], fg=P["muted"])
            count_lbl.pack(side="right")
            self.legend_rows[name] = count_lbl

    # ==========================================================
    # "HOW IT WORKS" EXPLAINER POPUP
    # ==========================================================
    def open_how_it_works(self):
        win = tk.Toplevel(self.root)
        win.title("How a Lexical Analyzer Works")
        win.configure(bg=P["bg"])
        win.geometry("980x640")
        win.transient(self.root)

        # ---- Title ----
        tk.Label(win, text="Lexical Analyzer  (Scanner)", font=("Georgia", 22, "bold"),
                 bg=P["bg"], fg=P["accent_text"]).pack(pady=(20, 2))
        pill = tk.Frame(win, bg=P["soft_purple"])
        pill.pack(pady=(0, 18))
        tk.Label(pill, text="Reads the source code and converts it into tokens.",
                 font=F_MAIN, bg=P["soft_purple"], fg=P["accent_text"]).pack(padx=16, pady=6)

        # ---- Row: Source Code -> Lexical Analyzer -> Tokens ----
        row = tk.Frame(win, bg=P["bg"])
        row.pack(fill="x", padx=24)
        row.grid_columnconfigure(0, weight=1, uniform="a")
        row.grid_columnconfigure(1, weight=0)
        row.grid_columnconfigure(2, weight=1, uniform="a")
        row.grid_columnconfigure(3, weight=0)
        row.grid_columnconfigure(4, weight=1, uniform="a")

        # -- Card 1: Source Code --
        c1 = RoundedCard(row, bg=P["card"])
        c1.grid(row=0, column=0, sticky="nsew")
        c1.configure(height=260)
        c1.pack_propagate(False)
        tk.Label(c1.inner, text="</>  Source Code", font=F_SECTION,
                 bg=P["card"], fg=P["text"]).pack(anchor="w")
        tk.Label(c1.inner, text="(Input)", font=F_SMALL, bg=P["card"], fg=P["muted"]).pack(anchor="w")
        code_box = tk.Frame(c1.inner, bg=P["editor_bg"], highlightthickness=1,
                             highlightbackground=P["border"])
        code_box.pack(fill="both", expand=True, pady=(10, 0))
        sample_code = "int x = 10;\nif (x >= 10) {\n    return x;\n}"
        tk.Label(code_box, text=sample_code, font=F_MONO, bg=P["editor_bg"], fg=P["text"],
                 justify="left", anchor="nw").pack(fill="both", expand=True, padx=10, pady=10)

        # -- Arrow 1 --
        a1 = tk.Canvas(row, width=50, height=40, bg=P["bg"], highlightthickness=0)
        a1.grid(row=0, column=1, sticky="s", pady=(0, 110))
        draw_arrow(a1, 4, 20, 46, P["purple"])

        # -- Card 2: Lexical Analyzer --
        c2 = RoundedCard(row, bg=P["soft_blue"])
        c2.grid(row=0, column=2, sticky="nsew")
        c2.configure(height=260)
        c2.pack_propagate(False)
        tk.Label(c2.inner, text="Lexical Analyzer", font=F_SECTION,
                 bg=P["soft_blue"], fg=P["text"]).pack(anchor="w", pady=(0, 8))
        for step in ("Reads characters", "Groups them into lexemes", "Identifies token type"):
            step_row = tk.Frame(c2.inner, bg=P["card"])
            step_row.pack(fill="x", pady=4)
            tk.Label(step_row, text="⚙", font=F_MAIN, bg=P["card"],
                     fg=P["accent_text"]).pack(side="left", padx=(8, 6), pady=6)
            tk.Label(step_row, text=step, font=F_MAIN, bg=P["card"], fg=P["text"]).pack(
                side="left", pady=6)

        # -- Arrow 2 --
        a2 = tk.Canvas(row, width=50, height=40, bg=P["bg"], highlightthickness=0)
        a2.grid(row=0, column=3, sticky="s", pady=(0, 110))
        draw_arrow(a2, 4, 20, 46, P["success"])

        # -- Card 3: Tokens output --
        c3 = RoundedCard(row, bg=P["soft_green"])
        c3.grid(row=0, column=4, sticky="nsew")
        c3.configure(height=260)
        c3.pack_propagate(False)
        tk.Label(c3.inner, text="Tokens  (Output)", font=F_SECTION,
                 bg=P["soft_green"], fg=P["text"]).pack(anchor="w", pady=(0, 6))

        sample_tokens = [
            ("int", "Keyword", P["soft_pink"]),
            ("x", "Identifier", P["soft_blue"]),
            ("=", "Operator", P["soft_yellow"]),
            ("10", "Constant", P["soft_purple"]),
            (";", "Symbol", P["soft_yellow"]),
        ]
        for tok, typ, color in sample_tokens:
            r = tk.Frame(c3.inner, bg=P["card"])
            r.pack(fill="x", pady=2)
            badge = tk.Label(r, text=tok, font=("Consolas", 9, "bold"), bg=color,
                              fg=P["text"], width=6)
            badge.pack(side="left", padx=(4, 8), pady=3)
            tk.Label(r, text=typ, font=F_SMALL, bg=P["card"], fg=P["muted"]).pack(side="left")
        tk.Label(c3.inner, text="...", font=F_MAIN, bg=P["soft_green"], fg=P["muted"]).pack(pady=(4, 0))

        # ---- Token Types legend ----
        legend_wrap = RoundedCard(win, bg=P["card"])
        legend_wrap.pack(fill="x", padx=24, pady=(20, 10))
        legend_wrap.configure(height=90)
        legend_wrap.pack_propagate(False)

        tk.Label(legend_wrap.inner, text="Token Types", font=F_SECTION,
                 bg=P["card"], fg=P["text"]).pack(anchor="w")
        chip_row = tk.Frame(legend_wrap.inner, bg=P["card"])
        chip_row.pack(anchor="w", pady=(8, 0))
        chips = [
            ("Keyword", P["soft_pink"], "int, if, return, ..."),
            ("Identifier", P["soft_blue"], "variable names"),
            ("Symbol", P["soft_yellow"], "( ) { } ; ,"),
            ("Operator", P["soft_green"], "+ - * / = > <"),
            ("Constant", P["soft_purple"], "10, 3.14, ..."),
        ]
        for name, color, desc in chips:
            chip = tk.Frame(chip_row, bg=P["bg"])
            chip.pack(side="left", padx=8)
            tk.Label(chip, text=f"  {name}  ", font=("Segoe UI", 9, "bold"), bg=color,
                     fg=P["text"]).pack()
            tk.Label(chip, text=desc, font=("Segoe UI", 8), bg=P["bg"], fg=P["muted"]).pack()

        # ---- Bottom flow: Characters -> Lexemes -> Tokens ----
        flow = tk.Frame(win, bg=P["bg"])
        flow.pack(pady=(14, 20))

        def flow_pill(parent, title, sub, color):
            box = tk.Frame(parent, bg=color)
            tk.Label(box, text=title, font=("Segoe UI", 11, "bold"), bg=color,
                     fg=P["text"]).pack(padx=22, pady=(8, 0))
            tk.Label(box, text=sub, font=F_SMALL, bg=color, fg=P["muted"]).pack(padx=22, pady=(0, 8))
            return box

        flow_pill(flow, "Characters", "(raw input)", P["soft_purple"]).pack(side="left")
        tk.Label(flow, text="  →  ", font=("Segoe UI", 12), bg=P["bg"],
                 fg=P["muted"]).pack(side="left")
        flow_pill(flow, "Lexemes", '(e.g. "int", "x")', P["soft_blue"]).pack(side="left")
        tk.Label(flow, text="  →  ", font=("Segoe UI", 12), bg=P["bg"],
                 fg=P["muted"]).pack(side="left")
        flow_pill(flow, "Tokens", "(type + value)", P["soft_green"]).pack(side="left")

        # ==========================================================
    # HISTORY POPUP
    # ==========================================================
    def open_history(self):
        win = tk.Toplevel(self.root)
        win.title("Analysis History")
        win.configure(bg=P["bg"])
        win.geometry("520x520")
        win.transient(self.root)

        tk.Label(win, text="Recent History", font=("Georgia", 18, "bold"),
                 bg=P["bg"], fg=P["accent_text"]).pack(pady=(20, 4))
        tk.Label(win, text="Click an entry to load that code back into the editor.",
                 font=F_SMALL, bg=P["bg"], fg=P["muted"]).pack(pady=(0, 14))

        list_card = RoundedCard(win, bg=P["card"])
        list_card.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        history = load_history()

        if not history:
            tk.Label(list_card.inner, text="No history yet — analyze some code first!",
                     font=F_MAIN, bg=P["card"], fg=P["muted"]).pack(pady=30)
            return

        canvas = tk.Canvas(list_card.inner, bg=P["card"], highlightthickness=0)
        scroll = ttk.Scrollbar(list_card.inner, orient="vertical", command=canvas.yview)
        rows_frame = tk.Frame(canvas, bg=P["card"])
        rows_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for entry in history:
            token_count = len(entry.get("tokens", []))
            error_count = len(entry.get("errors", []))
            row = tk.Frame(rows_frame, bg=P["soft_purple"], cursor="hand2")
            row.pack(fill="x", pady=5, padx=4)

            status_color = P["error"] if error_count else P["success"]
            status_text = f"{error_count} error(s)" if error_count else "OK"

            top = tk.Frame(row, bg=P["soft_purple"])
            top.pack(fill="x", padx=12, pady=(8, 0))
            tk.Label(top, text=entry.get("timestamp", ""), font=("Segoe UI", 10, "bold"),
                     bg=P["soft_purple"], fg=P["text"]).pack(side="left")
            tk.Label(top, text=status_text, font=F_SMALL, bg=P["soft_purple"],
                     fg=status_color).pack(side="right")

            preview = entry.get("code", "").replace("\n", "  ")[:60]
            body_lbl = tk.Label(row, text=f"{preview}...   ({token_count} tokens)",
                                 font=F_SMALL, bg=P["soft_purple"], fg=P["muted"],
                                 anchor="w", justify="left")
            body_lbl.pack(fill="x", padx=12, pady=(2, 8))

            def load_entry(event=None, code=entry.get("code", "")):
                self.set_example(code)
                win.destroy()

            for widget in (row, top, body_lbl):
                widget.bind("<Button-1>", load_entry)

    # ==========================================================
    # ANALYSIS LOGIC
    # ==========================================================
    def analyze(self, silent=False):
        code = self.input_text.get("1.0", "end-1c")
        if not code.strip():
            if not silent:
                messagebox.showwarning("Empty Code", "Pehle kuch code likho!")
            return

        lex_errors.clear()
        lexer.lineno = 1
        lexer.input(code)

        for row in self.tree.get_children():
            self.tree.delete(row)

        token_list = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            line_start = code.rfind("\n", 0, tok.lexpos) + 1
            column = tok.lexpos - line_start + 1
            token_list.append({"type": tok.type, "value": str(tok.value),
                                "line": tok.lineno, "column": column})
            self.tree.insert("", "end", values=(len(token_list), tok.type, tok.value,
                                                  tok.lineno, column),
                              tags=(get_tag(tok.type),))

        self.last_tokens = token_list
        errors = list(lex_errors)

        counts = {
            "Keywords": sum(t["type"] in reserved.values() for t in token_list),
            "Identifiers": sum(t["type"] == "ID" for t in token_list),
            "Operators": sum(t["type"] in OPERATORS for t in token_list),
            "Numbers": sum(t["type"] == "Number" for t in token_list),
            "Separators": sum(t["type"] in SEPARATORS for t in token_list),
        }
        for name, val in counts.items():
            self.legend_rows[name].config(text=str(val))

        self.prepare_donut_segments(counts)
        self._current_hover = None
        self._draw_donut_full(None)

        if errors:
            self.result_status.config(text=f"Done — {len(token_list)} tokens found, {len(errors)} error(s).",
                                       fg=P["error"])
            self.error_label.config(text="Errors: " + "  |  ".join(errors))
        else:
            self.result_status.config(text=f"Done — {len(token_list)} tokens found, no errors.",
                                       fg=P["success"])
            self.error_label.config(text="")

        if not silent:
            save_history_entry(code, token_list, errors)
            if not errors:
                self.celebrate()
        self.show_page(self.page_result)
        self.page_result.after(50, self._draw_donut_full, None)

    # ----------------------------------------------------------
    # Success celebration: a short confetti burst when there are no errors
    # ----------------------------------------------------------
    def celebrate(self):
        canvas = self.celebrate_canvas
        canvas.delete("all")

        colors = [P["purple"], P["blue"], P["yellow"], P["green"], P["pink"]]
        w = canvas.winfo_width() or 1000
        particles = []
        for _ in range(26):
            x = random.uniform(20, max(40, w - 20))
            y = random.uniform(-24, 8)
            vx = random.uniform(-1.0, 1.0)
            vy = random.uniform(1.3, 2.4)
            size = random.randint(5, 9)
            color = random.choice(colors)
            pid = canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
            particles.append([pid, x, y, vx, vy, size])

        def step(frame=0):
            if not canvas.winfo_exists():
                return
            if frame > 34:
                canvas.delete("all")
                return
            for p in particles:
                pid, x, y, vx, vy, size = p
                x += vx
                y += vy
                vy += 0.18
                canvas.coords(pid, x, y, x + size, y + size)
                p[1], p[2], p[4] = x, y, vy
            canvas.after(20, step, frame + 1)

        step()

    # ----------------------------------------------------------
    # Interactive donut: hover a slice -> it pops out + shows its detail
    # ----------------------------------------------------------
    def prepare_donut_segments(self, counts):
        colors = [P["purple"], P["blue"], P["yellow"], P["green"], "#0891B2"]
        total = sum(counts.values())
        self.donut_total = total
        segments = []
        std_start = 90.0
        cw_cursor = 0.0
        for label, color in zip(counts.keys(), colors):
            val = counts[label]
            frac = (val / total) if total else 0
            std_extent = -360 * frac
            segments.append({
                "label": label, "value": val, "color": color,
                "std_start": std_start, "std_extent": std_extent,
                "cw_start": cw_cursor, "cw_end": cw_cursor + 360 * frac,
            })
            std_start += std_extent
            cw_cursor += 360 * frac
        self.donut_segments = segments

    def _draw_donut_full(self, hover_label):
        canvas = self.donut_canvas
        canvas.delete("all")
        w = canvas.winfo_width() or 240
        h = canvas.winfo_height() or 210
        cx, cy = w / 2, h / 2
        r_out = min(w, h) / 2 - 14
        r_in = min(w, h) / 2 - 40

        total = getattr(self, "donut_total", 0)
        segs = getattr(self, "donut_segments", [])

        if not total:
            canvas.create_oval(cx - r_out, cy - r_out, cx + r_out, cy + r_out,
                                fill="#EEEAF9", outline="")
        else:
            for seg in segs:
                if seg["value"] == 0:
                    continue
                is_hover = seg["label"] == hover_label
                offset = 9 if is_hover else 0
                rr = r_out + (5 if is_hover else 0)
                mid_std = math.radians(seg["std_start"] + seg["std_extent"] / 2)
                ox = offset * math.cos(mid_std)
                oy = -offset * math.sin(mid_std)
                canvas.create_arc(cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr,
                                   start=seg["std_start"], extent=seg["std_extent"],
                                   fill=seg["color"], outline=P["card"], width=2,
                                   style="pieslice")

        canvas.create_oval(cx - r_in, cy - r_in, cx + r_in, cy + r_in, fill=P["card"], outline="")

        if hover_label and total:
            seg = next(s for s in segs if s["label"] == hover_label)
            pct = round(100 * seg["value"] / total) if total else 0
            canvas.create_text(cx, cy - 10, text=str(seg["value"]),
                                font=("Segoe UI", 20, "bold"), fill=P["text"])
            canvas.create_text(cx, cy + 15, text=f"{seg['label']}  ({pct}%)",
                                font=F_SMALL, fill=P["muted"])
        else:
            canvas.create_text(cx, cy - 8, text=str(total),
                                font=("Segoe UI", 20, "bold"), fill=P["text"])
            canvas.create_text(cx, cy + 14, text="tokens", font=F_SMALL, fill=P["muted"])

        self._donut_geo = (cx, cy, r_out, r_in)

    def _on_donut_motion(self, event):
        if not getattr(self, "donut_segments", None) or not getattr(self, "donut_total", 0):
            return
        cx, cy, r_out, r_in = self._donut_geo
        dx, dy = event.x - cx, event.y - cy
        r = math.hypot(dx, dy)

        if r > r_out + 16:
            if getattr(self, "_current_hover", None) is not None:
                self._current_hover = None
                self._draw_donut_full(None)
            return

        std_angle = math.degrees(math.atan2(-dy, dx)) % 360
        cw = (90 - std_angle) % 360

        hovered = None
        for seg in self.donut_segments:
            if seg["value"] == 0:
                continue
            if seg["cw_start"] <= cw < seg["cw_end"]:
                hovered = seg["label"]
                break

        if hovered != getattr(self, "_current_hover", None):
            self._current_hover = hovered
            self._draw_donut_full(hovered)

    def _on_donut_leave(self, event):
        if getattr(self, "_current_hover", None) is not None:
            self._current_hover = None
            self._draw_donut_full(None)


if __name__ == "__main__":
    root = tk.Tk()
    app = LexerApp(root)
    root.mainloop()