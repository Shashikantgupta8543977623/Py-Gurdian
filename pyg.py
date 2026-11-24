# ==========================================================
# PyGuardian - Python Based Password Manager & Phishing Checker
# B.Tech IT 2nd Year | BSSITM
# Prototype - 100% Python
# Chalane ke liye: python pyguardian_prototype.py
# ==========================================================

import tkinter as tk
from tkinter import messagebox
import sqlite3, random, string, re, urllib.parse

# ---------- 1. DATABASE - SQLite ----------
conn = sqlite3.connect("pyguardian.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS vault (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT,
    username TEXT,
    password TEXT
)
""")
conn.commit()

# ---------- 2. ENCRYPTION - Simple Demo ----------
# Real me cryptography library use hoti hai, yahan samajhne ke liye simple XOR use kiya hai
def encrypt(text):
    key = "pyguardian"
    out = ""
    for i, ch in enumerate(text):
        out += chr(ord(ch) ^ ord(key[i % len(key)]))
    return out.encode("utf-8").hex()

def decrypt(hex_text):
    try:
        key = "pyguardian"
        text = bytes.fromhex(hex_text).decode("utf-8")
        out = ""
        for i, ch in enumerate(text):
            out += chr(ord(ch) ^ ord(key[i % len(key)]))
        return out
    except:
        return "[Error]"

# ---------- 3. PHISHING CHECKER - ML Logic ----------
def check_url(url):
    url = url.strip().lower()
    if not url:
        return "Pehle link daalo!", "black", []
    if not url.startswith("http"):
        url = "http://" + url

    score = 0
    reasons = []
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc

    # Rule 1: https nahi hai
    if parsed.scheme == "http":
        score += 2; reasons.append("HTTPS nahi hai, sirf HTTP hai")
    # Rule 2: URL bahut lamba
    if len(url) > 75:
        score += 2; reasons.append("URL bahut lamba hai")
    # Rule 3: Bahut zyada dot
    if url.count(".") > 4:
        score += 2; reasons.append("URL me bahut zyada dot (.) hain")
    # Rule 4: IP address se bana hai
    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        score += 3; reasons.append("IP address se link bana hai")
    # Rule 5: Suspicious words
    for word in ["free", "offer", "win", "lottery", "verify", "login", "urgent", "reward", "gift"]:
        if word in url:
            score += 1; reasons.append(f"Suspicious word mila: {word}")
    # Rule 6: @ ya - hai
    if "@" in url:
        score += 1; reasons.append("URL me @ hai, ye phishing ka sign hai")

    if score >= 5:
        return "DANGER - Phishing Link!", "red", reasons
    elif score >= 2:
        return "SUSPICIOUS - Dhyan se kholo", "orange", reasons
    else:
        return "SAFE - Link Safe hai", "green", reasons

# ---------- 4. GUI - Tkinter ----------
root = tk.Tk()
root.title("PyGuardian - Password Manager & Phishing Checker")
root.geometry("620x680")
root.configure(bg="#f5f3ff")

tk.Label(root, text="PyGuardian", font=("Arial", 26, "bold"), bg="#f5f3ff", fg="#6C4CF1").pack(pady=8)
tk.Label(root, text="Python Based Password Manager & Phishing Link Checker", bg="#f5f3ff", fg="#333").pack()

# --- Section 1: Password Generator ---
f1 = tk.LabelFrame(root, text="1. Password Generator", padx=10, pady=10, bg="white", font=("Arial", 10, "bold"))
f1.pack(fill="x", padx=15, pady=8)
pass_var = tk.StringVar()
tk.Entry(f1, textvariable=pass_var, font=("Arial", 12), width=32).pack(side="left", padx=5)
strength_label = tk.Label(f1, text="Strength: -", bg="white", font=("Arial", 10, "bold"))
strength_label.pack(side="left", padx=5)

def gen_pass():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = "".join(random.choice(chars) for _ in range(12))
    pass_var.set(pwd)
    strength_label.config(text="Strength: STRONG", fg="green")

tk.Button(f1, text="Generate", command=gen_pass, bg="#6C4CF1", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

# --- Section 2: Save in Vault ---
f2 = tk.LabelFrame(root, text="2. Save in Encrypted Vault (SQLite)", padx=10, pady=10, bg="white", font=("Arial", 10, "bold"))
f2.pack(fill="x", padx=15, pady=5)
tk.Label(f2, text="Site:", bg="white").grid(row=0, column=0, sticky="w")
site_var = tk.StringVar(); tk.Entry(f2, textvariable=site_var, width=32).grid(row=0, column=1, padx=5, pady=3)
tk.Label(f2, text="Username:", bg="white").grid(row=1, column=0, sticky="w")
user_var = tk.StringVar(); tk.Entry(f2, textvariable=user_var, width=32).grid(row=1, column=1, padx=5, pady=3)

def save_pass():
    site, user, pwd = site_var.get().strip(), user_var.get().strip(), pass_var.get().strip()
    if not site or not user or not pwd:
        messagebox.showwarning("Missing", "Site, Username aur Password bharo!")
        return
    enc = encrypt(pwd)
    cur.execute("INSERT INTO vault (site, username, password) VALUES (?,?,?)", (site, user, enc))
    conn.commit()
    messagebox.showinfo("Saved", f"{site} ka password Encrypted Vault me save ho gaya!")
    show_vault()

tk.Button(f2, text="Save in Vault", command=save_pass, bg="#00C9A7", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

# --- Section 3: Vault ---
f3 = tk.LabelFrame(root, text="3. Saved Vault", padx=10, pady=10, bg="white", font=("Arial", 10, "bold"))
f3.pack(fill="x", padx=15, pady=5)
vault_list = tk.Listbox(f3, width=75, height=5)
vault_list.pack()
def show_vault():
    vault_list.delete(0, tk.END)
    cur.execute("SELECT site, username, password FROM vault")
    rows = cur.fetchall()
    if not rows:
        vault_list.insert(tk.END, "Abhi koi password save nahi hai...")
    for site, user, enc in rows:
        vault_list.insert(tk.END, f"{site} | {user} | {decrypt(enc)}  (Encrypted Saved)")
tk.Button(f3, text="Show Vault", command=show_vault, bg="#333", fg="white").pack(pady=3)

# --- Section 4: Phishing Checker ---
f4 = tk.LabelFrame(root, text="4. Phishing Link Checker", padx=10, pady=10, bg="white", font=("Arial", 10, "bold"))
f4.pack(fill="x", padx=15, pady=5)
url_var = tk.StringVar()
tk.Entry(f4, textvariable=url_var, width=52).pack(pady=5)
result_label = tk.Label(f4, text="Result yahan aayega", bg="white", font=("Arial", 11, "bold"))
result_label.pack()
def check_now():
    result, color, reasons = check_url(url_var.get())
    result_label.config(text=result, fg=color)
    if reasons:
        messagebox.showinfo("Kyu?", "\n".join(["- " + r for r in reasons]))
    elif "SAFE" in result:
        messagebox.showinfo("Safe", "Koi suspicious cheez nahi mili.")
tk.Button(f4, text="Check Link", command=check_now, bg="#D32F2F", fg="white", font=("Arial", 10, "bold")).pack()

tk.Label(root, text="B.Tech IT 2nd Year | BSSITM | Python + Tkinter + SQLite + ML", bg="#f5f3ff", fg="grey").pack(pady=10)
root.mainloop()