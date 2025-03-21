import tkinter as tk
from tkinter import ttk, messagebox, font
from storage import search_movies, save_movie, delete, fetch_summary
from PIL import Image, ImageTk
import requests
from io import BytesIO
from MovieClass import Movie, make_movie_objects

# Create window
window = tk.Tk()
window.title("Movie Organizer")
window.geometry("1200x800")

## Fonts
titleFont = font.Font(size=30)
descFont = font.Font(size=10, slant='italic')

# Data to manage list and pages
current_results = []
current_page = 1
total_pages = 1
list = []
results_mapping = {}  
saved_list_ids = {}  

## Frame 0: Title and Desc
frame0 = tk.Frame(window)
frame0.pack()

title = tk.Label(frame0, text="My Movies List", font=titleFont)
title.pack(side=tk.TOP)
desc = tk.Label(frame0, text="Search for movies you've seen, view their poster, and add them to your Holding list. Select an item in the Holding list\nif you wish remove it. Then, click 'update to Watch list', and view your Watch list to see all your movies' stats.", font=descFont)
desc.pack(side=tk.BOTTOM)

## Frame 1: Filter options
frame1 = tk.Frame(window)
frame1.pack(pady=10)

filter_label = tk.Label(frame1, text="Filter by:")
filter_label.grid(row=0,column=0, padx=5)

genre_vals = [
    "", "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
]


# Widgets for filters
title_label = tk.Label(frame1, text="Title")
title_var = tk.StringVar()
title_entry = ttk.Entry(frame1, textvariable=title_var, width=30)
title_entry.grid(row=0,column=1,padx=5)
title_label.grid(row=1,column=1,padx=5)

genre_label = tk.Label(frame1, text="Genre")
genre_var = tk.StringVar()
genre_combo = ttk.Combobox(frame1, state="readonly", values=genre_vals, textvariable=genre_var)
genre_combo.grid(row=0,column=2,padx=5)
genre_label.grid(row=1,column=2,padx=5)

language_label = tk.Label(frame1, text="Language")
language_var = tk.StringVar()
language_values = ["", "English", "Spanish", "French", "German", "Chinese", "Korean", "Japanese", "Portuguese", "Hindi"]
language_values_dict = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Korean": "ko",
    "Japanese": "ja",
    "Portuguese": "pt",
    "Hindi": "hi",
    "": ""
}

language_combo = ttk.Combobox(frame1, state="readonly", values=language_values, textvariable=language_var)
language_combo.grid(row=0,column=3,padx=5)
language_label.grid(row=1,column=3,padx=5)

year_label = tk.Label(frame1, text="Year")
year_var = tk.StringVar()
year_entry = ttk.Entry(frame1, textvariable=year_var, width=10)
year_entry.grid(row=0,column=4,padx=5)
year_label.grid(row=1,column=4,padx=5)

fetch_button = ttk.Button(frame1, text="Fetch")
fetch_button.grid(row=0,column=5,padx=5)

clear_filters_button = ttk.Button(frame1, text="Clear filters")
clear_filters_button.grid(row=1,column=5, padx=5)

## Frame 2: Results and list Display
frame2 = tk.Frame(window)
frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Box 1: Search Results
results_frame = tk.LabelFrame(frame2, text="Search Results", padx=10, pady=10)
results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

results_listbox = tk.Listbox(results_frame, height=20, width=50, selectmode=tk.MULTIPLE)
results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_listbox.yview)
results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_listbox.config(yscrollcommand=results_scrollbar.set)

# Box 2: Saved list
list_frame = tk.LabelFrame(frame2, text="Holding list", padx=10, pady=10)
list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

list_listbox = tk.Listbox(list_frame, height=20, width=50)
list_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=list_listbox.yview)
list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
list_listbox.config(yscrollcommand=list_scrollbar.set)

## Frame 3: Buttons for Actions
frame3 = tk.Frame(window)
frame3.pack(pady=10,fill='x')

clear_results_button = ttk.Button(frame3, text="Clear search results")
clear_results_button.pack(side=tk.LEFT, padx=5)

view_poster_button = ttk.Button(frame3, text="View Poster")
view_poster_button.pack(side=tk.LEFT, padx=5)

add_button = ttk.Button(frame3, text="Add to Holding list")
add_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(frame3, text="Update Holding list to Watch list")
save_button.pack(side=tk.RIGHT, padx=5)

