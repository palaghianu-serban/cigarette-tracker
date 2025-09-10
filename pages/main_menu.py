import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

DARK_BG = "#23272e"
TEXT_MAIN = "#e0e0e0"
TEXT_ACCENT = "#ffb74d"

def create_main_menu(app):
    main_menu = tk.Frame(app, bg=DARK_BG)
    app.frames["main_menu"] = main_menu

    header = tk.Label(main_menu, text="Cigarette Savings Tracker", font=("Segoe UI", 18, "bold"), bg=DARK_BG, fg=TEXT_ACCENT)
    header.pack(pady=(20, 10))

    info_label = tk.Label(main_menu, text="Track your progress and savings!", font=("Segoe UI", 11), bg=DARK_BG, fg=TEXT_MAIN)
    info_label.pack(pady=(0, 10))

    app.menu_message_label = tk.Label(main_menu, text="", font=("Segoe UI", 11), bg=DARK_BG, fg="#81c784")
    app.menu_message_label.pack(pady=(0, 10))

    top_frame = tk.Frame(main_menu, bg=DARK_BG)
    top_frame.pack(fill="x", pady=(20, 10))

    # Streaks (left)
    current_streak, best_streak = app.get_streaks()
    streak_label = tk.Label(
        top_frame,
        text=f"Current streak: {current_streak} days\nBest streak: {best_streak} days",
        font=("Segoe UI", 13, "bold"),
        bg=DARK_BG,
        fg=TEXT_ACCENT,
        anchor="w",
        justify="left"
    )
    streak_label.pack(side="left", padx=(10, 0))
    app.streak_label = streak_label

    # Totals (right)
    total_money, total_time = app.get_all_time_totals()
    totals_label = tk.Label(
        top_frame,
        text=f"Total money saved: {total_money:.2f} RON\nTotal time saved: {total_time} min",
        font=("Segoe UI", 13, "bold"),
        bg=DARK_BG,
        fg=TEXT_ACCENT,
        anchor="e",
        justify="right"
    )
    totals_label.pack(side="right", padx=(0, 10))
    app.totals_label = totals_label

    btn_frame = tk.Frame(main_menu, bg=DARK_BG)
    btn_frame.pack(pady=10, side="bottom", fill="x")  # Ensure buttons are at the bottom

    has_baseline = app.get_current_baseline() is not None

    today_entry_exists = False
    if has_baseline:
        today_entry = app.find_entry_for_today(app.data.get("entries", []))
        today_entry_exists = today_entry is not None

    if has_baseline:
        log_btn_text = "Update Today's Cigarettes" if today_entry_exists else "Log Today's Cigarettes"
        app.log_btn = ttk.Button(
            btn_frame,
            text=log_btn_text,
            style="Rounded.TButton",
            command=lambda: app.show_frame("log_page")
        )
        app.log_btn.grid(row=0, column=0, padx=10, pady=8, sticky="ew")

    baseline_btn_text = "Set Initial Baseline" if not has_baseline else "Update Baseline"
    app.baseline_btn = ttk.Button(
        btn_frame,
        text=baseline_btn_text,
        style="Rounded.TButton",
        command=lambda: app.show_frame("baseline_page")
    )
    app.baseline_btn.grid(row=1, column=0, padx=10, pady=8, sticky="ew")

    ttk.Button(btn_frame, text="Analytics", style="Rounded.TButton", command=lambda: app.show_frame("analytics_page")).grid(row=2, column=0, padx=10, pady=8, sticky="ew")
    ttk.Button(btn_frame, text="Reset Data", style="Rounded.TButton", command=app.show_reset_confirmation).grid(row=3, column=0, padx=10, pady=8, sticky="ew")
    ttk.Button(btn_frame, text="Exit", style="Rounded.TButton", command=app.exit_app).grid(row=4, column=0, padx=10, pady=8, sticky="ew")
    btn_frame.grid_columnconfigure(0, weight=1)

    # Comparison frame
    comparison_frame = tk.Frame(main_menu, bg=DARK_BG)
    comparison_frame.pack(fill="x", pady=(0, 10))

    period_var = tk.StringVar(value="week")

    def update_comparison():
        stats = app.get_period_comparison(period_var.get())
        comparison_label.config(
            text=(
                f"Current: {stats['curr_cigs']} cigs, {stats['curr_money']:.2f} RON, {stats['curr_time']} min\n"
                f"Previous: {stats['prev_cigs']} cigs, {stats['prev_money']:.2f} RON, {stats['prev_time']} min\n"
                f"Change: {stats['cigs_pct']} cigs, {stats['money_pct']} RON, {stats['time_pct']} min"
            )
        )

    ttk.Radiobutton(comparison_frame, text="Week", variable=period_var, value="week", style="TRadiobutton", command=update_comparison).pack(side="left", padx=5)
    ttk.Radiobutton(comparison_frame, text="Month", variable=period_var, value="month", style="TRadiobutton", command=update_comparison).pack(side="left", padx=5)

    comparison_label = tk.Label(
        comparison_frame,
        text="",
        font=("Segoe UI", 10),
        bg=DARK_BG,
        fg=TEXT_MAIN,
        justify="left"
    )
    comparison_label.pack(side="left", padx=10)
    app.comparison_label = comparison_label

    update_comparison()

    main_menu.pack(fill="both", expand=True)

    if hasattr(app, "streak_label") and hasattr(app, "totals_label"):
        current_streak, best_streak = app.get_streaks()
        total_money, total_time = app.get_all_time_totals()
        app.streak_label.config(
            text=f"Current streak: {current_streak} days\nBest streak: {best_streak} days"
        )
        app.totals_label.config(
            text=f"Total money saved: {total_money:.2f} RON\nTotal time saved: {total_time} min"
        )