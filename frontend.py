import customtkinter as ctk

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

COLUMNS = ["ID", "Name", "Year", "Major", "GPA"]
COL_W   = [60, 160, 90, 180, 60]


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Records")
        self.geometry("920x640")
        self.minsize(820, 580)
        self.configure(fg_color=BG_DEEP)
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

        # Buttons — no commands attached
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
                      corner_radius=6, height=38
                      ).grid(row=6, column=0, padx=12, pady=2, sticky="ew")

        # ── Main panel ─────────────────────────────────────────────────────────
        main = ctk.CTkFrame(self, fg_color=BG_PANEL, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew", padx=(1, 0))
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=0, height=60)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        ctk.CTkLabel(hdr, text="Student Records", font=FONT_HEAD,
                     text_color=TEXT_PRI).grid(row=0, column=0, padx=24, sticky="w")

        # Table area
        table_outer = ctk.CTkFrame(main, fg_color=BG_DEEP, corner_radius=0)
        table_outer.grid(row=1, column=0, sticky="nsew")
        table_outer.grid_columnconfigure(0, weight=1)
        table_outer.grid_rowconfigure(1, weight=1)

        # Column headers
        col_hdr = ctk.CTkFrame(table_outer, fg_color=BG_CARD, corner_radius=0, height=36)
        col_hdr.grid(row=0, column=0, sticky="ew")
        col_hdr.grid_propagate(False)
        x = 12
        for col, w in zip(COLUMNS, COL_W):
            ctk.CTkLabel(col_hdr, text=col.upper(), font=("Courier New", 9, "bold"),
                         text_color=ACCENT, width=w, anchor="w"
                         ).place(x=x, rely=0.5, anchor="w")
            x += w + 12

        # Empty scrollable body
        ctk.CTkScrollableFrame(
            table_outer, fg_color=BG_DEEP,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
            corner_radius=0
        ).grid(row=1, column=0, sticky="nsew")

        # Status bar
        status_bar = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=0, height=28)
        status_bar.grid(row=2, column=0, sticky="ew")
        status_bar.grid_propagate(False)
        ctk.CTkLabel(status_bar, text="Ready", font=FONT_MONO,
                     text_color=TEXT_SEC).grid(row=0, column=0, padx=16, sticky="w")
