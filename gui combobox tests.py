import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("Combobox Example")
window.geometry("600x600")

# Create a combobox
vals = ["Genre", "Year Released", "Length"]
combo = ttk.Combobox(window, values=vals)
combo.current(0)  # Set the default selection
combo.pack() #<- add to window

# create label
text_var = tk.StringVar()
text_var.set("Please make a selection.")
label = tk.Label(window, textvariable=text_var, anchor=tk.CENTER, bg="lightblue", height=3, width=30, bd=3)
label.pack(pady=20)  # Add some padding to the top

# combobox function to handle the selection
def on_select(event):
    #print("Selected:", combo.get())
    text_var.set(combo.get())

# Bind the selection event to the function
combo.bind("<<ComboboxSelected>>", on_select)

#popup
def open_popup():
    popup = tk.Toplevel(window)
    popup.title("Popup Window")

    # Add content to the popup window
    label = tk.Label(popup, text="This is a popup window!")
    label.pack(pady=20)


button = ttk.Button(window, text="Open Popup", command=open_popup)
button.pack(pady=20)

# Start the main loop
window.mainloop()