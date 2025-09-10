import tkinter as tk

def themed_confirm(app, title, message, on_confirm, auto_confirm=False):
    if auto_confirm:
        on_confirm()
        return

    dialog = tk.Toplevel(app)
    dialog.title(title)
    dialog.configure(bg=app["bg"] if hasattr(app, "bg") else "#23272e")
    dialog.transient(app)
    dialog.grab_set()

    # Set dialog size (wider for longer messages)
    width, height = 400, 160
    dialog.geometry(f"{width}x{height}")

    # Center the dialog in the parent window
    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - (width // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (height // 2)
    dialog.geometry(f"+{x}+{y}")

    label = tk.Label(
        dialog,
        text=message,
        font=("Segoe UI", 12),
        bg=app["bg"] if hasattr(app, "bg") else "#23272e",
        fg="#ffb74d",
        wraplength=360,  # Wrap text at 360 pixels
        justify="center"
    )
    label.pack(pady=(30, 10), padx=20)

    btn_frame = tk.Frame(dialog, bg=app["bg"] if hasattr(app, "bg") else "#23272e")
    btn_frame.pack(pady=10)

    def confirm():
        dialog.destroy()
        on_confirm()

    def cancel():
        dialog.destroy()

    tk.Button(btn_frame, text="Yes", font=("Segoe UI", 11), bg="#ffb74d", fg="#23272e", width=8, command=confirm).pack(side="left", padx=10)
    tk.Button(btn_frame, text="No", font=("Segoe UI", 11), bg="#23272e", fg="#ffb74d", width=8, command=cancel).pack(side="left", padx=10)