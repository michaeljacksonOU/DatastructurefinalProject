import os
import customtkinter as ctk
from student_data import load_students, build_hash_table

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_DEEP    = "#0f1117"
BG_PANEL   = "#161b27"
BG_CARD    = "#1c2333"
BG_ROW_ALT = "#212840"
ACCENT     = "#4f8ef7"
ACCENT2    = "#6c63ff"
DANGER     = "#e05c6a"
TEXT_PRI   = "#e8eaf6"
TEXT_SEC   = "#7986cb"
BORDER     = "#2a3050"

FONT_HEAD  = ("Courier New", 22, "bold")
FONT_BTN   = ("Courier New", 12, "bold")
FONT_LABEL = ("Courier New", 11)
FONT_MONO  = ("Courier New", 10)

# (display label, JSON key(s), column width)
# Name combines first+last; Year has no JSON field so shows "N/A"
COLUMNS = [
    ("ID",    "student_id",               60),
    ("Name",  ("first_name", "last_name"),160),
    ("Major", "major",                    180),
    ("GPA",   "gpa",                       60),
]


def get_cell(student: dict, key) -> str:
    """Resolve a JSON key, tuple of keys, or None → display string."""
    if key is None:
        return "N/A"
    if isinstance(key, tuple):
        return " ".join(str(student.get(k, "")) for k in key).strip()
    return str(student.get(key, ""))


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Records")
        self.geometry("920x640")
        self.minsize(820, 580)
        self.configure(fg_color=BG_DEEP)

        # Resolve mock_data.json relative to this file's directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._students = load_students(os.path.join(base_dir, "mock_data.json"))
        self._hash_table = build_hash_table(self._students)
        self._filtered_students = self._students
        

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar ────────────────────────────────────────────────────────────
        sidebar = ctk.CTkFrame(self, width=220, fg_color=BG_PANEL, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(sidebar, text="◈ STUDENT\n  DATABASE",
                     font=("Courier New", 18, "bold"),
                     text_color=ACCENT, justify="left"
                     ).grid(row=0, column=0, padx=24, pady=(28, 4), sticky="w")

        ctk.CTkLabel(sidebar, text="v1.0.0", font=FONT_MONO, text_color=TEXT_SEC
                     ).grid(row=1, column=0, padx=24, pady=(0, 24), sticky="w")

        ctk.CTkFrame(sidebar, height=1, fg_color=BORDER, corner_radius=0
                     ).grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 20))

        ctk.CTkLabel(sidebar, text="ACTIONS", font=("Courier New", 9, "bold"),
                     text_color=TEXT_SEC
                     ).grid(row=3, column=0, padx=24, pady=(0, 8), sticky="w")

        ctk.CTkButton(sidebar, text="＋  Add Student", font=FONT_BTN,
                      fg_color="transparent", hover_color=BG_CARD,
                      text_color=ACCENT, anchor="w", border_width=0,
                      corner_radius=6, height=38
                      ).grid(row=4, column=0, padx=12, pady=2, sticky="ew")

        ctk.CTkButton(sidebar, text="－  Remove Student", font=FONT_BTN,
                      fg_color="transparent", hover_color=BG_CARD,
                      text_color=DANGER, anchor="w", border_width=0,
                      corner_radius=6, height=38
                      ).grid(row=5, column=0, padx=12, pady=2, sticky="ew")

        ctk.CTkButton(sidebar, text="⌕  Find Student", font=FONT_BTN,
                      fg_color="transparent", hover_color=BG_CARD,
                      text_color=ACCENT2, anchor="w", border_width=0,
                      corner_radius=6, height=38,
                      command=self._open_search
                      ).grid(row=6, column=0, padx=12, pady=2, sticky="ew")
                        

        # ── Main panel ─────────────────────────────────────────────────────────
        main = ctk.CTkFrame(self, fg_color=BG_PANEL, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew", padx=(1, 0))
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)  # table expands
        main.grid_rowconfigure(3, weight=0)  # status bar stays fixed

        # Header
        hdr = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=0, height=60)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        ctk.CTkLabel(hdr, text="Student Records", font=FONT_HEAD,
                     text_color=TEXT_PRI).grid(row=0, column=0, padx=24, sticky="w")
        
        # Filter bar — add this between hdr and table_outer
        filter_bar = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=0, height=48)
        filter_bar.grid(row=1, column=0, sticky="ew")
        filter_bar.grid_propagate(False)

        ctk.CTkLabel(filter_bar, text="Major:", font=FONT_LABEL,
             text_color=TEXT_SEC).place(x=16, rely=0.5, anchor="w")

        self._major_var = ctk.StringVar()
        self._major_var.trace_add("write", lambda *_: self._apply_filter())
        ctk.CTkEntry(filter_bar, textvariable=self._major_var,
             font=FONT_MONO, width=160,
             fg_color=BG_DEEP, border_color=BORDER,
             text_color=TEXT_PRI, placeholder_text="e.g. Biology"
             ).place(x=70, rely=0.5, anchor="w")

        ctk.CTkLabel(filter_bar, text="Last Name:", font=FONT_LABEL,
             text_color=TEXT_SEC).place(x=248, rely=0.5, anchor="w")

        self._last_var = ctk.StringVar()
        self._last_var.trace_add("write", lambda *_: self._apply_filter())
        ctk.CTkEntry(filter_bar, textvariable=self._last_var,
             font=FONT_MONO, width=160,
             fg_color=BG_DEEP, border_color=BORDER,
             text_color=TEXT_PRI, placeholder_text="e.g. Smith"
             ).place(x=340, rely=0.5, anchor="w")

        ctk.CTkButton(filter_bar, text="✕ Clear", font=FONT_BTN,
              fg_color="transparent", hover_color=BG_DEEP,
              text_color=DANGER, border_width=0, width=70,
              command=self._clear_filter
              ).place(x=516, rely=0.5, anchor="w")

        # Table area
        table_outer = ctk.CTkFrame(main, fg_color=BG_DEEP, corner_radius=0)
        table_outer.grid(row=2, column=0, sticky="nsew")
        table_outer.grid_columnconfigure(0, weight=1)
        table_outer.grid_rowconfigure(1, weight=1)

        # Column headers
        col_hdr = ctk.CTkFrame(table_outer, fg_color=BG_CARD, corner_radius=0, height=36)
        col_hdr.grid(row=0, column=0, sticky="ew")
        col_hdr.grid_propagate(False)
        x = 12
        for label, _, w in COLUMNS:
            ctk.CTkLabel(col_hdr, text=label.upper(),
                         font=("Courier New", 9, "bold"),
                         text_color=ACCENT, width=w, anchor="w"
                         ).place(x=x, rely=0.5, anchor="w")
            x += w + 12

        # Scrollable body — populated with student rows
        self._scroll_frame = ctk.CTkScrollableFrame(
        table_outer,
        fg_color=BG_DEEP,
        scrollbar_button_color=BORDER,
        scrollbar_button_hover_color=ACCENT,
        corner_radius=0
        )
        self._scroll_frame.grid(row=1, column=0, sticky="nsew")

        self._populate_rows(self._scroll_frame)

        # Status bar
        status_bar = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=0, height=28)
        status_bar.grid(row=3, column=0, sticky="ew")
        status_bar.grid_propagate(False)
        self._status_label = ctk.CTkLabel(status_bar,
                                   text=f"{len(self._students)} students loaded",
                                   font=FONT_MONO, text_color=TEXT_SEC)
        self._status_label.grid(row=0, column=0, padx=16, sticky="w")
    def _populate_rows(self, parent: ctk.CTkScrollableFrame, students: list[dict] = None):
        """Build one label-row per student inside the scrollable frame."""
        if students is None:
            students = self._students
    
        self._row_frames = {}
        self._row_defaults = {}

        for i, student in enumerate(students):
            row_color = BG_ROW_ALT if i % 2 == 0 else BG_DEEP

            row_frame = ctk.CTkFrame(parent, fg_color=row_color,
                                 corner_radius=0, height=32)
            row_frame.pack(fill="x", pady=(0, 1))
            row_frame.pack_propagate(False)
        
            sid = student["student_id"]
            self._row_frames[sid] = row_frame
            self._row_defaults[sid] = row_color

            x = 12
            for _, key, w in COLUMNS:
                ctk.CTkLabel(row_frame,
                         text=get_cell(student, key),
                         font=FONT_MONO, text_color=TEXT_PRI,
                         width=w, anchor="w"
                         ).place(x=x, rely=0.5, anchor="w")
                x += w + 12
            
    def _open_search(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Find Student")
        dialog.geometry("400x260")
        dialog.configure(fg_color=BG_PANEL)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Enter Student ID",
                    font=FONT_LABEL, text_color=TEXT_SEC
                    ).pack(pady=(24, 6))

        entry = ctk.CTkEntry(dialog, font=FONT_BTN, width=200,
                         fg_color=BG_CARD, border_color=BORDER,
                         text_color=TEXT_PRI)
        entry.pack()
        entry.focus()

        result_label = ctk.CTkLabel(dialog, text="", font=FONT_MONO,
                                text_color=TEXT_PRI, wraplength=360)
        result_label.pack(pady=16, padx=20)

        def do_search(event=None):
            raw = entry.get().strip()
            if not raw.isdigit():
                result_label.configure(text="⚠ Please enter a valid numeric ID.",
                                   text_color=DANGER)
                return

            student = self._hash_table.get(int(raw))   # O(1) lookup
            if student:
                result_label.configure(
                    text=f"✓  {student['first_name']} {student['last_name']}\n"
                         f"Major: {student['major']}  |  GPA: {student['gpa']}\n"
                        f"Email: {student['email']}",
                    text_color=ACCENT
                )
            else:
                result_label.configure(text=f"✗  No student found with ID {raw}.",
                                   text_color=DANGER)

        entry.bind("<Return>", do_search)
        ctk.CTkButton(dialog, text="Search", font=FONT_BTN,
                  fg_color=ACCENT, text_color="#ffffff",
                  command=do_search).pack()
        
    def _apply_filter(self):
        # Cancel previous scheduled filter
        if hasattr(self, '_filter_after_id'):
            self.after_cancel(self._filter_after_id)
    
        # Schedule filter to run after 300ms of no typing
        self._filter_after_id = self.after(300, self._do_filter)

    def _do_filter(self):
        major_q = self._major_var.get().strip().lower()
        last_q  = self._last_var.get().strip().lower()

        self._filtered_students = [
            s for s in self._students
            if (not major_q or major_q in s.get("major", "").lower())
            and (not last_q  or last_q  in s.get("last_name", "").lower())
        ]
        self._refresh_table()

    def _clear_filter(self):
        self._major_var.set("")
        self._last_var.set("")

    def _refresh_table(self):
        for widget in self._scroll_frame.winfo_children():
            widget.destroy()
        self._populate_rows(self._scroll_frame, self._filtered_students)
        self._status_label.configure(
            text=f"{len(self._filtered_students)} of {len(self._students)} students"
        )