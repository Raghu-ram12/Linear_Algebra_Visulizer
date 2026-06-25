import tkinter as tk
from tkinter import ttk, messagebox
from state import *
import math
from vector_math import *
import transformations


VECTOR_COLORS = [
    "#FF4444",
    "#4488FF",
    "#44DD44",
    "#FF44FF",
    "#44DDDD",
    "#FFD700",
    "#FFA500",
    "#AA44FF",
    "#00C5CD",
    "#FF6666",
]

BG_DARK = "#1a1a1a"
BG_PANEL = "#222222"
BG_SECTION = "#2a2a2a"
FG_TEXT = "#e0e0e0"
FG_DIM = "#888888"
ACCENT = "#4488FF"
BORDER = "#3a3a3a"
CANVAS_BG = "#0d0d0d"
SELECTED_BG = "#1a3a5c"



class Render:

    def __init__(self, height, width, canvas):
        self.cos_30 = math.cos(math.radians(30))
        self.sin_30 = math.sin(math.radians(30))
        self.width = width
        self.height = height
        self.screen_origin = None
        self.scale = 20
        self.axis_len = 10
        self.canvas = canvas
        self.colour_index = 0
        self.theta_x = 35.26
        self.theta_y = 45
        self.theta_z = 0
        self._update_trig()
        self.projection = "orthographic"

    def _get_next_color(self):
        c = VECTOR_COLORS[self.colour_index % len(VECTOR_COLORS)]
        self.colour_index += 1
        return c

    def _update_trig(self):
        self.sx = math.sin(math.radians(self.theta_x))
        self.cx = math.cos(math.radians(self.theta_x))
        self.sy = math.sin(math.radians(self.theta_y))
        self.cy = math.cos(math.radians(self.theta_y))
        self.sz = math.sin(math.radians(self.theta_z))
        self.cz = math.cos(math.radians(self.theta_z))

    def _rotate(self, x, y, z):
        y1 = y * self.cx - z * self.sx
        z1 = y * self.sx + z * self.cx
        x1 = x
        x2 = x1 * self.cy + z1 * self.sy
        z2 = -x1 * self.sy + z1 * self.cy
        y2 = y1
        x3 = x2 * self.cz - y2 * self.sz
        y3 = x2 * self.sz + y2 * self.cz
        z3 = z2
        return x3, y3, z3

    def world_to_screen(self, x, y):
        return x * self.scale + self.width / 2, -y * self.scale + self.height / 2

    def project(self, x, y, z):
        x, y, z = self._rotate(x, y, z)
        if self.projection == "isometric":
            x2 = (x - y) * self.cos_30
            y2 = (x + y) * self.sin_30 - z
            return self.world_to_screen(x2, y2)
        return self.world_to_screen(x, y)

    # kept as alias so nothing breaks
    isometric_projection_screen = project

    def draw_coordinate_plane(self, grid=False):
        self.screen_origin = self.project(0, 0, 0)

        if grid:
            cur = -self.axis_len
            while cur <= self.axis_len:
                s = self.project(-self.axis_len, 0, cur)
                e = self.project(self.axis_len, 0, cur)
                self.canvas.create_line(
                    s[0], s[1], e[0], e[1], fill="#252525", width=0.5
                )
                s = self.project(cur, 0, -self.axis_len)
                e = self.project(cur, 0, self.axis_len)
                self.canvas.create_line(
                    s[0], s[1], e[0], e[1], fill="#252525", width=0.5
                )
                cur += 1

        axes = [
            ("X", self.axis_len, 0, 0, -self.axis_len, 0, 0, "#4466FF"),
            ("Y", 0, self.axis_len, 0, 0, -self.axis_len, 0, "#FF4444"),
            ("Z", 0, 0, self.axis_len, 0, 0, -self.axis_len, "#44AA44"),
        ]
        for label, px, py, pz, nx, ny, nz, col in axes:
            ps = self.project(px, py, pz)
            ns = self.project(nx, ny, nz)
            # positive half solid, negative half dashed
            self.canvas.create_line(
                self.screen_origin[0],
                self.screen_origin[1],
                ps[0],
                ps[1],
                fill=col,
                width=1.2,
                arrow=tk.LAST,
            )
            self.canvas.create_line(
                self.screen_origin[0],
                self.screen_origin[1],
                ns[0],
                ns[1],
                fill=col,
                width=1.2,
                dash=(4, 4),
            )
            self.canvas.create_text(
                ps[0] + 10,
                ps[1] - 10,
                text=f"+{label}",
                fill=col,
                font=("Consolas", 10, "bold"),
            )
            self.canvas.create_text(
                ns[0] - 10, ns[1] + 10, text=f"−{label}", fill=col, font=("Consolas", 9)
            )

    def draw_vector_on_canvas(self, v: Vector, highlight=False):
        if not v.color or v.color == "white":
            v.color = self._get_next_color()
        sx, sy = self.project(v.components[0], v.components[1], v.components[2])
        width = 3 if highlight else 2
        color = v.color
        # draw a faint halo when highlighted
        if highlight:
            self.canvas.create_line(
                self.screen_origin[0],
                self.screen_origin[1],
                sx,
                sy,
                fill="#ffffff",
                width=6,
                arrow=tk.LAST,
                capstyle=tk.ROUND,
            )
        vid = self.canvas.create_line(
            self.screen_origin[0],
            self.screen_origin[1],
            sx,
            sy,
            fill=color,
            width=width,
            arrow=tk.LAST,
        )
        v.vector_id = vid


