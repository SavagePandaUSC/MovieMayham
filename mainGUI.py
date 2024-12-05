import tkinter as tk
from tkinter import ttk, messagebox
from storage import search_movies, save_movie, delete, get_id

# Create window
window = tk.Tk()
window.title("Movie Organizer")
window.geometry("1200x800")

# Data to manage list and pages
current_results = []
current_page = 1
total_pages = 1
list = []

## Frame 1: Filter options
frame1 = tk.Frame(window)
frame1.pack(pady=10)

filter_label = tk.Label(frame1, text="Filter by:")
filter_label.pack(side=tk.LEFT, padx=5)

genre_vals = [
    "", "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
]

genre_map = {
    "": None,
     28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western",
    # TV Genres
    10759: "Action & Adventure",
    10762: "Kids",
    10763: "News",
    10764: "Reality",
    10765: "Sci-Fi & Fantasy",
    10766: "Soap",
    10767: "Talk",
    10768: "War & Politics"
}

# Widgets for filters
title_var = tk.StringVar()
title_entry = ttk.Entry(frame1, textvariable=title_var, width=30)
title_entry.pack(side=tk.LEFT, padx=5)

genre_var = tk.StringVar()
genre_combo = ttk.Combobox(frame1, state="readonly", values=genre_vals, textvariable=genre_var)
genre_combo.pack(side=tk.LEFT, padx=5)

language_var = tk.StringVar()
language_combo = ttk.Combobox(frame1, state="readonly", values=["en", "es", "fr", "de"], textvariable=language_var)
language_combo.pack(side=tk.LEFT, padx=5)

year_var = tk.StringVar()
year_entry = ttk.Entry(frame1, textvariable=year_var, width=10)
year_entry.pack(side=tk.LEFT, padx=5)

fetch_button = ttk.Button(frame1, text="Fetch")
fetch_button.pack(side=tk.LEFT, padx=5)

## Frame 2: Results and list Display
frame2 = tk.Frame(window)
frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Box 1: Search Results
results_frame = tk.LabelFrame(frame2, text="Search Results", padx=10, pady=10)
results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

results_listbox = tk.Listbox(results_frame, height=20, width=50)
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
    genre = genre_map.get(genre_var.get())
    language = language_var.get()
    year = year_var.get()

    if not title:
        messagebox.showerror("Error", "Please enter a title.")
        return None

    results = search_movies(title, genre, year, language, page)

    print("Results fetched:", results)  # a simple terminal test
    
    current_results = results.get("results", [])
    current_page = page
    total_pages = results.get("total_pages", 1)

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