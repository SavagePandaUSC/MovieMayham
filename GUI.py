import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from storage import *

"""still to add:
add series as well
lang, rating, country (drop down)
api result list: show scroll wheel and "next"
parental warning when a movie is rated 18+
"show watchlist" button
"""

window = tk.Tk()
window.title("Movie Organizer")
window.geometry("600x300")

#fonts and colors
font1 = font.Font(family="Constantia", size=16)
font2 = font.Font(family="Constantia", size=14, slant="italic")

#frame0: show/movie selection
frame0 = tk.Frame(window)
frame0.pack()

#frame1: selection frame
frame1 = tk.Frame(window)
frame1.pack()
#frame1 widgets
filterLabel = tk.Label(frame1, text="Filter by:")
filterLabel.pack(side=tk.TOP)
#frame1a: checkboxes frame
frame1a = tk.Frame(frame1)
frame1a.pack()
titleCheckVar = tk.BooleanVar()
langCheckVar = tk.BooleanVar()
countryCheckVar = tk.BooleanVar()
dirCheckVar = tk.BooleanVar()
yrCheckVar = tk.BooleanVar()
genreCheckVar = tk.BooleanVar()
titleCheckBox = tk.Checkbutton(frame1a, text="Title", variable=titleCheckVar)
langCheckBox = tk.Checkbutton(frame1a, text="Language", variable=langCheckVar)
countryCheckBox = tk.Checkbutton(frame1a, text="Country", variable=countryCheckVar)
dirCheckBox = tk.Checkbutton(frame1a, text="Director", variable=dirCheckVar)
yrCheckBox = tk.Checkbutton(frame1a, text="Year", variable=yrCheckVar)
genreCheckBox = tk.Checkbutton(frame1a, text="Genre", variable=genreCheckVar)
titleCheckBox.pack(side=tk.LEFT)
langCheckBox.pack(side=tk.LEFT)
countryCheckBox.pack(side=tk.LEFT)
dirCheckBox.pack(side=tk.LEFT)
yrCheckBox.pack(side=tk.LEFT)
genreCheckBox.pack(side=tk.LEFT)
enterButton = tk.Button(frame1a, text="Enter")
enterButton.pack(side = tk.RIGHT)

#frame2: input frame
frame2 = tk.Frame(window)
frame2.pack()
##note: grid_remove() and grid() to hide and unhide widgets. for initialization all are hidden
#frame2 widgets - left
titleLabel = tk.Label(frame2, text="Title")
titleLabel.grid(row=0,column=0)
langLabel = tk.Label(frame2, text="Language Code")
langLabel.grid(row=1,column=0)
countryLabel = tk.Label(frame2, text="Country")
countryLabel.grid(row=2,column=0)
dirLabel=tk.Label(frame2, text="Director")
dirLabel.grid(row=3,column=0)
yrLabel=tk.Label(frame2, text="Year")
yrLabel.grid(row=4,column=0)
genreLabel = tk.Label(frame2, text="Genre")
genreLabel.grid(row=5,column=0)
#frame2 widgets - right
titleEntry = tk.Entry(frame2)
titleEntry.grid(row=0,column=1)
lang_vals = ["placeholder"]
langCombo = ttk.Combobox(frame2, values=lang_vals)
langCombo.grid(row=1,column=1)
country_vals = ["placeholder"]
countryCombo = ttk.Combobox(frame2, values=country_vals)
countryCombo.grid(row=2,column=1)
dirEntry = tk.Entry(frame2)
dirEntry.grid(row=3,column=1)
yrEntry = tk.Entry(frame2)
yrEntry.grid(row=4,column=1)
genre_vals = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", 
"History", "Horror", "Music", "Mystery", "Romance", "Science fiction", "Tv movie", "Thriller", "War", "Western"]
genreCombo = ttk.Combobox(frame2, values=genre_vals)
genreCombo.grid(row=5,column=1)
#frame2a: fetch and clear buttons
frame2a = tk.Frame(frame2)
frame2a.grid(row=6,column=1)
fetchButton = tk.Button(frame2a, text="Fetch")
fetchButton.pack(side=tk.RIGHT)
clearButton = tk.Button(frame2a, text="Clear")
clearButton.pack(side=tk.RIGHT)
#make invisible:
def make_frame2_invisible():
    titleLabel.grid_remove()
    langLabel.grid_remove()
    countryLabel.grid_remove()
    dirLabel.grid_remove()
    yrLabel.grid_remove()
    genreLabel.grid_remove()
    titleEntry.grid_remove()
    langCombo.grid_remove()
    countryCombo.grid_remove()
    dirEntry.grid_remove()
    yrEntry.grid_remove()
    genreCombo.grid_remove()
    frame2a.grid_remove()
