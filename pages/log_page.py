import tkinter as tk
from tkinter import ttk
from datetime import date

DARK_BG = "#23272e"
TEXT_MAIN = "#e0e0e0"
TEXT_ACCENT = "#ffb74d"
ERROR_COLOR = "#e57373"

def restore_entry_default(entry_widget, default_text):
    if not entry_widget.get():
        entry_widget.insert(0, default_text)

def create_log_page(app):
    log_page = tk.Frame(app, bg=DARK_BG)
    app.frames["log_page"] = log_page

    tk.Label(log_page, text="Log Today's Entry", font=("Segoe UI", 14, "bold"), bg=DARK_BG, fg=TEXT_ACCENT).pack(pady=10)

    today_str = date.today().isoformat()
    today_entry = next((e for e in app.data.get("entries", []) if e["entry_date"] == today_str), None)

    app.log_entry = tk.Entry(log_page, font=("Segoe UI", 12), bg=DARK_BG, fg=TEXT_MAIN, justify="center")
    app.log_entry.pack(pady=10)

    # Set default value to today's entry if exists, else 0
    if today_entry:
        app.log_entry.delete(0, tk.END)
        app.log_entry.insert(0, str(today_entry.get("cigs_smoked", 0)))
    else:
        app.log_entry.delete(0, tk.END)
        app.log_entry.insert(0, "0")

    app.log_entry.bind("<FocusIn>", lambda e: app.log_entry.delete(0, tk.END))
    app.log_entry.bind("<FocusOut>", lambda e: restore_entry_default(app.log_entry, "0"))

    app.log_submit_btn = ttk.Button(log_page, text="Submit", style="Rounded.TButton", command=app.submit_log)
    app.log_submit_btn.pack(pady=8)

    app.log_results_label = tk.Label(log_page, text="", font=("Segoe UI", 11), bg=DARK_BG, fg=TEXT_ACCENT, justify="left")
    app.log_results_label.pack(pady=(8, 4))

    app.log_confirm_label = tk.Label(log_page, text="", font=("Segoe UI", 11), bg=DARK_BG, fg=ERROR_COLOR)
    app.log_confirm_label.pack(pady=(4, 4))

    ttk.Button(log_page, text="Back", style="Rounded.TButton", command=lambda: app.show_frame("main_menu")).pack(pady=8)
    ttk.Button(log_page, text="Reset Today's Entry", style="Rounded.TButton", command=app.reset_today_entry).pack(pady=8)