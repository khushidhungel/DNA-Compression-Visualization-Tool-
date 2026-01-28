import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ======================================================
# ---------------- Linked List Implementation ----------
# ======================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, data):
        new_node = Node(data)
        self.size += 1
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def to_string(self):
        if not self.head:
            return ""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return "".join(result)

# ======================================================
# ---------------- Algorithm Functions -----------------
# ======================================================

def compress_dna(sequence):
    if not sequence:
        return ""
    compressed = LinkedList()
    count = 1
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            compressed.append(sequence[i - 1] + str(count))
            count = 1
    compressed.append(sequence[-1] + str(count))
    return compressed.to_string()

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
    bars = ax1.bar(labels, values, color=['#3498db', '#2ecc71'])
    ax1.set_title("Sequence Length Comparison")
    ax1.set_ylabel("Length")
    ax1.grid(True, axis="y", alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height,
                str(int(height)), ha="center", va="bottom")
    canvas1.draw_idle()

def update_frequency_graph(freq):
    ax2.clear()
    bases = list(freq.keys())
    values = list(freq.values())
    colors = ['#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
    bars = ax2.bar(bases, values, color=colors)
    ax2.set_title("DNA Base Frequency")
    ax2.set_ylabel("Count")
    ax2.grid(True, axis="y", alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height,
                str(int(height)), ha="center", va="bottom")
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
    compression_percentage = round((1 - compressed_len / original_len) * 100, 1)
    if compressed_len > original_len:
        efficiency_msg = f"⚠ NOT efficient ({abs(compression_percentage)}% increase)"
    else:
        efficiency_msg = f"✅ Efficient ({compression_percentage}% reduction)"
    info_label.config(
        text=f"Original: {original_len} | Compressed: {compressed_len} | Ratio: {ratio}\n"
             f"{efficiency_msg} | Data Structure: LINKED LIST"
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
        messagebox.showinfo("Decompressed DNA", f"{original}\n\nLength: {len(original)}")
    except:
        messagebox.showerror("Error", "Invalid compressed format.")

def load_sample():
    entry.delete(0, tk.END)
    entry.insert(0, "AAAATTTTGGGGCCCC")
    messagebox.showinfo("Sample Loaded", "High repetition sample loaded!")

def show_linkedlist_info():
    info = """🔗 LINKED LIST DATA STRUCTURE

What: Nodes connected by pointers
Each node: [data] → [next pointer]

For "AAAATTTTGGGG":
Head → [A4] → [T4] → [G4] → None

Operations:
• append() - O(n)
• to_string() - O(n)
    """
    messagebox.showinfo("Linked List Info", info)

# ======================================================
# ---------------- Navigation --------------------------
# ======================================================

def open_main_app():
    welcome.withdraw()
    build_main_window()

def go_back():
    main_window.destroy()
    welcome.deiconify()

# ======================================================
# ---------------- Main Window -------------------------
# ======================================================

def build_main_window():
    global main_window, entry, compressed_output, info_label
    global fig1, ax1, canvas1, fig2, ax2, canvas2

    main_window = tk.Toplevel(welcome)
    main_window.title("DNA Compression Tool")
    main_window.geometry("950x700")
    main_window.configure(bg="#eef5ff")

    # Header
    header = tk.Frame(main_window, bg="#1f4aa8", height=60)
    header.pack(fill="x")
    tk.Label(header, text="🧬 DNA Compression Tool (Linked List)",
            fg="white", bg="#1f4aa8",
            font=("Arial", 15, "bold")).pack(side="left", padx=20, pady=10)
    tk.Button(header, text="← Back", font=("Arial", 11, "bold"),
             bg="white", command=go_back).pack(side="right", padx=20)

    # Main Card
    card = tk.Frame(main_window, bg="white", bd=2, relief="groove")
    card.pack(padx=20, pady=20, fill="both", expand=True)

    # Input
    tk.Label(card, text="Enter DNA Sequence (A, T, C, G):",
            font=("Arial", 12, "bold"), bg="white").pack(pady=5)
    entry = tk.Entry(card, font=("Courier", 14), width=40)
    entry.pack(pady=5)

    # Sample button
    tk.Button(card, text="📋 Load Sample", bg="#f39c12", fg="white",
             font=("Arial", 9, "bold"), command=load_sample).pack(pady=3)

    # Action Buttons
    btn_frame = tk.Frame(card, bg="white")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Compress", bg="#2ecc71", fg="white",
             font=("Arial", 11, "bold"), width=12,
             command=compress_action).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Decompress", bg="#3498db", fg="white",
             font=("Arial", 11, "bold"), width=12,
             command=decompress_action).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="🔗 LL Info", bg="#9b59b6", fg="white",
             font=("Arial", 11, "bold"), width=12,
             command=show_linkedlist_info).grid(row=0, column=2, padx=10)

    # Output
    compressed_output = tk.StringVar()
    tk.Label(card, text="Compressed Output:",
            font=("Arial", 11, "bold"), bg="white").pack(pady=(10,0))
    tk.Entry(card, textvariable=compressed_output, font=("Courier", 12),
            width=50, state='readonly').pack(pady=5)

    info_label = tk.Label(card, text="", fg="#333",
                         font=("Arial", 10), bg="white")
    info_label.pack(pady=5)

    # Graphs
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
welcome.title("DNA Compression Tool")
welcome.geometry("650x500")
welcome.configure(bg="#1a1a2e")

