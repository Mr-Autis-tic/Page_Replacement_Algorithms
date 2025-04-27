import tkinter as tk
import random

# FIFO
def fifo(pages, frames):
    memory = []
    page_faults = 0
    for page in pages:
        if page not in memory:
            page_faults += 1
            if len(memory) >= frames:
                memory.pop(0)
            memory.append(page)
    return page_faults

# LRU
def lru(pages, frames):
    memory = []
    page_faults = 0
    for page in pages:
        if page not in memory:
            page_faults += 1
            if len(memory) >= frames:
                memory.pop(0)
        else:
            memory.remove(page)
        memory.append(page)
    return page_faults

# OPT
def optimal(pages, frames):
    memory = []
    page_faults = 0
    for i in range(len(pages)):
        page = pages[i]
        if page not in memory:
            page_faults += 1
            if len(memory) < frames:
                memory.append(page)
            else:
                future = pages[i + 1:]
                indexes = []
                for m in memory:
                    if m in future:
                        indexes.append(future.index(m))
                    else:
                        indexes.append(float('inf'))
                victim_index = indexes.index(max(indexes))
                memory[victim_index] = page
    return page_faults

# To Generate REference Strings
def generate_reference():
    global reference_string
    reference_string = [random.randint(0, 9) for _ in range(20)]
    reference_label.config(text=f"Page Reference: {reference_string}")

# For computing the faults
def run_simulation():
    try:
        frames = int(frames_entry.get())
        if frames <= 0:
            raise ValueError
    except ValueError:
        animate("⚠ Please enter a valid positive number of frames.", result_label)
        return
    if reference_string is None:
        animate("⚠ Please generate a page reference string first.", result_label)
        return
    fifo_faults = fifo(reference_string, frames)
    lru_faults = lru(reference_string, frames)
    opt_faults = optimal(reference_string, frames)
    result_text = (
        f"🧠 FIFO Faults: {fifo_faults}\n"
        f"📚 LRU  Faults: {lru_faults}\n"
        f"🚀 OPT  Faults: {opt_faults}"
    )
    animate(result_text, result_label)

# The following codes are for the GUI
def animate(text, label, index=0):
    if index <= len(text):
        label.config(text=text[:index])
        label.after(30, lambda: animate(text, label, index + 1))
def styled_button(master, text, command):
    btn = tk.Button(master, text=text, command=command, font=FONT_NORMAL,
                    bg=BTN_COLOR, fg="white", activebackground=BTN_HOVER,
                    activeforeground="white", bd=0, padx=15, pady=5, cursor="hand2")
    return btn
reference_string = [random.randint(0, 9) for _ in range(20)]
root = tk.Tk()
root.title("Page Replacement Simulator")
root.geometry("650x430")
root.configure(bg="#1e1e1e")
FONT_HEADER = ("Segoe UI", 20, "bold")
FONT_NORMAL = ("Segoe UI", 12)
FONT_RESULT = ("Consolas", 13)
FG_PRIMARY = "#f0f0f0"
FG_SECONDARY = "#a9a9a9"
BG_DARK = "#1e1e1e"
BG_ACCENT = "#333"
BTN_COLOR = "#3a7bd5"
BTN_HOVER = "#2b5fa2"
tk.Label(root, text="Page Replacement Simulator", font=FONT_HEADER, bg=BG_DARK, fg=FG_PRIMARY).pack(pady=15)
frame_input = tk.Frame(root, bg=BG_DARK)
frame_input.pack(pady=10)
tk.Label(frame_input, text="Number of Frames:", font=FONT_NORMAL, bg=BG_DARK, fg=FG_SECONDARY).pack(side=tk.LEFT, padx=5)
frames_entry = tk.Entry(frame_input, width=5, font=FONT_NORMAL, bg=BG_ACCENT, fg=FG_PRIMARY, insertbackground="white", justify="center", bd=0)
frames_entry.pack(side=tk.LEFT, padx=5)
styled_button(frame_input, "🎲 Generate String", generate_reference).pack(side=tk.LEFT, padx=10)
reference_label = tk.Label(root, text=f"Page Reference: {reference_string}", font=FONT_NORMAL, bg=BG_DARK, fg=FG_PRIMARY)
reference_label.pack(pady=10)
styled_button(root, "▶ Run Simulation", run_simulation).pack(pady=10)
result_label = tk.Label(root, text="", font=FONT_RESULT, bg=BG_DARK, fg=FG_PRIMARY, justify="left", anchor="w")
result_label.pack(pady=15)
root.mainloop()