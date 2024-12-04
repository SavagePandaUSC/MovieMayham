import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from storage import search_movies, search_movie_by_id, get_director_by_id, correct, save_movie, delete, get_id
import requests

"""still to add:
tv shows
lang, rating, country (drop down)
api result list: show scroll wheel and "next"
parental warning when a movie is rated 18+
"show watchlist" button
note: some filters (eg genres) will be different between shows and movies
FOR TONIGHT:
ability to search for a movie, have at least 2 or 3 filters, be able to save the movie
preferably: remove a movie also
NOTES - fix for final vers.:
    title will be selected by default for now
    no director filter yet
    no add/remove
    no filters
"""

# initialize window
window = tk.Tk()
window.title("Movie Organizer")
window.geometry("600x300")

# frame0: holds show/movie selection
# currently: doesn't exist/holds nothing
#frame0 = tk.Frame(window)
#frame0.pack()

# frame1: selection frame
frame1 = tk.Frame(window)
frame1.pack()
# frame1 widgets
filterLabel = tk.Label(frame1, text="Filter by:")
filterLabel.pack(side=tk.TOP)
# frame1a - holds everything besides filterLabel in Frame1:
frame1a = tk.Frame(frame1)
frame1a.pack()
# check variables (0 / False by default):
titleCheckVar = tk.BooleanVar()
langCheckVar = tk.BooleanVar()
countryCheckVar = tk.BooleanVar() 
dirCheckVar = tk.BooleanVar()
yrCheckVar = tk.BooleanVar()
genreCheckVar = tk.BooleanVar()
# checkboxes:
titleCheckBox = tk.Checkbutton(frame1a, text="Title", variable=titleCheckVar)
langCheckBox = tk.Checkbutton(frame1a, text="Language", variable=langCheckVar)
countryCheckBox = tk.Checkbutton(frame1a, text="Country", variable=countryCheckVar)
dirCheckBox = tk.Checkbutton(frame1a, text="Director", variable=dirCheckVar)
yrCheckBox = tk.Checkbutton(frame1a, text="Year", variable=yrCheckVar)
genreCheckBox = tk.Checkbutton(frame1a, text="Genre", variable=genreCheckVar)
# pack checkboxes:
titleCheckBox.pack(side=tk.LEFT)
langCheckBox.pack(side=tk.LEFT)
countryCheckBox.pack(side=tk.LEFT)
dirCheckBox.pack(side=tk.LEFT)
yrCheckBox.pack(side=tk.LEFT)
genreCheckBox.pack(side=tk.LEFT)
# enter button
enterButton = tk.Button(frame1a, text="Enter")
enterButton.pack(side = tk.RIGHT)

# FOR DRAFT1: this removes the user's ability to check/uncheck the title, leaving it checked by default
titleCheckVar.set(1)
titleCheckBox.config(state=tk.DISABLED)

# frame2: input frame
# frame2 is structured so that all the labels are on the left side (grid column position 0),
# and all the actual entry boxes / combo boxes that take input are on the right side (grid column position 1).
## note: grid_remove() and grid() to hide and unhide widgets. all are removed individually at initialization,
## so they can be made visible/invisible depending on what the user selects.
frame2 = tk.Frame(window)
frame2.pack()
#frame2 widgets - left (labels)
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
#frame2 widgets - right (input)
titleEntry = tk.Entry(frame2)
titleEntry.grid(row=0,column=1)
lang_vals = ["placeholder"] #add languages of choice
langCombo = ttk.Combobox(frame2, state="readonly", values=lang_vals)
langCombo.grid(row=1,column=1)
country_vals = ["placeholder"] #add countries of choice
countryCombo = ttk.Combobox(frame2, state="readonly", values=country_vals)
countryCombo.grid(row=2,column=1)
dirEntry = tk.Entry(frame2)
dirEntry.grid(row=3,column=1)
yrEntry = tk.Entry(frame2)
yrEntry.grid(row=4,column=1)
genre_vals = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", 
"History", "Horror", "Music", "Mystery", "Romance", "Science fiction", "Tv movie", "Thriller", "War", "Western"]
genreCombo = ttk.Combobox(frame2, state="readonly", values=genre_vals)
genreCombo.grid(row=5,column=1)
# frame2a: fetch and clear buttons
# goes directly underneath and to the right of the rest of frame2
frame2a = tk.Frame(frame2)
frame2a.grid(row=6,column=1)
fetchButton = tk.Button(frame2a, text="Fetch")
fetchButton.pack(side=tk.RIGHT)
clearButton = tk.Button(frame2a, text="Clear")
clearButton.pack(side=tk.RIGHT)
# to make all invisible:
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

# function for enter button:
# once pressed, it will reveal whatever filters were selected by the user, along with 
# revealing the fetch and clear buttons (frame2a), making the enter button itself invisible,
# and disabling all the checkbuttons.
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

###########################################################################
# FETCHING
###########################################################################