remove_button = ttk.Button(frame3, text="Remove from Holding list")
remove_button.pack(side=tk.RIGHT, padx=5)

view_button = ttk.Button(frame3, text="VIEW WATCH LIST")
view_button.pack(side=tk.BOTTOM, padx=5)

## Frame 4: Page Control
frame4 = tk.Frame(window)
frame4.pack(pady=10)

# page number tracker
pg_rep = tk.Label(frame4, text=f"Page {current_page} of {total_pages}")
pg_rep.pack(side=tk.LEFT, padx=10)

# page changing buttons
prev_button = ttk.Button(frame4, text="Previous")
prev_button.pack(side=tk.LEFT, padx=5)

next_button = ttk.Button(frame4, text="Next")
next_button.pack(side=tk.LEFT, padx=5)

# Functions for fetching and updating results

def clear_filters():
    """Clears all filters input by the user"""
    title_entry.delete(0, tk.END)
    language_combo.current(0)
    year_entry.delete(0, tk.END)
    genre_combo.current(0)

def clear_results():
    """Clears all results in the resutls listbox"""
    results_listbox.delete(0,tk.END)

def update_results_listbox(movies):
    """used in fetch_movies to clear & update results listbox each time the fetch button is pressed"""
    global results_mapping
    results_mapping.clear()  
    results_listbox.delete(0, tk.END)

    for index, movie in enumerate(movies):
        title = movie.get("title", "Unknown")
        release_date = movie.get("release_date", "N/A")
        movie_id = movie.get("id", "N/A")  

        display_text = f"{title} ({release_date})"
        results_mapping[index] = movie_id  # Map index to movie ID
        results_listbox.insert(tk.END, display_text)  # Show title and release date

def fetch_movies(page=1):
    """populates the results listbox with results from the API"""
    global current_results, current_page, total_pages

    title = title_var.get()
    genre = genre_var.get()
    language = language_values_dict[language_var.get()] 
    year = year_var.get()
    if not title:
        messagebox.showerror("Error", "Please enter a title.")
        return None
    if(genre == ""):
        genre = None
    results = search_movies(title, genre, year, language, page)

    print(genre)  # Test if genre is now the correct ID
    if genre is None:
        current_results = results.get("results", [])
        #print(type(current_results[0]))
        current_page = page
        total_pages = results.get("total_pages", 1)
    else:
        current_results = results
        #print(type(results))
        current_page = page
        print(len(results))
        total_pages = 5 # this does not work for now 

    if not current_results:
        messagebox.showinfo("No Results", "No movies found. Try different filters.")
        return None

    update_results_listbox(current_results)
    update_page_repr()



def next_page():
    """Increases the page variable by 1 and then calls to change the page forward"""
    if current_page < total_pages:
        fetch_movies(current_page + 1)


def previous_page():
    """Decreases the page variable by 1 and then call to change the page backward"""
    if current_page > 1:
        fetch_movies(current_page - 1)


def add_to_list():
    """Add selected movies to the saved list"""
    selected_indices = results_listbox.curselection()
    for index in selected_indices:
        movie_id = results_mapping.get(index)  # Get the movie ID
        title = current_results[index].get("title", "Unknown")
        release_date = current_results[index].get("release_date", "Unknown")
        display_text = f"{title} ({release_date})"

        # Checks to see if movies is already in the holding list
        if movie_id not in saved_list_ids.values():
            list_listbox.insert(tk.END, display_text)  
            saved_list_ids[list_listbox.size() - 1] = movie_id  # Map saved index to movie ID


def remove_from_list():
    """Remove selected movies from the saved list."""

    selected_indices = list_listbox.curselection()
    for index in selected_indices[::-1]:  # Reverse order to stop index issues
        list_listbox.delete(index)  # Remove item from Listbox
        saved_list_ids.pop(index, None)  # Remove ID from mapping

    messagebox.showinfo("Success", "Selected movies removed from the list.")


def update_page_repr():
    """Updates the page tracker"""
    pg_rep.config(text=f"Page {current_page} of {total_pages}")

