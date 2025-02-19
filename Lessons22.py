import tkinter as tk

def calculate():
    try:
        result.set(float(entry1.get()) - float(entry2.get()))
    except ValueError:
        result.set("Ошибка")

def toggle_theme():
    theme = dark_theme if root.cget("bg") == "#f0f0f0" else light_theme
    for widget, styles in theme.items():
        widget.configure(**styles)

root = tk.Tk()
root.title("Калькулятор (-)")
root.geometry("250x250")
root.configure(bg="#f0f0f0")

entry1 = tk.Entry(root, font=("Arial", 12))
entry2 = tk.Entry(root, font=("Arial", 12))
calculate_button = tk.Button(root, text="Вычислить", command=calculate, font=("Arial", 12))
result = tk.StringVar()
result_label = tk.Label(root, textvariable=result, font=("Arial", 14, "bold"))
theme_button = tk.Button(root, text="Темная тема", command=toggle_theme, font=("Arial", 10))

light_theme = {
    root: {"bg": "#f0f0f0"},
    entry1: {"bg": "#ffffff", "fg": "#000000"},
    entry2: {"bg": "#ffffff", "fg": "#000000"},
    calculate_button: {"bg": "#4CAF50", "fg": "#ffffff"},
    result_label: {"bg": "#f0f0f0", "fg": "#333333"},
    theme_button: {"bg": "#4CAF50", "fg": "#ffffff", "text": "Темная тема"}
}

dark_theme = {
    root: {"bg": "#2d2d2d"},
    entry1: {"bg": "#444444", "fg": "#ffffff"},
    entry2: {"bg": "#444444", "fg": "#ffffff"},
    calculate_button: {"bg": "#555555", "fg": "#ffffff"},
    result_label: {"bg": "#2d2d2d", "fg": "#ffffff"},
    theme_button: {"bg": "#555555", "fg": "#ffffff", "text": "Светлая тема"}
}

for widget in (entry1, entry2, calculate_button, result_label, theme_button):
    widget.pack(pady=10)

root.mainloop()