import tkinter as tk
from tkinter import ttk

DARK_BG = "#23272e"
TEXT_MAIN = "#e0e0e0"
TEXT_ACCENT = "#ffb74d"
ERROR_COLOR = "#e57373"

def create_baseline_page(app):
    baseline_page = tk.Frame(app, bg=DARK_BG)
    app.frames["baseline_page"] = baseline_page

    tk.Label(baseline_page, text="Update Baseline", font=("Segoe UI", 15, "bold"), bg=DARK_BG, fg=TEXT_ACCENT).pack(pady=(20, 10))
    app.avg_var = tk.IntVar()
    app.size_var = tk.IntVar()
    app.price_var = tk.DoubleVar()

    current_baseline = app.get_current_baseline()
    avg_default = str(current_baseline.avg_cigs_per_day) if current_baseline else "0"
    size_default = str(current_baseline.pack_size) if current_baseline else "0"
    price_default = f"{current_baseline.pack_price:.2f} RON" if current_baseline else "0.00 RON"

    ttk.Label(baseline_page, text="Average cigarettes per day:", background=DARK_BG, foreground=TEXT_MAIN).pack(pady=4)
    avg_frame = tk.Frame(baseline_page, bg=DARK_BG)
    avg_frame.pack(pady=4)
    avg_entry = ttk.Entry(avg_frame, textvariable=app.avg_var, font=("Segoe UI", 12), width=4)
    avg_entry.grid(row=0, column=1, padx=0)
    avg_entry.delete(0, tk.END)
    avg_entry.insert(0, avg_default)
    avg_entry.bind("<FocusIn>", lambda e: avg_entry.delete(0, tk.END))
    avg_entry.bind("<FocusOut>", lambda e: app.restore_entry_default(avg_entry, avg_default))
    ttk.Button(avg_frame, text="-", width=4, style="Rounded.TButton",
               command=lambda: app.avg_var.set(max(0, app.avg_var.get()-1))
    ).grid(row=0, column=0, padx=(0,2), ipady=1)
    ttk.Button(avg_frame, text="+", width=4, style="Rounded.TButton",
               command=lambda: app.avg_var.set(app.avg_var.get()+1)
    ).grid(row=0, column=2, padx=(2,0), ipady=1)

    ttk.Label(baseline_page, text="Number of cigarettes in a pack:", background=DARK_BG, foreground=TEXT_MAIN).pack(pady=4)
    size_frame = tk.Frame(baseline_page, bg=DARK_BG)
    size_frame.pack(pady=4)
    size_entry = ttk.Entry(size_frame, textvariable=app.size_var, font=("Segoe UI", 12), width=4)
    size_entry.grid(row=0, column=1, padx=0)
    size_entry.delete(0, tk.END)
    size_entry.insert(0, size_default)
    size_entry.bind("<FocusIn>", lambda e: size_entry.delete(0, tk.END))
    size_entry.bind("<FocusOut>", lambda e: app.restore_entry_default(size_entry, size_default))
    ttk.Button(size_frame, text="-", width=4, style="Rounded.TButton",
               command=lambda: app.size_var.set(max(0, app.size_var.get()-1))
    ).grid(row=0, column=0, padx=(0,2), ipady=1)
    ttk.Button(size_frame, text="+", width=4, style="Rounded.TButton",
               command=lambda: app.size_var.set(app.size_var.get()+1)
    ).grid(row=0, column=2, padx=(2,0), ipady=1)

    ttk.Label(baseline_page, text="Price of a pack:", background=DARK_BG, foreground=TEXT_MAIN).pack(pady=4)
    price_frame = tk.Frame(baseline_page, bg=DARK_BG)
    price_frame.pack(pady=4)
    price_entry = ttk.Entry(price_frame, font=("Segoe UI", 12), width=4)
    price_entry.grid(row=0, column=1, padx=0)
    price_entry.delete(0, tk.END)
    price_entry.insert(0, price_default)

    def price_focus_in(event):
        val = price_entry.get().replace(" RON", "")
        if val == price_default.replace(" RON", ""):
            val = ""
        price_entry.delete(0, tk.END)
        price_entry.insert(0, val)

    def price_focus_out(event):
        val = price_entry.get()
        if not val.endswith("RON"):
            price_entry.delete(0, tk.END)
            price_entry.insert(0, f"{val} RON" if val else price_default)

    price_entry.bind("<FocusIn>", price_focus_in)
    price_entry.bind("<FocusOut>", price_focus_out)

    def price_minus():
        try:
            val = float(price_entry.get().replace(" RON", ""))
        except Exception:
            val = 0.0
        val = max(0, val - 0.5)
        price_entry.delete(0, tk.END)
        price_entry.insert(0, f"{val:.2f}")
        price_focus_out(None)

    def price_plus():
        try:
            val = float(price_entry.get().replace(" RON", ""))
        except Exception:
            val = 0.0
        val += 0.5
        price_entry.delete(0, tk.END)
        price_entry.insert(0, f"{val:.2f}")
        price_focus_out(None)

    ttk.Button(price_frame, text="-", width=4, style="Rounded.TButton",
               command=price_minus
    ).grid(row=0, column=0, padx=(0,2), ipady=1)
    ttk.Button(price_frame, text="+", width=4, style="Rounded.TButton",
               command=price_plus
    ).grid(row=0, column=2, padx=(2,0), ipady=1)

    app.price_entry = price_entry

    app.baseline_message_label = tk.Label(baseline_page, text="", font=("Segoe UI", 11), bg=DARK_BG)
    app.baseline_message_label.pack(pady=(4, 4))

    ttk.Button(baseline_page, text="Submit", style="Rounded.TButton", command=app.submit_baseline).pack(pady=8)
    ttk.Button(baseline_page, text="Back", style="Rounded.TButton", command=lambda: app.show_frame("main_menu")).pack(pady=8)