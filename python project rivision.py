import tkinter as tk

root= tk.Tk()
root.title("TecZure Rivision")
root.geometry("1200x700")

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()




heading1=tk.Frame(root,bg="light blue",width="1150",height="650")
heading1.pack(pady=10)

heading2=tk.Frame(root,bg="light yellow",width="1150",height="250")
heading2.pack(pady=20)

root.mainloop()