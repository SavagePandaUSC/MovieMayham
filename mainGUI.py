import tkinter as tk
from tkinter import ttk, messagebox, font
from storage import search_movies, save_movie, delete, get_id
from PIL import Image, ImageTk
import requests
from io import BytesIO

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
desc = tk.Label(frame0, text="Search for movies you've seen and add them to your list. Then, click them to view their stats.", font=descFont)
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

add_button = ttk.Button(frame3, text="Add to holding list")
add_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(frame3, text="Save Holding movies to Watched")
save_button.pack(side=tk.RIGHT, padx=5)

remove_button = ttk.Button(frame3, text="Remove from holding list")
remove_button.pack(side=tk.RIGHT, padx=5)

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
    title_entry.delete(0, tk.END)
    language_combo.current(0)
    year_entry.delete(0, tk.END)
    genre_combo.current(0)

def clear_results():
    results_listbox.delete(0,tk.END)

def update_results_listbox(movies):
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
        print(type(current_results[0]))
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

    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"  # Construct the poster URL

    response = requests.get(poster_url)
    response.raise_for_status()  # Raise an error if the request failed
    img_data = BytesIO(response.content)  # Read the image data
    img = Image.open(img_data)

        # Resize the image to fit in the window
    img = img.resize((400, 600), Image.Resampling.LANCZOS)  # Updated for newer Pillow versions
    poster_image = ImageTk.PhotoImage(img)

        # Create a new window to display the poster
    poster_window = tk.Toplevel(window)
    poster_window.title(f"Poster - {movie.get('title', 'Unknown')}")
    poster_window.geometry("420x620")  # Adjust the size slightly larger than the image

    label = tk.Label(poster_window, image=poster_image)
    label.image = poster_image 
    label.pack()

def save_list():
    """Iterates throught throuth the holding list box and saves it to a file"""
    
    movie_ids = [saved_list_ids[index] for index in range(list_listbox.size())]

    for id in movie_ids:
        save_movie(id, "10-10-1010", "11")
    
    messagebox.showinfo("Success", "All movies in Holding updated to Saved List!")
   


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

# Run the main loop
window.mainloop()

if __name__ == "__main__":
  pass