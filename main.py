import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ======================================================
# ---------------- Algorithm Functions -----------------
# ======================================================

def compress_dna(sequence):
    if not sequence:
        return ""

    compressed = []
    count = 1

    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            compressed.append(sequence[i - 1] + str(count))
            count = 1

    compressed.append(sequence[-1] + str(count))
    return "".join(compressed)


def decompress_dna(sequence):
    decompressed = ""
    number = ""
    prev_char = ""

    for char in sequence:
        if char.isdigit():
            number += char
        else:
            if number:
                decompressed += prev_char * int(number)
            prev_char = char
            number = ""

    if number:
        decompressed += prev_char * int(number)

    return decompressed


def is_valid_dna(sequence):
    for ch in sequence:
        if ch not in ["A", "T", "C", "G"]:
            return False
    return True


def base_frequency(sequence):
    freq = {"A": 0, "T": 0, "C": 0, "G": 0}
    for base in sequence:
        freq[base] += 1
    return freq

# ======================================================
# ---------------- Graph Functions ---------------------
# ======================================================

def update_length_graph(original_len, compressed_len):
    ax1.clear()

    labels = ["Original", "Compressed"]
    values = [original_len, compressed_len]

    bars = ax1.bar(labels, values)

    ax1.set_title("Sequence Length Comparison")
    ax1.set_ylabel("Length")
    ax1.grid(True, axis="y", alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(height),
            ha="center",
            va="bottom"
        )

    canvas1.draw_idle()


def update_frequency_graph(freq):
    ax2.clear()

    bases = list(freq.keys())
    values = list(freq.values())

    bars = ax2.bar(bases, values)

    ax2.set_title("DNA Base Frequency")
    ax2.set_ylabel("Count")
    ax2.grid(True, axis="y", alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(height),
            ha="center",
            va="bottom"
        )

    canvas2.draw_idle()

# ======================================================
# ---------------- Button Actions ----------------------
# ======================================================

def compress_action():
    dna = entry.get().upper().replace(" ", "")

    if not dna:
        messagebox.showerror("Error", "Please enter DNA sequence.")
        return

    if not is_valid_dna(dna):
        messagebox.showerror("Invalid Input", "Only A, T, C, G allowed.")
        return

    compressed = compress_dna(dna)
    compressed_output.set(compressed)

    original_len = len(dna)
    compressed_len = len(compressed)
    ratio = round(compressed_len / original_len, 2)

    if compressed_len > original_len:
        efficiency_msg = "⚠ Compression NOT efficient (low repetition)"
    else:
        efficiency_msg = "✅ Compression efficient"

    info_label.config(
        text=f"Original Length: {original_len} | "
             f"Compressed Length: {compressed_len} | "
             f"Compression Ratio: {ratio}\n"
             f"{efficiency_msg}"
    )

    freq = base_frequency(dna)
    update_length_graph(original_len, compressed_len)
    update_frequency_graph(freq)


def decompress_action():
    compressed = compressed_output.get()

    if not compressed:
        messagebox.showerror("Error", "No compressed sequence found.")
        return

    try:
        original = decompress_dna(compressed)
        messagebox.showinfo("Decompressed DNA", original)
    except:
        messagebox.showerror("Error", "Invalid compressed format.")
# Add a "Sample DNA" button to auto-fill example sequences
def load_sample():
    samples = [
        "AAAATTTTGGGGCCCC",  # High repetition
        "ATCGATCGATCG",      # Low repetition
        "AAAAAAAAATTTTTGGGGGGCCCCCC"  # Very high repetition
    ]
    entry.delete(0, tk.END)
    entry.insert(0, samples[0])
# ======================================================
# ---------------- Window Navigation -------------------
# ======================================================

def open_main_app():
    welcome.withdraw()
    build_main_window()


def go_back():
    window.destroy()
    welcome.deiconify()

# ======================================================
# ---------------- Main App Window ---------------------
# ======================================================

def build_main_window():
    global window, entry, compressed_output, info_label
    global fig1, ax1, canvas1, fig2, ax2, canvas2

    window = tk.Toplevel()
    window.title("🧬 DNA Compression Tool")
    window.geometry("900x650")
    window.configure(bg="#eef5ff")

    # Header
    header = tk.Frame(window, bg="#1f4aa8", height=60)
    header.pack(fill="x")

    tk.Label(
        header,
        text="🧬 DNA Compression & Visualization Tool",
        fg="white",
        bg="#1f4aa8",
        font=("Segoe UI", 16, "bold")
    ).pack(side="left", padx=20)

    tk.Button(
        header,
        text="⬅ Back",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        command=go_back
    ).pack(side="right", padx=20)

    # Main Card
    card = tk.Frame(window, bg="white", bd=2, relief="groove")
    card.pack(padx=20, pady=20, fill="both", expand=True)

    # Input
    tk.Label(card, text="Enter DNA Sequence (A, T, C, G):",
             font=("Segoe UI", 12), bg="white").pack(pady=5)

    entry = tk.Entry(card, font=("Consolas", 14), width=40)
    entry.pack(pady=5)

    # Buttons
    btn_frame = tk.Frame(card, bg="white")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Compress", bg="#2ecc71",
              font=("Segoe UI", 11, "bold"),
              width=12, command=compress_action).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="Decompress", bg="#3498db",
              font=("Segoe UI", 11, "bold"),
              width=12, command=decompress_action).grid(row=0, column=1, padx=10)

    # Output
    compressed_output = tk.StringVar()
    tk.Label(card, text="Compressed Output:",
             font=("Segoe UI", 11), bg="white").pack()

    tk.Entry(card, textvariable=compressed_output,
             font=("Consolas", 12), width=50).pack(pady=5)

    info_label = tk.Label(card, text="", fg="#333",
                          font=("Segoe UI", 10), bg="white")
    info_label.pack(pady=5)

    # Graph Area
    graph_frame = tk.Frame(card, bg="white")
    graph_frame.pack(pady=10)

    fig1, ax1 = plt.subplots(figsize=(4, 3), dpi=100)
    fig1.patch.set_facecolor("white")
    canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=0, column=0, padx=15)

    fig2, ax2 = plt.subplots(figsize=(4, 3), dpi=100)
    fig2.patch.set_facecolor("white")
    canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=1, padx=15)

# ======================================================
# ---------------- Welcome Window ----------------------
# ======================================================

welcome = tk.Tk()
welcome.title("Mini Project Launcher")
welcome.geometry("700x450")
welcome.configure(bg="#0f172a")

card = tk.Frame(welcome, bg="#111827", bd=2, relief="ridge")
card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=320)

tk.Label(card, text="🧬 DNA Compression Tool",
         fg="white", bg="#111827",
         font=("Segoe UI", 24, "bold")).pack(pady=20)

tk.Label(card, text="BICP 201 – Data Structures & Algorithms\nMini Project",
         fg="#cbd5e1", bg="#111827",
         font=("Segoe UI", 12)).pack()

tk.Label(card, text="Group Members:\nKhushi Dhungel\naska palikhey and gaurabi shah\nanoma maskey",
         fg="#e5e7eb", bg="#111827",
         font=("Segoe UI", 11)).pack(pady=20)

tk.Button(card, text="✨ enter ",
          font=("Segoe UI", 13, "bold"),
          bg="#2563eb", fg="white",
          width=20, command=open_main_app).pack(pady=15)

welcome.mainloop()




