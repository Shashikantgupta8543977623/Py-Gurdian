import tkinter as tk

root=tk.Tk()
root.title("TecZure")
root.geometry("1100x700")

mf=tk.Frame(background="black",width=1100,height=700)
mf.pack(pady=10)

lable1=tk.Label(root,text="Welcome")

mf2=tk.Frame(background="blue",width=1020,height=200)
mf2.place(x=300,y=10)

mf3=tk.Frame(background="gray",width=300,height=700)
mf3.place(x=0,y=10)

f1=tk.Frame(background="blue",width=480,height=250)
f1.place(x=310,y=220)



mf4=tk.Frame(background="white",width=300,height=230)
mf4.place(x=350,y=230)

f2=tk.Frame(background="blue",width=480,height=250)
f2.place(x=830,y=220)

mf5=tk.Frame(background="white",width=430,height=230)
mf5.place(x=870,y=230)

f3=tk.Frame(background="blue",width=480,height=230)
f3.place(x=310,y=480)


mf6=tk.Frame(background="white",width=300,height=200)
mf6.place(x=350,y=500)

f4=tk.Frame(background="blue",width=480,height=230)
f4.place(x=830,y=480)


mf7=tk.Frame(background="white",width=430,height=200)
mf7.place(x=870,y=500)




root.mainloop()