make_frame2_invisible()

#enter button
def enterButtonPress():
    frame2a.grid()
    enterButton.pack_forget()
    titleCheckBox.config(state=tk.DISABLED)
    langCheckBox.config(state=tk.DISABLED)
    countryCheckBox.config(state=tk.DISABLED)
    dirCheckBox.config(state=tk.DISABLED)
    yrCheckBox.config(state=tk.DISABLED)
    genreCheckBox.config(state=tk.DISABLED)
    if titleCheckVar.get()==True:
        titleLabel.grid()
        titleEntry.grid()
    if langCheckVar.get()==True:
        langLabel.grid()
        langCombo.grid()
    if countryCheckVar.get()==True:
        countryLabel.grid()
        countryCombo.grid()
    if dirCheckVar.get()==True:
        dirLabel.grid()
        dirEntry.grid()
    if yrCheckVar.get()==True:
        yrLabel.grid()
        yrEntry.grid()
    if genreCheckVar.get()==True:
        genreLabel.grid()
        genreCombo.grid()

enterButton.configure(command=enterButtonPress)

def clearButtonPress():
    titleCheckVar.set(0)
    langCheckVar.set(0) 
    countryCheckVar.set(0)
    dirCheckVar.set(0)
    yrCheckVar.set(0)
    genreCheckVar.set(0)
    make_frame2_invisible()
    enterButton.pack()
    titleCheckBox.config(state=tk.NORMAL)
    langCheckBox.config(state=tk.NORMAL)
    countryCheckBox.config(state=tk.NORMAL)
    dirCheckBox.config(state=tk.NORMAL)
    yrCheckBox.config(state=tk.NORMAL)
    genreCheckBox.config(state=tk.NORMAL)

clearButton.configure(command=clearButtonPress)

##fetching
#items will be the (1st) list of 20 results from the API. if there are multiple pages, the "next" button will cycle through them
items = ["test","test","test","test","test","test","test","test","test","test","test","test","test","test","test","test","test","test","test","test",]

listFrame = tk.Frame(window)
listFrame.pack()
listFrame.pack_forget()

scrollFrame = tk.Frame(listFrame)
scrollFrame.pack()

listbox = tk.Listbox(scrollFrame, selectmode=tk.MULTIPLE)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(scrollFrame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)

for item in items:
    listbox.insert(tk.END, item)

def missing_input():
    titleInput = titleEntry.get()
    langInput = langCombo.get()
    countryInput = countryCombo.get()
    dirInput = dirEntry.get()
    yrInput = yrEntry.get()
    genreInput = genreCombo.get()
    if titleCheckVar.get() == True and titleInput == "":
        return True
    if langCheckVar.get() == True and langInput == "":
        return True
    if dirCheckVar.get() == True and dirInput == "":
        return True
    if yrCheckVar.get() == True and yrInput == "":
        return True
    if genreCheckVar.get() == True and genreInput == "":
        return True
    else:
        return False

def fetchButtonPress():
    if missing_input():
        msg=messagebox.showinfo("Error", "Missing input.")
    else:
        frame1.pack_forget()
        frame2.pack_forget()
        listFrame.pack()

fetchButton.configure(command=fetchButtonPress)

window.mainloop()