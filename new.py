import tkinter as tk
from tkinter import ttk, messagebox
from storage import search_movies, search_movie_by_id, get_director_by_id, correct, save_movie, delete, get_id

# Initialize window
window = tk.Tk()
window.title("Movie Organizer")
window.geometry("1000x600")

# Data to manage watchlist and API pagination
current_results = []
current_page = 1
total_pages = 1
watchlist = []

# Frame 1: Filter options
frame1 = tk.Frame(window)
frame1.pack(pady=10)

filter_label = tk.Label(frame1, text="Filter by:")
filter_label.pack(side=tk.LEFT, padx=5)

genre_vals = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
]
genre_map = {v: i for i, v in enumerate(genre_vals, start=1)}

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

# Frame 2: Results and Watchlist Display
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

# Box 2: Saved Watchlist
watchlist_frame = tk.LabelFrame(frame2, text="Saved Watchlist", padx=10, pady=10)
watchlist_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

watchlist_listbox = tk.Listbox(watchlist_frame, height=20, width=50)
watchlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

watchlist_scrollbar = ttk.Scrollbar(watchlist_frame, orient=tk.VERTICAL, command=watchlist_listbox.yview)
watchlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
watchlist_listbox.config(yscrollcommand=watchlist_scrollbar.set)

# Frame 3: Buttons for Actions
frame3 = tk.Frame(window)
frame3.pack(pady=10)

add_button = ttk.Button(frame3, text="Add to Watchlist")
add_button.pack(side=tk.LEFT, padx=5)

remove_button = ttk.Button(frame3, text="Remove from Watchlist")
remove_button.pack(side=tk.LEFT, padx=5)

# Frame 4: Pagination
frame4 = tk.Frame(window)
frame4.pack(pady=10)

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
    
    # Debugging API response
    print("Results fetched:", results)  # Log full response for debugging

    current_results = results.get("results", [])
    current_page = page
    total_pages = results.get("total_pages", 1)

    if not current_results:
        messagebox.showinfo("No Results", "No movies found. Try different filters.")
        return None

    update_results_listbox(current_results)


def fetch_next_page():
    if current_page < total_pages:
        fetch_movies(current_page + 1)

def fetch_previous_page():
    if current_page > 1:
        fetch_movies(current_page - 1)

def add_to_watchlist():
    selected_indices = results_listbox.curselection()
    for idx in selected_indices:
        movie = current_results[idx]
        if movie not in watchlist:
            watchlist.append(movie)
            watchlist_listbox.insert(tk.END, movie.get("title", "Unknown"))
    messagebox.showinfo("Success", "Selected movies added to watchlist.")

def remove_from_watchlist():
    selected_indices = watchlist_listbox.curselection()
    for idx in selected_indices[::-1]:  # Remove in reverse to avoid index issues
        watchlist.pop(idx)
        watchlist_listbox.delete(idx)
    messagebox.showinfo("Success", "Selected movies removed from watchlist.")

# Button configurations
fetch_button.configure(command=lambda: fetch_movies(1))
next_button.configure(command=fetch_next_page)
prev_button.configure(command=fetch_previous_page)
add_button.configure(command=add_to_watchlist)
remove_button.configure(command=remove_from_watchlist)

# Run the main loop
window.mainloop()

if __name__ == "__main__":
  pass