# fetchingFrame: the main frame that holds the scrollable listbox, and the add/remove/[view list] buttons. [still to add]
# the whole thing is removed by default until "fetch" is pressed.
fetchingFrame = tk.Frame(window)
fetchingFrame.pack()
fetchingFrame.pack_forget()

# fFrameLeft: the left side of the fetchingFrame, holds the ADD/REMOVE buttons
fFrameLeft = tk.Frame(fetchingFrame)
fFrameLeft.pack(side=tk.LEFT)
# fFrameLeft widgets
addButton = tk.Button(fFrameLeft, text="ADD")
addButton.pack()
removeButton = tk.Button(fFrameLeft, text="REMOVE")
removeButton.pack()

#fFrameRight: the right side of the fetchingFrame, holds the scrollable listbox
fFrameRight = tk.Frame(fetchingFrame)
fFrameRight.pack(side=tk.RIGHT)
# the listbox
listbox = tk.Listbox(fFrameRight, width=50, selectmode=tk.MULTIPLE)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# the listbox's scrollbar
scrollbar = tk.Scrollbar(fFrameRight, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# attaches scrollbar to listbox
listbox.config(yscrollcommand=scrollbar.set)

# function to clear all items in the listbox (eg. refreshes the fetched movies)
def clear_listbox():
    listbox.delete(0,tk.END)

###########################################################################
# FETCHING-SECTION BUTTONS
###########################################################################

def clearButtonPress():
    #titleCheckVar.set(0) #FOR DRAFT1: this is disabled because we wanted 'title' to be checked by default/uncheckable
    langCheckVar.set(0) 
    countryCheckVar.set(0)
    dirCheckVar.set(0)
    yrCheckVar.set(0)
    genreCheckVar.set(0)
    make_frame2_invisible()
    enterButton.pack()
    #titleCheckBox.config(state=tk.NORMAL) #this is disabled for same reason as above^
    langCheckBox.config(state=tk.NORMAL)
    countryCheckBox.config(state=tk.NORMAL)
    dirCheckBox.config(state=tk.NORMAL)
    yrCheckBox.config(state=tk.NORMAL)
    genreCheckBox.config(state=tk.NORMAL)
    fetchingFrame.pack_forget()
    #clear all input:
    titleEntry.delete(0, tk.END)
    langCombo.set("")
    countryCombo.set("")
    dirEntry.delete(0, tk.END)
    yrEntry.delete(0, tk.END)
    genreCombo.set("")

clearButton.configure(command=clearButtonPress)

"""to add later:
##next and prev buttons
nextButton = tk.Button(fetchingFrame, text="Next")
nextButton.pack(side=tk.RIGHT)
prevButton = tk.Button(fetchingFrame, text="Prev")
prevButton.pack(side=tk.RIGHT)"""

# define input variables:
# for some reason just putting these input variabes outside the missing_input() and fetchButtonPress() functions
# would break and cause issues with the functions. copying them this way, 3 separate times (once outside any functions,
# once in the missing_input() and once in the fetchButtonPress()), allows the program to work as intended. Not sure why.
titleInput = titleEntry.get()
langInput = langCombo.get()
countryInput = countryCombo.get()
dirInput = dirEntry.get()
yrInput = yrEntry.get()
genreInput = genreCombo.get()

# function that finds if any of the text fields/drop downs are empty
def missing_input():
    # define input variables (again):
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
    if countryCheckVar.get() == True and countryInput == "":
        return True
    if dirCheckVar.get() == True and dirInput == "":
        return True
    if yrCheckVar.get() == True and yrInput == "":
        return True
    if genreCheckVar.get() == True and genreInput == "":
        return True
    else:
        return False

# fetch button function:
# throws error popup if there are any missing inputs.
# else, sorts through the search_movies(titleInput) dictionary and returns the name and year of any given movie
# returned by the API, and adds them each individually to the scrollable listbox.
# CURRENTLY there is no next/prev list selection, nor is there a way I can find to get the movie's ID. this is crucial
# for adding the movies to the user's new database, so this should be highest priority.
def fetchButtonPress():
    clear_listbox()
    # define input variables (again):
    titleInput = titleEntry.get()
    langInput = langCombo.get()
    countryInput = countryCombo.get()
    dirInput = dirEntry.get()
    yrInput = yrEntry.get()
    genreInput = genreCombo.get()
    if missing_input():
        msg=messagebox.showinfo("Error", "Missing input.")
    else:
        fetchingFrame.pack()
        resultsDic = search_movies(titleInput)
        for k in resultsDic['results']:
            year_str = ""
            title_str = ""
            for k2 in k:
                if k2 == "release_date":
                    year_str = k[k2][:4]
                if k2 == 'title':
                    title_str = k[k2]
            listbox.insert(tk.END, title_str + " : " + year_str)

fetchButton.configure(command=fetchButtonPress)

"""to add:
add, remove, and show list buttons"""
        
window.mainloop()

def isAdult(data):
    """returns True or False on whether a movie is adult or not. It accepts the dictionary of movie data"""
    
    return data['adult']