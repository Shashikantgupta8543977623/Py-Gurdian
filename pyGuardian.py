
# PyGuardian - Python Based Password Manager & Phishing Link Checker
# B.Tech IT 2nd Year - BSSITM
# Run: python pyguardian.py

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3, random, string, re, hashlib, urllib.parse

DB = "pyguardian.db"

# ---------- Security ----------
def encrypt(text, key="pyguardian"):
    # Simple demo encryption (XOR + hex) - presentation ke liye
    # Real project me cryptography library use kar sakte ho
    out = []
    for i, ch in enumerate(text):
        out.append(chr(ord(ch) ^ ord(key[i % len(key)])))
    return "".join(out).encode("utf-8").hex()

def decrypt(hex_text, key="pyguardian"):
    try:
        text = bytes.fromhex(hex_text).decode("utf-8")
        out = []
        for i, ch in enumerate(text):
            out.append(chr(ord(ch) ^ ord(key[i % len(key)])))
        return "".join(out)
    except:
        return "[Decrypt Error]"

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ---------- Database ----------
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY AUTOINCREMENT, site TEXT, username TEXT, password TEXT)")
conn.commit()

# ---------- Phishing Checker (ML Logic - Rule Based Demo) ----------
def check_url(url):
    url = url.strip().lower()
    score = 0
    reasons = []
    if not url.startswith("http"):
        url = "http://" + url
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc

    if parsed.scheme == "http":
        score += 2; reasons.append("HTTPS nahi hai, sirf HTTP hai")
    if len(url) > 75:
        score += 2; reasons.append("URL bahut lamba hai")
    if url.count(".") > 4:
        score += 2; reasons.append("URL me bahut zyada dot (.) hain")
    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        score += 3; reasons.append("IP address se link bana hai")
    for word in ["free", "offer", "win", "lottery", "verify", "login", "urgent", "reward"]:
        if word in url:
            score += 1; reasons.append(f"Suspicious word mila: {word}")
    if "@" in url or "-" in domain:
        score += 1; reasons.append("URL me @ ya - suspicious hai")

    if score >= 5:
        return "DANGER - Phishing Link!", "red", reasons
    elif score >= 2:
        return "SUSPICIOUS - Dhyan se kholo", "orange", reasons
    else:
        return "SAFE - Link Safe hai", "green", reasons

# ---------- GUI ----------
root = tk.Tk()
root.title("PyGuardian - Password Manager & Phishing Checker")
root.geometry("620x650")
root.configure(bg="#208DDB")

tk.Label(root, text="PyGuardian", font=("Arial", 24, "bold"), bg="#f2f2f2", fg="#4a148c").pack(pady=10)
tk.Label(root, text="Python Based Password Manager & Phishing Link Checker", bg="#f2f2f2").pack()

# --- Password Generator ---
frame1 = tk.LabelFrame(root, text="1. Password Generator", padx=10, pady=10, bg="white")
frame1.pack(fill="x", padx=15, pady=10)
pass_var = tk.StringVar()
tk.Entry(frame1, textvariable=pass_var, font=("Arial", 12), width=35).pack(side="left", padx=5)

def gen_pass():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = "".join(random.choice(chars) for _ in range(12))
    pass_var.set(pwd)
    strength_label.config(text="Strength: STRONG", fg="green")

tk.Button(frame1, text="Generate", command=gen_pass, bg="#4a148c", fg="white").pack(side="left", padx=5)
strength_label = tk.Label(frame1, text="Strength: -", bg="white")
strength_label.pack(side="left")

# --- Save to Vault ---
frame2 = tk.LabelFrame(root, text="2. Save Password in Encrypted Vault (SQLite)", padx=10, pady=10, bg="white")
frame2.pack(fill="x", padx=15, pady=5)
tk.Label(frame2, text="Site:", bg="white").grid(row=0, column=0, sticky="w")
site_var = tk.StringVar(); tk.Entry(frame2, textvariable=site_var, width=30).grid(row=0, column=1, padx=5, pady=3)
tk.Label(frame2, text="Username:", bg="white").grid(row=1, column=0, sticky="w")
user_var = tk.StringVar(); tk.Entry(frame2, textvariable=user_var, width=30).grid(row=1, column=1, padx=5, pady=3)

def save_pass():
    site, user, pwd = site_var.get(), user_var.get(), pass_var.get()
    if not site or not user or not pwd:
        messagebox.showwarning("Missing", "Site, Username aur Password bharo!")
        return
    enc = encrypt(pwd)
    cur.execute("INSERT INTO vault (site, username, password) VALUES (?,?,?)", (site, user, enc))
    conn.commit()
    messagebox.showinfo("Saved", f"{site} ka password Encrypted Vault me save ho gaya!")
    show_vault()

#tk.Button(frame2, text="Save in Vault", command=save_pass, bg="green", fg="white").pack(pady=5)

# --- Vault View ---
frame3 = tk.LabelFrame(root, text="3. Saved Vault", padx=10, pady=10, bg="white")
frame3.pack(fill="x", padx=15, pady=5)
vault_list = tk.Listbox(frame3, width=75, height=5)
vault_list.pack()
def show_vault():
    vault_list.delete(0, tk.END)
    cur.execute("SELECT site, username, password FROM vault")
    for site, user, enc in cur.fetchall():
        vault_list.insert(tk.END, f"{site} | {user} | {decrypt(enc)} (Encrypted Saved)")
tk.Button(frame3, text="Show Vault", command=show_vault).pack(pady=3)

# --- Phishing Checker ---
frame4 = tk.LabelFrame(root, text="4. Phishing Link Checker", padx=10, pady=10, bg="white")
frame4.pack(fill="x", padx=15, pady=5)
url_var = tk.StringVar()
tk.Entry(frame4, textvariable=url_var, width=50).pack(pady=5)
result_label = tk.Label(frame4, text="Result is here", bg="white", font=("Arial", 11, "bold"))
result_label.pack()
def check_now():
    result, color, reasons = check_url(url_var.get())
    result_label.config(text=result, fg=color)
    if reasons:
        messagebox.showinfo("Kyu?", "\n".join(["- " + r for r in reasons]))
    else:
        messagebox.showinfo("Safe", "Koi suspicious cheez nahi mili.")
tk.Button(frame4, text="Check Link", command=check_now, bg="#d32f2f", fg="white").pack()

tk.Label(root, text="B.Tech IT 2nd Year | BSSITM | Python + Tkinter + SQLite + ML", bg="#f2f2f2", fg="grey").pack(pady=10)
root.mainloop()