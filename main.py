import tkinter as tk
from tkinter import ttk, messagebox
from storage import write_json, read_json, migrate_json_to_db, load_data, init_db, automated_backup
from models import Baseline
from datetime import date
from tkcalendar import Calendar # type: ignore
from utils.dialogs import themed_confirm
import json
import matplotlib.pyplot as plt # type: ignore
from datetime import datetime

from pages.main_menu import create_main_menu
from pages.log_page import create_log_page
from pages.baseline_page import create_baseline_page
from pages.analytics_page import create_analytics_page

DARK_BG = "#23272e"
DARK_PANEL = "#2c313c"
DARK_ACCENT = "#4f5b66"
TEXT_MAIN = "#e0e0e0"
TEXT_ACCENT = "#ffb74d"
ERROR_COLOR = "#e57373"

JSON_PATH = "c:/nu stiu/smoking_data.json"

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("Segoe UI", 10))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class CigaretteTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        init_db()
        automated_backup()  # Backup at startup
        self.data = load_data()
        self.title("Cigarette Savings Tracker")
        self.geometry("650x750")
        self.configure(bg=DARK_BG)
        self.frames = {}
        self.set_styles()
        self.build_pages()
        self.show_frame("main_menu")

        self.header = tk.Label(self, text="Cigarette Savings Tracker", font=("Segoe UI", 18, "bold"),
                               bg=DARK_BG, fg=TEXT_ACCENT, pady=16)
        self.header.pack(side="top", fill="x")

        self.footer = tk.Label(self, text="Track your progress and save money!", font=("Segoe UI", 10),
                               bg=DARK_BG, fg=TEXT_ACCENT, pady=8)
        self.footer.pack(side="bottom", fill="x")

        ttk.Button(self.header, text="Toggle Theme", command=self.toggle_theme).pack(side="right", padx=10)

        self.protocol("WM_DELETE_WINDOW", self.exit_app)  # Use custom exit logic

    def set_styles(self):
        style = ttk.Style()
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

    def build_pages(self):
        self.show_progress(create_main_menu, self)
        self.show_progress(create_log_page, self)
        self.show_progress(create_baseline_page, self)
        self.show_progress(create_analytics_page, self)

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        if frame_name == "main_menu":
            if "main_menu" in self.frames:
                self.frames["main_menu"].destroy()
                del self.frames["main_menu"]
            self.show_progress(create_main_menu, self)
        self.frames[frame_name].pack(fill="both", expand=True, padx=20, pady=20)

    def get_current_baseline(self):
        if "baselines" in self.data and self.data["baselines"]:
            return Baseline(**self.data["baselines"][-1])
        else:
            return None

    def find_entry_for_today(self, entries):
        today = date.today().isoformat()
        for entry in entries:
            if entry["entry_date"] == today:
                return entry
        return None

    def show_progress(self, task_func, *args, **kwargs):
        progress = ttk.Progressbar(self, mode='indeterminate')
        progress.pack(pady=20)
        progress.start()
        self.update_idletasks()
        try:
            task_func(*args, **kwargs)
        finally:
            progress.stop()
            progress.destroy()

    def reset_data(self):
        if not self.data.get("baselines") and not self.data.get("entries"):
            self.show_frame("main_menu")
            self.menu_message_label.config(text="No data to reset.", fg=ERROR_COLOR)
            self.after(3000, lambda: self.menu_message_label.config(text="", fg=ERROR_COLOR))
            return
        themed_confirm(self, "Confirm Reset", "Are you sure you want to reset all data?", self.confirm_reset_yes)

    def show_reset_confirmation(self):
        self.show_frame("main_menu")
        if hasattr(self, "reset_confirm_frame") and self.reset_confirm_frame.winfo_exists():
            self.reset_confirm_frame.destroy()
        self.reset_confirm_frame = tk.Frame(self.frames["main_menu"], bg=DARK_BG, bd=2, relief="ridge")
        # Center the frame in the main window
        self.reset_confirm_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(
            self.reset_confirm_frame,
            text="Are you sure you want to reset all data?",
            font=("Segoe UI", 12, "bold"),
            bg=DARK_BG,
            fg=TEXT_ACCENT,
            pady=10,
            padx=10
        ).pack(pady=(10, 5), padx=10)
        btns = tk.Frame(self.reset_confirm_frame, bg=DARK_BG)
        btns.pack(pady=(0, 10))
        ttk.Button(btns, text="Yes", style="Rounded.TButton", command=self.confirm_reset_yes).pack(side="left", padx=8)
        ttk.Button(btns, text="No", style="Rounded.TButton", command=self.confirm_reset_no).pack(side="left", padx=8)

    def confirm_reset_yes(self):
        if hasattr(self, "reset_confirm_frame") and self.reset_confirm_frame.winfo_exists():
            self.reset_confirm_frame.destroy()
        self.show_progress(automated_backup)  # Backup before reset
        self.data = {"baselines": [], "entries": []}
        self.show_progress(write_json, self.data)
        self.show_progress(migrate_json_to_db)
        self.data = load_data()
        if hasattr(self, "reset_confirm_frame") and self.reset_confirm_frame.winfo_exists():
            self.reset_confirm_frame.destroy()
        # Destroy old frames before recreating
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()
        self.build_pages()
        self.show_frame("main_menu")
        self.menu_message_label.config(text="All data has been reset. You can start over.", fg="#81c784")
        self.after(3000, lambda: self.menu_message_label.config(text="", fg="#81c784"))

    def confirm_reset_no(self):
        if hasattr(self, "reset_confirm_frame") and self.reset_confirm_frame.winfo_exists():
            self.reset_confirm_frame.destroy()
        self.menu_message_label.config(text="Reset cancelled.", fg=TEXT_ACCENT)
        self.after(2000, lambda: self.menu_message_label.config(text="", fg=TEXT_ACCENT))

    def restore_entry_default(self, entry_widget, default_text):
        if not entry_widget.get():
            entry_widget.insert(0, default_text)

    def submit_log(self):
        baseline = self.get_current_baseline()
        if not baseline:
            self.show_frame("main_menu")
            messagebox.showinfo("Info", "Please set your baseline first.")
            return
        try:
            cigs = int(self.log_entry.get())
        except Exception:
            messagebox.showerror("Input Error", "Please enter a valid number for cigarettes smoked.")
            self.log_confirm_label.config(text="Please enter a valid number.", fg=ERROR_COLOR)
            return

        # Data validation
        if cigs < 0:
            self.log_confirm_label.config(text="Cigarettes smoked cannot be negative.", fg=ERROR_COLOR)
            return
        if cigs > 200:
            self.log_confirm_label.config(text="Cigarettes smoked seems to high.", fg=ERROR_COLOR)
            return

        try:
            # Data for today's entry
            today_entry = self.find_entry_for_today(self.data.get("entries", []))
            entry = {
                "entry_date": date.today().isoformat(),
                "cigs_smoked": cigs
            }
            cigs_saved = baseline.avg_cigs_per_day - cigs
            packs_smoked = cigs / baseline.pack_size
            money_spent = packs_smoked * baseline.pack_price
            productive_minutes_wasted = cigs * 5
            packs_saved = cigs_saved / baseline.pack_size
            money_saved = packs_saved * baseline.pack_price
            productive_minutes_saved = cigs_saved * 5
            entry["money_saved"] = round(money_saved, 2)
            entry["productive_minutes_saved"] = productive_minutes_saved

            # Write to JSON
            data = read_json()
            entries = data.setdefault("entries", [])
            # Update today's entry if exists
            for i, e in enumerate(entries):
                if e["entry_date"] == entry["entry_date"]:
                    entries[i] = entry
                    break
            else:
                entries.append(entry)
            self.show_progress(write_json, data)
            self.show_progress(migrate_json_to_db)
            self.data = load_data()

            self.log_confirm_label.config(text="Entry logged successfully!", fg="#81c784")
            baseline_money_spent = baseline.pack_price * (baseline.avg_cigs_per_day / baseline.pack_size)
            diff_money = money_spent - baseline_money_spent
            baseline_minutes_wasted = baseline.avg_cigs_per_day * 5
            diff_minutes = productive_minutes_wasted - baseline_minutes_wasted

            self.log_results_label.config(
                text=(
                    f"Money spent today: {money_spent:.2f} RON ({diff_money:+.2f} RON)\n"
                    f"Productive time wasted: {productive_minutes_wasted} minutes ({diff_minutes:+d} min)"
                ),
                fg=TEXT_ACCENT
            )
            self.after(9000, lambda: self.log_confirm_label.config(text=""))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save entry: {e}")
            self.log_confirm_label.config(text="Error saving entry.", fg=ERROR_COLOR)

    def submit_baseline(self):
        try:
            avg = int(self.avg_var.get())
            size = int(self.size_var.get())
            price_str = self.price_entry.get().replace(" RON", "")
            price = float(price_str)
        except Exception:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
            self.baseline_message_label.config(text="Please enter valid numbers.", fg=ERROR_COLOR)
            return

        # Data validation
        if avg <= 0:
            self.baseline_message_label.config(text="Average cigarettes per day must be positive.", fg=ERROR_COLOR)
            return
        if size <= 0:
            self.baseline_message_label.config(text="Pack size must be positive.", fg=ERROR_COLOR)
            return
        if price <= 0:
            self.baseline_message_label.config(text="Pack price must be positive.", fg=ERROR_COLOR)
            return
        if avg > 200:
            self.baseline_message_label.config(text="Average cigarettes per day seems to high.", fg=ERROR_COLOR)
            return
        if size > 200:
            self.baseline_message_label.config(text="Pack size seems to high.", fg=ERROR_COLOR)
            return
        if price > 1000:
            self.baseline_message_label.config(text="Pack price seems to high.", fg=ERROR_COLOR)
            return

        current_baseline = self.get_current_baseline()
        if current_baseline and (
            avg == current_baseline.avg_cigs_per_day and
            size == current_baseline.pack_size and
            abs(price - current_baseline.pack_price) < 0.01
        ):
            self.baseline_message_label.config(text="Baseline already present.", fg=ERROR_COLOR)
            return

        # Write to JSON
        try:
            data = read_json()
            data.setdefault("baselines", []).append({
                "avg_cigs_per_day": avg,
                "pack_size": size,
                "pack_price": price
            })
            self.show_progress(write_json, data)
            self.show_progress(migrate_json_to_db)
            self.data = load_data()
            self.show_frame("main_menu")
            self.menu_message_label.config(text="Baseline updated successfully!", fg="#81c784")
            self.after(3000, lambda: self.menu_message_label.config(text="", fg="#81c784"))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save baseline: {e}")
            self.baseline_message_label.config(text="Error saving baseline.", fg=ERROR_COLOR)

    def show_selected_day_analytics(self):
        selected_date = self.calendar.selection_get().isoformat()
        self.show_analytics_data(period="custom_day", custom_date=selected_date)

    def show_selected_month_analytics(self):
        selected_date = self.calendar.selection_get()
        self.show_analytics_data(period="custom_month", custom_date=selected_date)

    def show_selected_year_analytics(self):
        selected_date = self.calendar.selection_get()
        self.show_analytics_data(period="custom_year", custom_date=selected_date)

    def show_analytics_data(self, period="today", custom_date=None):
        entries = self.data.get("entries", [])
        baseline = self.get_current_baseline()
        filtered_entries = []

        if not entries:
            self.analytics_label.config(text="No entries found.", fg=ERROR_COLOR)
            return

        if period == "custom_day" and custom_date:
            filtered_entries = [e for e in entries if e["entry_date"] == custom_date]
            period_label = f"{custom_date}'s"
        elif period == "custom_month" and custom_date:
            filtered_entries = [
                e for e in entries
                if date.fromisoformat(e["entry_date"]).year == custom_date.year and
                   date.fromisoformat(e["entry_date"]).month == custom_date.month
            ]
            period_label = f"{custom_date.strftime('%B %Y')}"
        elif period == "custom_year" and custom_date:
            filtered_entries = [
                e for e in entries
                if date.fromisoformat(e["entry_date"]).year == custom_date.year
            ]
            period_label = f"{custom_date.year}"
        else:  # Default to today
            today = date.today().isoformat()
            filtered_entries = [e for e in entries if e["entry_date"] == today]
            period_label = "Today's"

        if not filtered_entries:
            self.analytics_label.config(text="No entry for selected period.", fg=ERROR_COLOR)
            return

        total_cigs = sum(e["cigs_smoked"] for e in filtered_entries)
        total_money_spent = sum((e["cigs_smoked"] / baseline.pack_size) * baseline.pack_price for e in filtered_entries) if baseline else 0
        total_time_wasted = sum(e["cigs_smoked"] * 5 for e in filtered_entries)
        avg_cigs = total_cigs / len(filtered_entries) if filtered_entries else 0

        if baseline:
            baseline_money_spent = baseline.pack_price * (baseline.avg_cigs_per_day / baseline.pack_size) * len(filtered_entries)
            diff_money = total_money_spent - baseline_money_spent
            baseline_minutes_wasted = baseline.avg_cigs_per_day * 5 * len(filtered_entries)
            diff_minutes = total_time_wasted - baseline_minutes_wasted
        else:
            diff_money = 0
            diff_minutes = 0

        msg = (
            f"{period_label} cigarettes per day: {avg_cigs:.2f}\n"
            f"Total money spent: {total_money_spent:.2f} RON ({diff_money:+.2f} RON)\n"
            f"Total productive time wasted: {total_time_wasted} minutes ({diff_minutes:+d} min)"
        )
        self.analytics_label.config(text=msg, fg=TEXT_MAIN)

    def show_trends_chart(self, trend_type="daily"):
        import matplotlib.pyplot as plt # type: ignore
        from datetime import datetime
        from collections import defaultdict

        entries = self.data.get("entries", [])
        if not entries:
            self.analytics_label.config(text="No entries to show trends.", fg="#e57373")
            return

        entries_sorted = sorted(entries, key=lambda e: e["entry_date"])
        dates = [datetime.strptime(e["entry_date"], "%Y-%m-%d") for e in entries_sorted]
        cigs = [e["cigs_smoked"] for e in entries_sorted]
        money = [e["money_saved"] for e in entries_sorted]
        minutes = [e["productive_minutes_saved"] for e in entries_sorted]

        if trend_type == "daily":
            self.iconify()
            plt.figure(figsize=(10, 5))
            plt.plot(dates, cigs, label="Cigarettes Smoked", marker="o")
            plt.plot(dates, money, label="Money Saved (RON)", marker="o")
            plt.plot(dates, minutes, label="Minutes Saved", marker="o")
            plt.xlabel("Date")
            plt.ylabel("Value")
            plt.title("Daily Trends")
            plt.legend()
            plt.tight_layout()
            plt.show()
            self.deiconify()

        elif trend_type == "weekly":
            weekly = defaultdict(lambda: {"cigs": 0, "money": 0, "minutes": 0, "count": 0})
            for e in entries_sorted:
                dt = datetime.strptime(e["entry_date"], "%Y-%m-%d")
                year_week = dt.strftime("%Y-W%U")
                weekly[year_week]["cigs"] += e["cigs_smoked"]
                weekly[year_week]["money"] += e["money_saved"]
                weekly[year_week]["minutes"] += e["productive_minutes_saved"]
                weekly[year_week]["count"] += 1
            weeks = sorted(weekly.keys())
            week_labels = weeks
            week_cigs = [weekly[w]["cigs"] / weekly[w]["count"] for w in weeks]
            week_money = [weekly[w]["money"] / weekly[w]["count"] for w in weeks]
            week_minutes = [weekly[w]["minutes"] / weekly[w]["count"] for w in weeks]

            self.iconify()
            plt.figure(figsize=(10, 5))
            plt.plot(week_labels, week_cigs, label="Avg Cigarettes Smoked", marker="o")
            plt.plot(week_labels, week_money, label="Avg Money Saved (RON)", marker="o")
            plt.plot(week_labels, week_minutes, label="Avg Minutes Saved", marker="o")
            plt.xlabel("Week")
            plt.ylabel("Average Value")
            plt.title("Weekly Trends")
            plt.legend()
            plt.tight_layout()
            plt.show()
            self.deiconify()

        elif trend_type == "monthly":
            monthly = defaultdict(lambda: {"cigs": 0, "money": 0, "minutes": 0, "count": 0})
            for e in entries_sorted:
                dt = datetime.strptime(e["entry_date"], "%Y-%m-%d")
                year_month = dt.strftime("%Y-%m")
                monthly[year_month]["cigs"] += e["cigs_smoked"]
                monthly[year_month]["money"] += e["money_saved"]
                monthly[year_month]["minutes"] += e["productive_minutes_saved"]
                monthly[year_month]["count"] += 1
            months = sorted(monthly.keys())
            month_labels = months
            month_cigs = [monthly[m]["cigs"] / monthly[m]["count"] for m in months]
            month_money = [monthly[m]["money"] / monthly[m]["count"] for m in months]
            month_minutes = [monthly[m]["minutes"] / monthly[m]["count"] for m in months]

            self.iconify()
            plt.figure(figsize=(10, 5))
            plt.plot(month_labels, month_cigs, label="Avg Cigarettes Smoked", marker="o")
            plt.plot(month_labels, month_money, label="Avg Money Saved (RON)", marker="o")
            plt.plot(month_labels, month_minutes, label="Avg Minutes Saved", marker="o")
            plt.xlabel("Month")
            plt.ylabel("Average Value")
            plt.title("Monthly Trends")
            plt.legend()
            plt.tight_layout()
            plt.show()
            self.deiconify()
    def toggle_theme(self):
        if not self.winfo_exists():
            return  # App is closed, don't update

        if self.cget("bg") == DARK_BG:
            new_bg = "#f0f0f0"
            new_fg = "#333"
            accent = "#ffb74d"
            btn_bg = "#e0e0e0"
            btn_fg = "#333"
        else:
            new_bg = DARK_BG
            new_fg = TEXT_MAIN
            accent = TEXT_ACCENT
            btn_bg = DARK_ACCENT
            btn_fg = TEXT_MAIN

        try:
            self.configure(bg=new_bg)
            if hasattr(self, "header") and self.header.winfo_exists():
                self.header.configure(bg=new_bg, fg=accent)
            if hasattr(self, "footer") and self.footer.winfo_exists():
                self.footer.configure(bg=new_bg, fg=accent)

            def update_widget_colors(widget):
                if not widget.winfo_exists():
                    return
                try:
                    if isinstance(widget, tk.Frame):
                        widget.configure(bg=new_bg)
                    elif isinstance(widget, tk.Label):
                        widget.configure(bg=new_bg, fg=new_fg)
                    elif isinstance(widget, ttk.Button):
                        style = ttk.Style()
                        style.configure("TButton", background=btn_bg, foreground=btn_fg)
                        style.configure("Rounded.TButton", background=btn_bg, foreground=btn_fg)
                    elif isinstance(widget, tk.Entry):
                        widget.configure(bg=new_bg, fg=new_fg)
                    elif isinstance(widget, Calendar):
                        widget.configure(background=new_bg, foreground=new_fg, selectbackground=accent)
                    for child in widget.winfo_children():
                        update_widget_colors(child)
                except tk.TclError:
                    pass  # Widget is destroyed

            update_widget_colors(self)

            style = ttk.Style()
            style.configure("TButton", background=btn_bg, foreground=btn_fg)
            style.configure("Rounded.TButton", background=btn_bg, foreground=btn_fg)
            style.configure("TLabel", background=new_bg, foreground=new_fg)
            style.configure("TEntry", fieldbackground=new_bg, foreground=new_fg, background=new_bg)
        except tk.TclError:
            pass  # App or widget is destroyed

    def destroy(self):
        self.show_progress(automated_backup)  # Backup at shutdown
        super().destroy()

    def exit_app(self):
        from utils.dialogs import themed_confirm
        themed_confirm(self, "Confirm Exit", "Are you sure you want to exit?", self.destroy)

    def update_entry_for_date(self, entry_date, cigs_smoked):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data["baselines"]:
            self.menu_message_label.config(text="No baseline set.", fg="#e57373")
            return

        baseline = data["baselines"][-1]
        avg_cigs = baseline["avg_cigs_per_day"]
        pack_size = baseline["pack_size"]
        pack_price = baseline["pack_price"]

        baseline_money_spent = (avg_cigs / pack_size) * pack_price
        actual_money_spent = (cigs_smoked / pack_size) * pack_price
        money_saved = round(baseline_money_spent - actual_money_spent, 2)
        productive_minutes_saved = (avg_cigs - cigs_smoked) * 5

        updated = False
        for entry in data["entries"]:
            if entry["entry_date"] == entry_date:
                entry["cigs_smoked"] = cigs_smoked
                entry["money_saved"] = money_saved
                entry["productive_minutes_saved"] = productive_minutes_saved
                entry["source"] = "manual"
                updated = True
                break

        if not updated:
            data["entries"].append({
                "entry_date": entry_date,
                "cigs_smoked": cigs_smoked,
                "money_saved": money_saved,
                "productive_minutes_saved": productive_minutes_saved,
                "source": "manual",
                "created_at": f"{entry_date} 00:00:00"
            })

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self.menu_message_label.config(text=f"Entry for {entry_date} updated!", fg="#81c784")
        self.data = data

    def show_edit_entry_dialog(self):
        import tkinter as tk
        from tkinter import ttk
        from datetime import date

        dialog = tk.Toplevel(self)
        dialog.title("Edit Previous Entry")
        dialog.configure(bg=DARK_BG)
        dialog.geometry("320x270")
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog in the parent window
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (320 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (220 // 2)
        dialog.geometry(f"+{x}+{y}")

        selected_date = self.calendar.selection_get().isoformat()
        today_str = date.today().isoformat()

        # Only allow editing previous dates
        if selected_date >= today_str:
            tk.Label(dialog, text="You can only edit previous days here.", font=("Segoe UI", 11), bg=DARK_BG, fg="#e57373").pack(pady=40)
            ttk.Button(dialog, text="Close", style="Rounded.TButton", command=dialog.destroy).pack(pady=15)
            return

        tk.Label(dialog, text="Date:", font=("Segoe UI", 11), bg=DARK_BG, fg=TEXT_ACCENT).pack(pady=(20, 5))
        date_var = tk.StringVar(value=selected_date)
        date_entry = tk.Entry(
            dialog,
            font=("Segoe UI", 11),
            bg=DARK_BG,
            fg=TEXT_ACCENT,
            textvariable=date_var,
            state="readonly",
            readonlybackground=DARK_BG
        )
        date_entry.pack(pady=5)

        tk.Label(dialog, text="Cigarettes Smoked:", font=("Segoe UI", 11), bg=DARK_BG, fg=TEXT_ACCENT).pack(pady=(10, 5))
        cigs_entry = tk.Entry(dialog, font=("Segoe UI", 11), bg=DARK_BG, fg=TEXT_MAIN)
        cigs_entry.pack(pady=5)

        error_label = tk.Label(dialog, text="", font=("Segoe UI", 10), bg=DARK_BG, fg="#e57373")
        error_label.pack()

        def save_edit():
            entry_date = date_var.get()
            try:
                cigs_smoked = int(cigs_entry.get())
                current_entry = next((e for e in self.data["entries"] if e["entry_date"] == entry_date), None)
                if current_entry and current_entry.get("cigs_smoked") == cigs_smoked:
                    error_label.config(text="Value is the same as already logged.", fg="#e57373")
                    return
                self.update_entry_for_date(entry_date, cigs_smoked)
                dialog.destroy()
                if hasattr(self, "analytics_label"):
                    self.analytics_label.config(text=f"Entry for {entry_date} updated!", fg="#81c784")
            except Exception:
                error_label.config(text="Invalid input!", fg="#e57373")

        save_btn = ttk.Button(dialog, text="Update", style="Rounded.TButton", command=save_edit)
        save_btn.pack(pady=15)

    def reset_today_entry(self):
        def do_reset():
            today_str = date.today().isoformat()
            # Remove today's entry from JSON
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            entries = data.get("entries", [])
            new_entries = [e for e in entries if e["entry_date"] != today_str]
            data["entries"] = new_entries
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            # Remove today's entry from DB
            import sqlite3
            conn = sqlite3.connect("smoking_data.db")
            c = conn.cursor()
            c.execute("DELETE FROM entries WHERE entry_date = ?", (today_str,))
            conn.commit()
            conn.close()
            self.data = data

            # Destroy and recreate the log page so it reflects the reset
            if "log_page" in self.frames:
                self.frames["log_page"].destroy()
                del self.frames["log_page"]
            self.show_progress(create_log_page, self)

            self.show_frame("main_menu")  # Go back to main menu
            self.menu_message_label.config(text="Today's entry has been reset.", fg="#81c784")
            self.after(3000, lambda: self.menu_message_label.config(text="", fg="#81c784"))

        themed_confirm(
            self,
            "Confirm Reset",
            "Are you sure you want to reset today's entry?",
            do_reset
        )

    def show_trend_selector(self):
        import tkinter as tk
        from tkinter import ttk

        dialog = tk.Toplevel(self)
        dialog.title("Select Trend Type")
        dialog.configure(bg=DARK_BG)
        dialog.geometry("300x220")
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (180 // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text="Choose trend type:", font=("Segoe UI", 12), bg=DARK_BG, fg=TEXT_ACCENT).pack(pady=(20, 10))

        def show_selected_trend(trend_type):
            dialog.destroy()
            self.show_trends_chart(trend_type)

        ttk.Button(dialog, text="Daily", style="Rounded.TButton", command=lambda: show_selected_trend("daily")).pack(pady=4)
        ttk.Button(dialog, text="Weekly", style="Rounded.TButton", command=lambda: show_selected_trend("weekly")).pack(pady=4)
        ttk.Button(dialog, text="Monthly", style="Rounded.TButton", command=lambda: show_selected_trend("monthly")).pack(pady=4)

    def show_best_worst_selector(self):
        import tkinter as tk
        from tkinter import ttk

        dialog = tk.Toplevel(self)
        dialog.title("Select Best/Worst Period")
        dialog.configure(bg=DARK_BG)
        dialog.geometry("300x220")
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (300 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (180 // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text="Choose period:", font=("Segoe UI", 12), bg=DARK_BG, fg=TEXT_ACCENT).pack(pady=(20, 10))

        def show_selected_best_worst(period):
            dialog.destroy()
            self.show_best_worst_days(period)

        ttk.Button(dialog, text="All Time", style="Rounded.TButton", command=lambda: show_selected_best_worst("all")).pack(pady=4)
        ttk.Button(dialog, text="This Month", style="Rounded.TButton", command=lambda: show_selected_best_worst("month")).pack(pady=4)
        ttk.Button(dialog, text="This Year", style="Rounded.TButton", command=lambda: show_selected_best_worst("year")).pack(pady=4)

    def show_best_worst_days(self, period="all"):
        from datetime import date

        entries = self.data.get("entries", [])
        if not entries:
            self.analytics_label.config(text="No entries to analyze.", fg="#e57373")
            return

        today = date.today()
        if period == "month":
            entries = [e for e in entries if date.fromisoformat(e["entry_date"]).year == today.year and date.fromisoformat(e["entry_date"]).month == today.month]
        elif period == "year":
            entries = [e for e in entries if date.fromisoformat(e["entry_date"]).year == today.year]

        if not entries:
            self.analytics_label.config(text="No entries for selected period.", fg="#e57373")
            return

        best_entry = min(entries, key=lambda e: e["cigs_smoked"])
        worst_entry = max(entries, key=lambda e: e["cigs_smoked"])

        msg = (
            f"Best Day: {best_entry['entry_date']} ({best_entry['cigs_smoked']} cigarettes)\n"
            f"Worst Day: {worst_entry['entry_date']} ({worst_entry['cigs_smoked']} cigarettes)"
        )
        self.analytics_label.config(text=msg, fg=TEXT_ACCENT)

    def get_streaks(self):
        entries = sorted(self.data.get("entries", []), key=lambda e: e["entry_date"])
        baseline = self.get_current_baseline()
        if not entries or not baseline:
            return 0, 0

        current_streak = 0
        best_streak = 0
        streak = 0

        for entry in entries:
            if entry["cigs_smoked"] < baseline.avg_cigs_per_day:
                streak += 1
                best_streak = max(best_streak, streak)
            else:
                streak = 0

        # Calculate current streak (from last entry backwards)
        streak = 0
        for entry in reversed(entries):
            if entry["cigs_smoked"] < baseline.avg_cigs_per_day:
                streak += 1
            else:
                break
        current_streak = streak

        return current_streak, best_streak

        if hasattr(self, "streak_label"):
            current_streak, best_streak = self.get_streaks()
            self.streak_label.config(
                text=f"Current streak: {current_streak} days\nBest streak: {best_streak} days"
            )

    def get_all_time_totals(self):
        entries = self.data.get("entries", [])
        total_money = sum(e.get("money_saved", 0) for e in entries)
        total_time = sum(e.get("productive_minutes_saved", 0) for e in entries)
        return round(total_money, 2), int(total_time)

    def get_period_comparison(self, period="week"):
        from datetime import date

        entries = self.data.get("entries", [])
        today = date.today()
        if period == "month":
            # Current month
            current_entries = [e for e in entries if date.fromisoformat(e["entry_date"]).year == today.year and date.fromisoformat(e["entry_date"]).month == today.month]
            # Previous month
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            prev_entries = [e for e in entries if date.fromisoformat(e["entry_date"]).year == prev_year and date.fromisoformat(e["entry_date"]).month == prev_month]
        else:
            # Current week
            current_week = today.isocalendar()[1]
            current_entries = [e for e in entries if date.fromisoformat(e["entry_date"]).isocalendar()[1] == current_week and date.fromisoformat(e["entry_date"]).year == today.year]
            # Previous week
            prev_week = current_week - 1 if current_week > 1 else 52
            prev_year = today.year if current_week > 1 else today.year - 1
            prev_entries = [e for e in entries if date.fromisoformat(e["entry_date"]).isocalendar()[1] == prev_week and date.fromisoformat(e["entry_date"]).year == prev_year]

        def calc_stats(entry_list):
            if not entry_list:
                return 0, 0, 0
            cigs = sum(e["cigs_smoked"] for e in entry_list)
            money = sum(e.get("money_saved", 0) for e in entry_list)
            time = sum(e.get("productive_minutes_saved", 0) for e in entry_list)
            return cigs, money, time

        curr_cigs, curr_money, curr_time = calc_stats(current_entries)
        prev_cigs, prev_money, prev_time = calc_stats(prev_entries)

        def pct_change(curr, prev):
            if prev == 0:
                return "N/A"
            change = ((curr - prev) / prev) * 100
            sign = "+" if change > 0 else ""
            return f"{sign}{change:.1f}%"

        return {
            "curr_cigs": curr_cigs,
            "curr_money": curr_money,
            "curr_time": curr_time,
            "prev_cigs": prev_cigs,
            "prev_money": prev_money,
            "prev_time": prev_time,
            "cigs_pct": pct_change(curr_cigs, prev_cigs),
            "money_pct": pct_change(curr_money, prev_money),
            "time_pct": pct_change(curr_time, prev_time)
        }

    def show_weekday_distribution(self):
        import matplotlib.pyplot as plt
        import calendar
        from datetime import datetime, date

        entries = self.data.get("entries", [])
        if not entries:
            self.analytics_label.config(text="No entries to analyze.", fg="#e57373")
            return

        # Find the date of the first entry
        first_entry_date = min(date.fromisoformat(e["entry_date"]) for e in entries)

        # Filter entries from the first entry date onward (effectively all entries)
        filtered_entries = [
            e for e in entries
            if date.fromisoformat(e["entry_date"]) >= first_entry_date
        ]

        # Prepare weekday sums and counts
        weekday_sums = [0] * 7  # Monday=0 ... Sunday=6
        weekday_counts = [0] * 7

        for e in filtered_entries:
            dt = datetime.strptime(e["entry_date"], "%Y-%m-%d")
            weekday = dt.weekday()
            weekday_sums[weekday] += e["cigs_smoked"]
            weekday_counts[weekday] += 1

        # Calculate averages
        weekday_avgs = [
            (weekday_sums[i] / weekday_counts[i]) if weekday_counts[i] > 0 else 0
            for i in range(7)
        ]

        days = [calendar.day_name[i] for i in range(7)]
        plt.figure(figsize=(7, 5))
        plt.bar(days, weekday_avgs, color="#ffb74d")
        plt.xlabel("Day of Week")
        plt.ylabel("Average Cigarettes Smoked")
        plt.title("Average Cigarettes Smoked by Day of Week\n(from first entry)")
        plt.tight_layout()
        self.iconify()
        plt.show()
        self.deiconify()

if __name__ == "__main__":
    app = CigaretteTrackerApp()
    app.mainloop()