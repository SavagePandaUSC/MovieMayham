import tkinter as tk
from tkinter import ttk
from tkinter import font

window = tk.Tk()
window.title("Movie Organizer")
window.geometry("600x300")

#fonts and colors
font1 = font.Font(family="Constantia", size=16)
font2 = font.Font(family="Constantia", size=14, slant="italic")

#frame1: selection frame
frame1 = tk.Frame(window)
frame1.pack()
#frame1 widgets
filterLabel = tk.Label(frame1, text="Filter by:")
filterLabel.pack(side=tk.TOP)
#frame1a: checkboxes frame
frame1a = tk.Frame(frame1)
frame1a.pack()
titleCheckVar = tk.IntVar()
langCheckVar = tk.IntVar()
dirCheckVar = tk.IntVar()
yrCheckVar = tk.IntVar()
genreCheckVar = tk.IntVar()
titleCheckBox = tk.Checkbutton(frame1a, text="Title", variable=titleCheckVar)
langCheckBox = tk.Checkbutton(frame1a, text="Language", variable=langCheckVar)
dirCheckBox = tk.Checkbutton(frame1a, text="Director", variable=dirCheckVar)
yrCheckBox = tk.Checkbutton(frame1a, text="Year", variable=yrCheckVar)
genreCheckBox = tk.Checkbutton(frame1a, text="Genre", variable=genreCheckVar)
titleCheckBox.pack(side=tk.LEFT)
langCheckBox.pack(side=tk.LEFT)
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
langLabel = tk.Label(frame2, text="Language Code (ie. 'eng')")
langLabel.grid(row=1,column=0)
dirLabel=tk.Label(frame2, text="Director")
dirLabel.grid(row=2,column=0)
yrLabel=tk.Label(frame2, text="Year")
yrLabel.grid(row=3,column=0)
genreLabel = tk.Label(frame2, text="Genre")
genreLabel.grid(row=4,column=0)
#frame2 widgets - right
titleEntry = tk.Entry(frame2)
titleEntry.grid(row=0,column=1)
langEntry = tk.Entry(frame2)
langEntry.grid(row=1,column=1)
dirEntry = tk.Entry(frame2)
dirEntry.grid(row=2,column=1)
yrEntry = tk.Entry(frame2)
yrEntry.grid(row=3,column=1)
genre_vals = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", 
"History", "Horror", "Music", "Mystery", "Romance", "Science fiction", "Tv movie", "Thriller", "War", "Western"]
genreCombo = ttk.Combobox(frame2, values=genre_vals)
genreCombo.grid(row=4,column=1)
#frame2a: fetch and clear buttons
frame2a = tk.Frame(frame2)
frame2a.grid(row=5,column=1)
fetchButton = tk.Button(frame2a, text="Fetch")
fetchButton.pack(side=tk.RIGHT)
clearButton = tk.Button(frame2a, text="Clear")
clearButton.pack(side=tk.RIGHT)
#make invisible:
titleLabel.grid_remove()
langLabel.grid_remove()
dirLabel.grid_remove()
yrLabel.grid_remove()
genreLabel.grid_remove()
titleEntry.grid_remove()
langEntry.grid_remove()
dirEntry.grid_remove()
yrEntry.grid_remove()
genreCombo.grid_remove()
frame2a.grid_remove()

#enter button
def enterButtonPress():
    frame2a.grid()
    if titleCheckVar:
        titleLabel.grid()
        titleEntry.grid()
    if langCheckVar:
        langLabel.grid()
        langEntry.grid()
    if dirCheckVar:
        dirLabel.grid()
        dirEntry.grid()
    if yrCheckVar:
        yrLabel.grid()
        yrEntry.grid()
    if genreCheckVar:
        genreLabel.grid()
        genreCombo.grid()

enterButton.configure(command=enterButtonPress)

def clearButtonPress():
    langCheckVar.set(0) 
    dirCheckVar.set(0)
    yrCheckVar.set(0)
    genreCheckVar.set(0)
clearButton.configure(command=clearButtonPress)

def fetchButtonPress():
    titleInput = titleEntry.get()
    langInput = langEntry.get()
    dirInput = dirEntry.get()
    yrInput = yrEntry.get()
    genreInput = genreCombo.get()

    print(titleEntry)
    print(langInput)
    print(dirInput)
    print(yrInput)
    print(genreInput)
fetchButton.configure(command=fetchButtonPress)

window.mainloop()