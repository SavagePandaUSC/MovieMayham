import tkinter as tk
from tkinter import ttk, messagebox, font
from storage import search_movies, save_movie, delete, get_id

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

genre_map = {
    "": None,
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "TV Movie": 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37,
    "Action & Adventure": 10759,
    "Kids": 10762,
    "News": 10763,
    "Reality": 10764,
    "Sci-Fi & Fantasy": 10765,
    "Soap": 10766,
    "Talk": 10767,
    "War & Politics": 10768
}

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
language_values = ["", "English", "Spanish", "French", "German", "Chinese", "Korean", "Japanese", "Portuguese", "other"]
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
list_frame = tk.LabelFrame(frame2, text="Saved list", padx=10, pady=10)
list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

list_listbox = tk.Listbox(list_frame, height=20, width=50)
list_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=list_listbox.yview)
list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
list_listbox.config(yscrollcommand=list_scrollbar.set)

## Frame 3: Buttons for Actions
frame3 = tk.Frame(window)
frame3.pack(pady=10)

clear_results_button = ttk.Button(frame3, text="Clear search results")
clear_results_button.pack(side=tk.LEFT, padx=5)

add_button = ttk.Button(frame3, text="Add to list")
add_button.pack(side=tk.LEFT, padx=5)

remove_button = ttk.Button(frame3, text="Remove from list")
remove_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(frame3, text="Save to Watched")
save_button.pack(side=tk.LEFT, padx=5)

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
    results_listbox.delete(0, tk.END)
    for movie in movies:
        title = movie.get("title", "Unknown")
        release_date = movie.get("release_date", "N/A")
        adult = movie.get("adult", False)

        display_text = f"{title} ({release_date})"
        if adult:
            display_text += " [18+]"

        results_listbox.insert(tk.END, display_text)


def fetch_movies(page=1):
    global current_results, current_page, total_pages

    title = title_var.get()
    genre_name = genre_var.get()
    genre = genre_map.get(genre_name)  # Now this will return the genre ID
    language = language_var.get()
    year = year_var.get()

    if not title:
        messagebox.showerror("Error", "Please enter a title.")
        return None

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
    selected_index = results_listbox.curselection()
    for index in selected_index:
        movie = current_results[index]
        if movie not in list:
            list.append(movie)
            list_listbox.insert(tk.END, movie.get("title", "Unknown"))
    messagebox.showinfo("Success", "Selected movies added to list.")


def remove_from_list():
    selected_index = list_listbox.curselection()
    for index in selected_index[::-1]:  # Remove in reverse to avoid index issues
        list.pop(index)
        list_listbox.delete(index)
    messagebox.showinfo("Success", "Selected movies removed from list.")


def update_page_repr():
    pg_rep.config(text=f"Page {current_page} of {total_pages}")


# Button configurations
clear_filters_button.configure(command=clear_filters)
clear_results_button.configure(command=clear_results)
fetch_button.configure(command=lambda: fetch_movies(1))
next_button.configure(command=next_page)
prev_button.configure(command=previous_page)
add_button.configure(command=add_to_list)
remove_button.configure(command=remove_from_list)
save_button.configure(command=save_movie)

# Run the main loop
window.mainloop()

if __name__ == "__main__":
  pass