def view_poster():
    """Opens the poster of the selected movie in a new Tkinter window."""
    selected_index = results_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Please select a movie to view the poster.")
        return

    movie = current_results[selected_index[0]]
    poster_path = movie.get("poster_path")
    if not poster_path:
        messagebox.showinfo("No Poster", "No poster available for the selected movie.")
        return

    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"  # gets the poster URL

    response = requests.get(poster_url)
    response.raise_for_status()  # Raise an error if the request failed
    img_data = BytesIO(response.content)
    img = Image.open(img_data)

        # Resize the image to fit in the window
    img = img.resize((400, 600), Image.Resampling.LANCZOS)
    poster_image = ImageTk.PhotoImage(img)

        # Create a new window to display the poster
    poster_window = tk.Toplevel(window)
    poster_window.title(f"Poster - {movie.get('title', 'Unknown')}")
    poster_window.geometry("420x620")  # Adjust the size slightly larger than the image

    label = tk.Label(poster_window, image=poster_image)
    label.image = poster_image 
    label.pack()
    

def save_list():
    """Iterates through the holding list box and saves it to a file"""
    
    movie_ids = [saved_list_ids[index] for index in range(list_listbox.size())]

    for id in movie_ids:
        save_movie(id)
    
    messagebox.showinfo("Success", "All movies in Holding updated to Saved List!")


## Frame 5: the watch list screen; will appear when all previous frames are invisible
frame5 = tk.Frame(window)

go_back_button = tk.Button(frame5, text="Go back")
go_back_button.pack()

remove_watch_button = tk.Button(frame5, text="Remove Movie")
remove_watch_button.pack()

# Displaying the Watch List

frame5a = tk.Frame(frame5)
frame5a.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame5a, selectmode='extended')
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tree_scrollbar = ttk.Scrollbar(frame5a, orient=tk.VERTICAL, command=tree.yview)
tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.config(yscrollcommand=tree_scrollbar.set)

style = ttk.Style()
style.configure("Treeview", rowheight=100)

   
# Function for switching to Watch List:

def wrap_text(s,x):
    """to use with description in the tree; will mimic text wrapping by inserting a newline every x words in a string"""
    result = ""
    templist = s.split()
    for i in range(0,len(templist), x):
        result += " ".join(templist[i:i+x]) + "\n"
    return result

def view_watch_list():
    """clear all items in tree first to avoid repeats"""
    for item in tree.get_children():
        tree.delete(item)

    """refreshes to update with information on txt file"""
    holder = make_movie_objects()
    for k in holder.keys():
        parent = tree.insert("", "end", text=holder[k].title + " - " + holder[k].release_date[:4])
        display_info = ("Director: " + holder[k].director + "\nRuntime (min): " + holder[k].runtime + "\nGenre: " + holder[k].genre + "\nDescription: " + wrap_text(fetch_summary(holder[k].id),30))
        tree.insert(parent, "end", text=display_info)

    """Makes all frames but frame5 invisible, simulating a new window"""
    frame0.pack_forget()
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame5.pack(fill=tk.BOTH, expand=True)

def go_back():
    """unhides all frames but frame5, and hides frame5"""
    frame0.pack()
    frame1.pack(pady=10)
    frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    frame3.pack(pady=10,fill='x')
    frame4.pack(pady=10)
    frame5.pack_forget()


def remove_movie_from_watch_list():
    """Remove selected movie from the watch list."""
    selected_item = tree.selection()  # Get selected item in the TreeView
    if not selected_item:
        messagebox.showerror("Error", "Please select a movie to remove.")
        return

    movie_title = tree.item(selected_item, "text").split(" - ")[0]  # Extract the title
    holder = make_movie_objects()

    # Find the movie by title (simplistic approach, assumes unique titles)
    movie_to_remove = None
    for movie in holder.values():
        if movie.title == movie_title:
            movie_to_remove = movie
            break

    if movie_to_remove:
        # Remove the movie using its method
        movie_to_remove.remove_movie()
        messagebox.showinfo("Success", f"Movie '{movie_to_remove.title}' removed from the watch list.")
        view_watch_list()  # Refresh the watch list display
    else:
        messagebox.showerror("Error", "Movie not found in the watch list.")

# Button configurations
clear_filters_button.configure(command=clear_filters)
clear_results_button.configure(command=clear_results)
fetch_button.configure(command=lambda: fetch_movies(1))
next_button.configure(command=next_page)
prev_button.configure(command=previous_page)
add_button.configure(command=add_to_list)
remove_button.configure(command=remove_from_list)
save_button.configure(command=save_list)
view_poster_button.configure(command=view_poster)
view_button.configure(command=view_watch_list)
go_back_button.configure(command=go_back)
remove_watch_button.configure(command=remove_movie_from_watch_list)    

# Run the main loop
window.mainloop()

if __name__ == "__main__":
  pass