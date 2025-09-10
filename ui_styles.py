def set_styles(app):
    from tkinter import ttk
    DARK_BG = "#23272e"
    DARK_PANEL = "#2c313c"
    DARK_ACCENT = "#4f5b66"
    TEXT_MAIN = "#e0e0e0"
    TEXT_ACCENT = "#ffb74d"
    style = ttk.Style(app)
    style.theme_use('clam')
    style.configure("TButton",
                    font=("Segoe UI", 11),
                    padding=8,
                    background=DARK_ACCENT,
                    foreground=TEXT_MAIN,
                    borderwidth=0,
                    relief="flat")
    style.map("TButton",
              background=[('active', DARK_PANEL)],
              foreground=[('active', TEXT_ACCENT)])
    style.configure("Rounded.TButton",
                    font=("Segoe UI", 11),
                    padding=8,
                    background=DARK_ACCENT,
                    foreground=TEXT_MAIN,
                    borderwidth=0,
                    relief="flat")
    style.layout("Rounded.TButton", [
        ("Button.border", {"sticky": "nswe", "children": [
            ("Button.focus", {"sticky": "nswe", "children": [
                ("Button.padding", {"sticky": "nswe", "children": [
                    ("Button.label", {"sticky": "nswe"})
                ]})
            ]})
        ]})
    ])
    style.configure("TLabel",
                    background=DARK_BG,
                    foreground=TEXT_MAIN)
    style.configure("TEntry",
                    fieldbackground=DARK_PANEL,
                    foreground=TEXT_MAIN,
                    background=DARK_PANEL)