# ── UI ────────────────────────────────────────────────────────────────────────
class UI(Render):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.root = tk.Tk()
        self.root.title("Linear Algebra Visualiser")
        self.root.configure(bg=BG_DARK)
        self.root.geometry(f"{width}x{height}")

        # canvas
        self.canvas = tk.Canvas(
            self.root,
            height=height,
            width=width - PANEL_WIDTH,
            bg=CANVAS_BG,
            highlightthickness=0,
        )

        # scrollable panel
        self.panel_outer = tk.Frame(self.root, width=PANEL_WIDTH, bg=BG_PANEL)
        self._panel_canvas = tk.Canvas(
            self.panel_outer, bg=BG_PANEL, highlightthickness=0, width=PANEL_WIDTH
        )
        self._scrollbar = ttk.Scrollbar(
            self.panel_outer, orient="vertical", command=self._panel_canvas.yview
        )
        self._panel_canvas.configure(yscrollcommand=self._scrollbar.set)
        self._scrollbar.pack(side="right", fill="y")
        self._panel_canvas.pack(side="left", fill="both", expand=True)
        self.frame = tk.Frame(self._panel_canvas, bg=BG_PANEL, width=PANEL_WIDTH)
        self._frame_window = self._panel_canvas.create_window(
            (0, 0), window=self.frame, anchor="nw"
        )
        self.frame.bind(
            "<Configure>",
            lambda e: self._panel_canvas.configure(
                scrollregion=self._panel_canvas.bbox("all")
            ),
        )

        self._active_input_frame = None
        self.status_var = tk.StringVar(value="Ready")

        super().__init__(height=height, width=width - PANEL_WIDTH, canvas=self.canvas)

    # ── helpers ───────────────────────────────────────────────────────────────
    def _section(self, title):
        """Returns a labelled frame for grouping controls."""
        lf = tk.LabelFrame(
            self.frame,
            text=title,
            fg=ACCENT,
            bg=BG_SECTION,
            font=("Consolas", 9, "bold"),
            bd=1,
            relief="flat",
            labelanchor="nw",
            padx=6,
            pady=4,
        )
        lf.pack(fill="x", padx=6, pady=(6, 2))
        return lf

    def _btn(self, parent, text, cmd, **kw):
        b = tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=BG_SECTION,
            fg=FG_TEXT,
            activebackground=ACCENT,
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Consolas", 9),
            bd=0,
            padx=6,
            pady=4,
            **kw,
        )
        b.pack(fill="x", padx=4, pady=2)
        return b

    def _label(self, parent, text):
        tk.Label(
            parent, text=text, bg=BG_SECTION, fg=FG_DIM, font=("Consolas", 8)
        ).pack(anchor="w", padx=4)

    def _entry(self, parent, placeholder=""):
        e = tk.Entry(
            parent,
            bg="#333333",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
            font=("Consolas", 10),
            bd=4,
        )
        e.pack(fill="x", padx=4, pady=2)
        if placeholder:
            e.insert(0, placeholder)
            e.config(fg=FG_DIM)
            e.bind(
                "<FocusIn>", lambda ev, en=e, ph=placeholder: self._clear_ph(ev, en, ph)
            )
            e.bind(
                "<FocusOut>", lambda ev, en=e, ph=placeholder: self._add_ph(ev, en, ph)
            )
        return e

    def _clear_ph(self, _, entry, ph):
        if entry.get() == ph:
            entry.delete(0, tk.END)
            entry.config(fg=FG_TEXT)

    def _add_ph(self, _, entry, ph):
        if not entry.get():
            entry.insert(0, ph)
            entry.config(fg=FG_DIM)

    def _set_status(self, msg, color=FG_TEXT):
        self.status_var.set(msg)
        self.status_label.config(fg=color)
        self.root.after(
            3000,
            lambda: self.status_var.set("Ready") or self.status_label.config(fg=FG_DIM),
        )

    def _close_input(self):
        if self._active_input_frame:
            self._active_input_frame.destroy()
            self._active_input_frame = None

    def _open_input(self, builder):
        self._close_input()
        f = tk.Frame(self.frame, bg=BG_SECTION, bd=0, relief="flat")
        f.pack(fill="x", padx=6, pady=4)
        self._active_input_frame = f
        builder(f)

    def _selected_vectors(self):
        indices = self.vector_list.curselection()
        if not indices:
            self._set_status("⚠  Select a vector first", "#FF8844")
        return [Vector.all_vectors[i] for i in indices]

    # ── build ─────────────────────────────────────────────────────────────────
    def build_ui(self):
        self.axis_len = 20
        self.draw_coordinate_plane(grid=True)

        # ── View section ──
        view_sec = self._section("  View")
        self._render_sliders(view_sec)
        self._render_zoom_slider(view_sec)

        row = tk.Frame(view_sec, bg=BG_SECTION)
        row.pack(fill="x", pady=2)
        tk.Button(
            row,
            text="Reset View",
            bg=BG_SECTION,
            fg=FG_DIM,
            relief="flat",
            cursor="hand2",
            font=("Consolas", 8),
            command=self._reset_view,
        ).pack(side="left", padx=4)
        tk.Button(
            row,
            text="Toggle Grid",
            bg=BG_SECTION,
            fg=FG_DIM,
            relief="flat",
            cursor="hand2",
            font=("Consolas", 8),
            command=self._toggle_grid,
        ).pack(side="left", padx=4)
        self._grid_on = True

        # ── Add Vector section ──
        add_sec = self._section("  Add Vector")
        self._render_vector_input_field(add_sec)

        # ── Transform section ──
        tr_sec = self._section("  Transform Selected")
        btn_row1 = tk.Frame(tr_sec, bg=BG_SECTION)
        btn_row1.pack(fill="x")
        for label, cmd in [
            ("Scale", self._open_scale),
            ("Rotate", self._open_rotate),
            ("Reflect", self._open_reflect),
        ]:
            tk.Button(
                btn_row1,
                text=label,
                bg="#333333",
                fg=FG_TEXT,
                activebackground=ACCENT,
                relief="flat",
                cursor="hand2",
                font=("Consolas", 9),
                bd=0,
                padx=8,
                pady=4,
                command=cmd,
            ).pack(side="left", padx=3, pady=4)

        # ── Vector List section ──
        list_sec = self._section("  Vectors")
        self._render_vector_list_box(list_sec)

        list_btn_row = tk.Frame(list_sec, bg=BG_SECTION)
        list_btn_row.pack(fill="x", pady=2)
        for label, cmd in [
            ("Delete", self._delete_selected),
            ("Rename", self._rename_selected),
        ]:
            tk.Button(
                list_btn_row,
                text=label,
                bg="#333333",
                fg=FG_TEXT,
                activebackground="#FF4444" if label == "Delete" else ACCENT,
                relief="flat",
                cursor="hand2",
                font=("Consolas", 9),
                bd=0,
                padx=8,
                pady=3,
                command=cmd,
            ).pack(side="left", padx=3)

        # ── Info panel ──
        info_sec = self._section("  Info")
        self.info_label = tk.Label(
            info_sec,
            text="—",
            bg=BG_SECTION,
            fg=FG_DIM,
            font=("Consolas", 8),
            justify="left",
            anchor="w",
            wraplength=PANEL_WIDTH - 24,
        )
        self.info_label.pack(fill="x", padx=4, pady=2)

        # ── Status bar ──
        self.status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#111111",
            fg=FG_DIM,
            font=("Consolas", 8),
            anchor="w",
            padx=8,
        )
        self.status_label.pack(side="bottom", fill="x")

        self.panel_outer.pack(side="left", fill="y")
        self.canvas.pack(side="right", expand=True, fill="both")

        # keyboard shortcuts
        self.root.bind("<Delete>", lambda e: self._delete_selected())
        self.root.bind("<Escape>", lambda e: self._close_input())
        self.root.bind(
            "<Control-z>", lambda e: self._set_status("Undo not yet implemented")
        )

        self.root.mainloop()

    # ── view controls ─────────────────────────────────────────────────────────
    def _render_sliders(self, parent):
        labels = [
            ("Rotate X", "theta_x", -180, 180, self.theta_x),
            ("Rotate Y", "theta_y", -180, 180, self.theta_y),
            ("Rotate Z", "theta_z", -180, 180, self.theta_z),
        ]
        for lbl, attr, lo, hi, default in labels:
            row = tk.Frame(parent, bg=BG_SECTION)
            row.pack(fill="x", padx=4, pady=1)
            tk.Label(
                row,
                text=lbl,
                bg=BG_SECTION,
                fg=FG_DIM,
                font=("Consolas", 8),
                width=10,
                anchor="w",
            ).pack(side="left")
            val_var = tk.StringVar(value=f"{default:.0f}°")
            tk.Label(
                row,
                textvariable=val_var,
                bg=BG_SECTION,
                fg=ACCENT,
                font=("Consolas", 8),
                width=5,
            ).pack(side="right")
            sl = tk.Scale(
                row,
                from_=lo,
                to=hi,
                orient="horizontal",
                resolution=1,
                bg=BG_SECTION,
                fg=FG_TEXT,
                troughcolor="#333",
                highlightthickness=0,
                showvalue=False,
                bd=0,
            )
            sl.set(default)
            sl.pack(side="left", fill="x", expand=True)
            sl.config(
                command=lambda v, a=attr, vv=val_var: (
                    setattr(self, a, float(v)),
                    vv.set(f"{float(v):.0f}°"),
                    self.redraw(),
                )
            )

    def _render_zoom_slider(self, parent):
        row = tk.Frame(parent, bg=BG_SECTION)
        row.pack(fill="x", padx=4, pady=1)
        tk.Label(
            row,
            text="Zoom",
            bg=BG_SECTION,
            fg=FG_DIM,
            font=("Consolas", 8),
            width=10,
            anchor="w",
        ).pack(side="left")
        zoom_var = tk.StringVar(value=f"{self.scale}px")
        tk.Label(
            row,
            textvariable=zoom_var,
            bg=BG_SECTION,
            fg=ACCENT,
            font=("Consolas", 8),
            width=5,
        ).pack(side="right")
        sl = tk.Scale(
            row,
            from_=5,
            to=60,
            orient="horizontal",
            resolution=1,
            bg=BG_SECTION,
            fg=FG_TEXT,
            troughcolor="#333",
            highlightthickness=0,
            showvalue=False,
            bd=0,
        )
        sl.set(self.scale)
        sl.pack(side="left", fill="x", expand=True)
        sl.config(
            command=lambda v: (
                setattr(self, "scale", int(v)),
                zoom_var.set(f"{int(v)}px"),
                self.redraw(),
            )
        )

    def _reset_view(self):
        self.theta_x = 35.26
        self.theta_y = 45
        self.theta_z = 0
        self.scale = 20
        self.redraw()
        self._set_status("View reset", ACCENT)

    def _toggle_grid(self):
        self._grid_on = not self._grid_on
        self.redraw()

   
    def _render_vector_input_field(self, parent):

        row = tk.Frame(parent, bg=BG_SECTION)
        row.pack(fill="x", padx=4, pady=4)
        entries = []
        for lbl in ("X", "Y", "Z"):
            col = tk.Frame(row, bg=BG_SECTION)
            col.pack(side="left", expand=True, fill="x", padx=2)
            tk.Label(
                col, text=lbl, bg=BG_SECTION, fg=ACCENT, font=("Consolas", 9, "bold")
            ).pack()
            e = tk.Entry(
                col,
                bg="#333",
                fg=FG_TEXT,
                insertbackground=FG_TEXT,
                relief="flat",
                font=("Consolas", 10),
                bd=3,
                width=5,
            )
            e.insert(0, "0")
            e.pack(fill="x")
            entries.append(e)
        tk.Button(
            parent,
            text="＋ Add Vector",
            bg=ACCENT,
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Consolas", 9, "bold"),
            bd=0,
            padx=6,
            pady=5,
            command=lambda: self._create_vector(entries),
        ).pack(fill="x", padx=4, pady=4)

    def _create_vector(self, entries):
        try:
            comp = [float(e.get()) for e in entries]
        except ValueError:
            self._set_status("⚠  Enter valid numbers", "#FF4444")
            return
        v = Vector(comp)
        self.draw_vector_on_canvas(v)
        v.name = f"v{len(Vector.all_vectors)}"
        label = self._vector_label(v)
        self.vector_list.insert(tk.END, label)
        self.vector_list.itemconfig(tk.END, fg=v.color, selectbackground=SELECTED_BG)
        for e in entries:
            e.delete(0, tk.END)
            e.insert(0, "0")
        self._set_status(f"Added {v.name}  ({comp[0]}, {comp[1]}, {comp[2]})", ACCENT)

    def _vector_label(self, v):
        c = v.components
        return f"{v.name}  ({c[0]:.2g}, {c[1]:.2g}, {c[2]:.2g})"

   
    def _render_vector_list_box(self, parent):
        self.vector_list = tk.Listbox(
            parent,
            bg="#1e1e1e",
            fg=FG_TEXT,
            selectbackground=SELECTED_BG,
            selectforeground="#ffffff",
            relief="flat",
            font=("Consolas", 9),
            activestyle="none",
            height=8,
            bd=0,
            highlightthickness=0,
        )
        self.vector_list.pack(fill="both", expand=True, padx=4, pady=4)
        self.vector_list.bind("<<ListboxSelect>>", self._on_list_select)

    def _on_list_select(self, _=None):
        indices = self.vector_list.curselection()
        self.redraw()  # redraws with highlight on selected
        if indices:
            v = Vector.all_vectors[indices[-1]]
            c = v.components
            from vector_math import magnitude

            mag = magnitude(v)
            self.info_label.config(
                text=f"Name : {v.name}\n"
                f"Comp : ({c[0]:.3g}, {c[1]:.3g}, {c[2]:.3g})\n"
                f"|v|  : {mag:.4f}"
            )
        else:
            self.info_label.config(text="—")

    def _delete_selected(self):
        indices = list(self.vector_list.curselection())
        if not indices:
            self._set_status("⚠  Select a vector to delete", "#FF8844")
            return
        for i in reversed(indices):
            v = Vector.all_vectors[i]
            Vector.all_vectors.pop(i)
            self.vector_list.delete(i)
        self.redraw()
        self._set_status(f"Deleted {len(indices)} vector(s)", "#FF6666")
        self.info_label.config(text="—")

    def _rename_selected(self):
        indices = self.vector_list.curselection()
        if not indices:
            self._set_status("⚠  Select a vector to rename", "#FF8844")
            return
        idx = indices[0]
        v = Vector.all_vectors[idx]

        # ── custom themed rename dialog ──
        dlg = tk.Toplevel(self.root)
        dlg.title("Rename Vector")
        dlg.configure(bg=BG_PANEL)
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        # centre over main window
        self.root.update_idletasks()
        rx, ry = self.root.winfo_rootx(), self.root.winfo_rooty()
        rw, rh = self.root.winfo_width(), self.root.winfo_height()
        dlg.update_idletasks()
        dw, dh = 260, 120
        dlg.geometry(f"{dw}x{dh}+{rx + rw//2 - dw//2}+{ry + rh//2 - dh//2}")

        tk.Label(
            dlg,
            text=f"New name for '{v.name}'",
            bg=BG_PANEL,
            fg=FG_DIM,
            font=("Consolas", 9),
        ).pack(anchor="w", padx=12, pady=(12, 2))

        entry = tk.Entry(
            dlg,
            bg="#333333",
            fg=FG_TEXT,
            insertbackground=FG_TEXT,
            relief="flat",
            font=("Consolas", 11),
            bd=4,
        )
        entry.insert(0, v.name)
        entry.select_range(0, tk.END)
        entry.pack(fill="x", padx=12, pady=4)
        entry.focus_set()

        result = [None]

        def confirm(_=None):
            result[0] = entry.get().strip()
            dlg.destroy()

        def cancel(_=None):
            dlg.destroy()

        btn_row = tk.Frame(dlg, bg=BG_PANEL)
        btn_row.pack(fill="x", padx=12, pady=8)
        tk.Button(
            btn_row,
            text="Rename",
            bg=ACCENT,
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            font=("Consolas", 9),
            bd=0,
            padx=10,
            pady=4,
            command=confirm,
        ).pack(side="left", padx=(0, 6))
        tk.Button(
            btn_row,
            text="Cancel",
            bg=BG_SECTION,
            fg=FG_DIM,
            relief="flat",
            cursor="hand2",
            font=("Consolas", 9),
            bd=0,
            padx=10,
            pady=4,
            command=cancel,
        ).pack(side="left")

        entry.bind("<Return>", confirm)
        entry.bind("<Escape>", cancel)
        dlg.wait_window()

        name = result[0]
        if name:
            v.name = name.strip()
            self.vector_list.delete(idx)
            self.vector_list.insert(idx, self._vector_label(v))
            self.vector_list.itemconfig(idx, fg=v.color)
            self._set_status(f"Renamed to {v.name}", ACCENT)

    def _refresh_list(self):
        self.vector_list.delete(0, tk.END)
        for v in Vector.all_vectors:
            self.vector_list.insert(tk.END, self._vector_label(v))
            self.vector_list.itemconfig(tk.END, fg=v.color)

    # ── transform panels ──────────────────────────────────────────────────────
    def _open_scale(self):
        def build(f):
            tk.Label(
                f, text="Scale factors", bg=BG_SECTION, fg=FG_DIM, font=("Consolas", 8)
            ).pack(anchor="w", padx=4)
            row = tk.Frame(f, bg=BG_SECTION)
            row.pack(fill="x", padx=4)
            entries = {}
            for lbl in ("SX", "SY", "SZ"):
                col = tk.Frame(row, bg=BG_SECTION)
                col.pack(side="left", expand=True, fill="x", padx=2)
                tk.Label(
                    col, text=lbl, bg=BG_SECTION, fg=ACCENT, font=("Consolas", 8)
                ).pack()
                e = tk.Entry(
                    col,
                    bg="#333",
                    fg=FG_TEXT,
                    insertbackground=FG_TEXT,
                    relief="flat",
                    font=("Consolas", 10),
                    bd=3,
                    width=5,
                )
                e.insert(0, "1")
                e.pack(fill="x")
                entries[lbl] = e
            tk.Button(
                f,
                text="Apply Scale",
                bg=ACCENT,
                fg="#fff",
                relief="flat",
                cursor="hand2",
                font=("Consolas", 9),
                bd=0,
                padx=6,
                pady=4,
                command=lambda: self._apply_scale(entries),
            ).pack(fill="x", padx=4, pady=4)

        self._open_input(build)

    def _apply_scale(self, entries):
        try:
            sx = float(entries["SX"].get())
            sy = float(entries["SY"].get())
            sz = float(entries["SZ"].get())
        except ValueError:
            self._set_status("⚠  Enter valid numbers", "#FF4444")
            return
        vecs = self._selected_vectors()
        if not vecs:
            return
        for v in vecs:
            nv = transformations.scale_vector(v, sx, sy, sz)
            v.components = nv.components
        self._refresh_list()
        self.redraw()
        self._set_status(f"Scaled {len(vecs)} vector(s)  ×({sx},{sy},{sz})", ACCENT)

    def _open_rotate(self):
        def build(f):
            tk.Label(
                f, text="Axis & angle", bg=BG_SECTION, fg=FG_DIM, font=("Consolas", 8)
            ).pack(anchor="w", padx=4)
            row = tk.Frame(f, bg=BG_SECTION)
            row.pack(fill="x", padx=4)
            axis_var = tk.StringVar(value="X")
            for ax in ("X", "Y", "Z"):
                tk.Radiobutton(
                    row,
                    text=ax,
                    variable=axis_var,
                    value=ax,
                    bg=BG_SECTION,
                    fg=FG_TEXT,
                    selectcolor="#444",
                    activebackground=BG_SECTION,
                    font=("Consolas", 9),
                ).pack(side="left", padx=6)
            tk.Label(
                f, text="Angle (°)", bg=BG_SECTION, fg=FG_DIM, font=("Consolas", 8)
            ).pack(anchor="w", padx=4)
            angle_entry = tk.Entry(
                f,
                bg="#333",
                fg=FG_TEXT,
                insertbackground=FG_TEXT,
                relief="flat",
                font=("Consolas", 10),
                bd=3,
            )
            angle_entry.insert(0, "45")
            angle_entry.pack(fill="x", padx=4, pady=2)
            tk.Button(
                f,
                text="Apply Rotation",
                bg=ACCENT,
                fg="#fff",
                relief="flat",
                cursor="hand2",
                font=("Consolas", 9),
                bd=0,
                padx=6,
                pady=4,
                command=lambda: self._apply_rotate(axis_var, angle_entry),
            ).pack(fill="x", padx=4, pady=4)

        self._open_input(build)

    def _apply_rotate(self, axis_var, angle_entry):
        try:
            angle = float(angle_entry.get())
        except ValueError:
            self._set_status("⚠  Enter a valid angle", "#FF4444")
            return
        axis = axis_var.get().lower()
        vecs = self._selected_vectors()
        if not vecs:
            return
        for v in vecs:
            nv = transformations.rotate_vector_about_axis(v, angle, axis)
            v.components = nv.components
        self._refresh_list()
        self.redraw()
        self._set_status(
            f"Rotated {len(vecs)} vector(s)  {angle}° about {axis.upper()}", ACCENT
        )

    def _open_reflect(self):
        def build(f):
            tk.Label(
                f,
                text="Reflection plane",
                bg=BG_SECTION,
                fg=FG_DIM,
                font=("Consolas", 8),
            ).pack(anchor="w", padx=4)
            plane_var = tk.StringVar(value="xy")
            for plane in ("xy", "yz", "xz"):
                tk.Radiobutton(
                    f,
                    text=plane.upper(),
                    variable=plane_var,
                    value=plane,
                    bg=BG_SECTION,
                    fg=FG_TEXT,
                    selectcolor="#444",
                    activebackground=BG_SECTION,
                    font=("Consolas", 9),
                ).pack(anchor="w", padx=12)
            tk.Button(
                f,
                text="Apply Reflection",
                bg=ACCENT,
                fg="#fff",
                relief="flat",
                cursor="hand2",
                font=("Consolas", 9),
                bd=0,
                padx=6,
                pady=4,
                command=lambda: self._apply_reflect(plane_var),
            ).pack(fill="x", padx=4, pady=4)

        self._open_input(build)

    def _apply_reflect(self, plane_var):
        plane = plane_var.get()
        vecs = self._selected_vectors()
        if not vecs:
            return
        for v in vecs:
            nv = transformations.reflect_on_planes(v, plane)
            if nv:
                v.components = nv.components
        self._refresh_list()
        self.redraw()
        self._set_status(
            f"Reflected {len(vecs)} vector(s) on {plane.upper()} plane", ACCENT
        )

    def redraw(self):
        self._update_trig()
        self.canvas.delete("all")
        self.draw_coordinate_plane(grid=self._grid_on)
        selected_indices = set(self.vector_list.curselection())
        for i, v in enumerate(Vector.all_vectors):
            self.draw_vector_on_canvas(v, highlight=(i in selected_indices))

    def update_vector(self, v: Vector, new_x, new_y):
        self.canvas.coords(
            v.vector_id, self.screen_origin[0], self.screen_origin[1], new_x, new_y
        )


app = UI(HEIGHT, WIDTH)
app.projection = "isometric"
app._grid_on = True
app.build_ui()