# Title
title_frame = tk.Frame(welcome, bg="#1a1a2e")
title_frame.pack(pady=40)

tk.Label(title_frame, text="🧬 DNA COMPRESSION TOOL",
        fg="white", bg="#1a1a2e",
        font=("Arial", 26, "bold")).pack()

tk.Label(title_frame, text="Using Linked List Data Structure",
        fg="#00ff88", bg="#1a1a2e",
        font=("Arial", 13, "bold")).pack(pady=5)

# Info
info_frame = tk.Frame(welcome, bg="#1a1a2e")
info_frame.pack(pady=20)

tk.Label(info_frame, text="BICP 201 – Data Structures & Algorithms",
        fg="#aaaaaa", bg="#1a1a2e",
        font=("Arial", 12)).pack()

tk.Label(info_frame, text="Mini Project",
        fg="#aaaaaa", bg="#1a1a2e",
        font=("Arial", 12)).pack()

# Members
members_frame = tk.Frame(welcome, bg="#1a1a2e")
members_frame.pack(pady=20)

tk.Label(members_frame, text="Group Members:",
        fg="white", bg="#1a1a2e",
        font=("Arial", 11, "bold")).pack()

tk.Label(members_frame, text="Khushi Dhungel • Aska Palikhey\nGaurabi Shah • Anoma Maskey",
        fg="#cccccc", bg="#1a1a2e",
        font=("Arial", 10)).pack(pady=5)

# DSA Info
dsa_frame = tk.Frame(welcome, bg="#1a1a2e")
dsa_frame.pack(pady=20)

tk.Label(dsa_frame, text="🔗 Linked List | 🎯 RLE Algorithm | 📊 Visualization",
        fg="#ffaa00", bg="#1a1a2e",
        font=("Arial", 10, "bold")).pack()

# ENTER BUTTON - LARGE AND CLEAR
enter_btn = tk.Button(
    welcome,
    text="CLICK HERE TO ENTER",
    font=("Arial", 16, "bold"),
    bg="#00aa00",
    fg="white",
    width=25,
    height=2,
    command=open_main_app,
    cursor="hand2",
    relief="raised",
    bd=5
)
enter_btn.pack(pady=30)

# Make button interactive
def btn_hover(e):
    enter_btn['bg'] = '#00ff00'

def btn_leave(e):
    enter_btn['bg'] = '#00aa00'

enter_btn.bind("<Enter>", btn_hover)
enter_btn.bind("<Leave>", btn_leave)

welcome.mainloop()




