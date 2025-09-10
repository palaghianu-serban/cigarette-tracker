import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar # type: ignore
from datetime import date

DARK_BG = "#23272e"
DARK_PANEL = "#2c313c"
DARK_ACCENT = "#4f5b66"
TEXT_MAIN = "#e0e0e0"
TEXT_ACCENT = "#ffb74d"

def create_analytics_page(app):
    analytics_page = tk.Frame(app, bg=DARK_BG)
    app.frames["analytics_page"] = analytics_page

    tk.Label(analytics_page, text="Analytics", font=("Segoe UI", 15, "bold"), bg=DARK_BG, fg=TEXT_ACCENT).pack(pady=(20, 10))

    cal_frame = tk.Frame(analytics_page, bg=DARK_BG)
    cal_frame.pack(pady=(0, 10))

    app.calendar = Calendar(
        cal_frame,
        selectmode='day',
        year=date.today().year,
        month=date.today().month,
        day=date.today().day,
        background=DARK_PANEL,
        foreground=TEXT_MAIN,
        headersbackground=DARK_ACCENT,
        headersforeground=TEXT_MAIN,
        selectbackground=TEXT_ACCENT,
        selectforeground=DARK_BG,
        weekendbackground=DARK_BG,
        weekendforeground=TEXT_ACCENT,
        othermonthforeground=TEXT_ACCENT,
        othermonthbackground=DARK_BG,
        bordercolor=DARK_ACCENT,
        normalbackground=DARK_BG,
        normalforeground=TEXT_MAIN,
        font=("Segoe UI", 10)
    )
    app.calendar.pack()

    btn_frame = tk.Frame(analytics_page, bg=DARK_BG)
    btn_frame.pack(pady=10)

    # Show Selected buttons (horizontal)
    horizontal_btns = tk.Frame(btn_frame, bg=DARK_BG)
    horizontal_btns.pack()

    ttk.Button(horizontal_btns, text="Show Selected Day", style="Rounded.TButton", command=app.show_selected_day_analytics).pack(side="left", padx=4)
    ttk.Button(horizontal_btns, text="Show Selected Month", style="Rounded.TButton", command=app.show_selected_month_analytics).pack(side="left", padx=4)
    ttk.Button(horizontal_btns, text="Show Selected Year", style="Rounded.TButton", command=app.show_selected_year_analytics).pack(side="left", padx=4)

    # Edit Previous Entry button below the horizontal buttons
    ttk.Button(btn_frame, text="Edit Previous Entry", style="Rounded.TButton", command=app.show_edit_entry_dialog).pack(pady=8)

    # Trends, Best/Worst, Weekday Distribution (side by side)
    analysis_btns = tk.Frame(btn_frame, bg=DARK_BG)
    analysis_btns.pack(pady=8)

    ttk.Button(analysis_btns, text="Show Trends", style="Rounded.TButton", command=app.show_trend_selector).pack(side="left", padx=4)
    ttk.Button(analysis_btns, text="Show Best/Worst Days", style="Rounded.TButton", command=app.show_best_worst_selector).pack(side="left", padx=4)
    ttk.Button(analysis_btns, text="Show Weekday Distribution", style="Rounded.TButton", command=app.show_weekday_distribution).pack(side="left", padx=4)

    app.analytics_label = tk.Label(analytics_page, text="", font=("Segoe UI", 12), bg=DARK_BG, fg=TEXT_MAIN, justify="left")
    app.analytics_label.pack(pady=10)
    ttk.Button(analytics_page, text="Back", style="Rounded.TButton", command=lambda: app.show_frame("main_menu")).pack(pady=8)