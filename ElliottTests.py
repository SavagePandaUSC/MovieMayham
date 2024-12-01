import tkinter as tk
from tkinter import ttk
import requests
from concurrent.futures import ThreadPoolExecutor

# API Configuration
API_KEY = "2fc9ee028a312888352de489e536da81"
BASE_URL = "https://api.themoviedb.org/3"

# Fetch genres from the API
def get_genres():
    """Fetches the list of genres and their IDs."""
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["name"]: genre["id"] for genre in genres}
    else:
        return {}

def fetch_page(genre_id, language, page):
    """Fetches a single page of results, filtering by genre and language."""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genre_id,
        "with_original_language": language,
        "page": page,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []

def discover_movies_by_genre_and_language(genre_id, language):
    """Fetches movies by genre ID and language."""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genre_id,
        "with_original_language": language,
        "page": 1,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    data = response.json()
    total_pages = data.get("total_pages", 1)

    movies = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_page, genre_id, language, page)
            for page in range(1, total_pages + 1)
        ]
        for future in futures:
            movies.extend(future.result())

    return movies

# GUI Implementation
window = tk.Tk()
window.title("Movie Finder")
window.geometry("800x600")

# Variables and UI Components
genres = get_genres()
if not genres:
    print("Failed to load genres. Check your API configuration.")

genre_names = list(genres.keys())
language_var = tk.StringVar(value="en")
genre_var = tk.StringVar(value="Select Genre")
custom_movie_list = []  # List to store user-selected movies
current_page = 0        # Tracks the current page for pagination
paginated_movies = []   # Stores paginated movie data

# Dropdown for genres
genre_combo = ttk.Combobox(window, values=genre_names, textvariable=genre_var)
genre_combo.set("Select Genre")
genre_combo.pack(pady=10)

# Entry for language code
language_label = tk.Label(window, text="Enter Language Code (e.g., 'en'):")
language_label.pack()
language_entry = tk.Entry(window, textvariable=language_var)
language_entry.pack()

# Results box
results_box = tk.Listbox(window, height=15, width=60)
results_box.pack(pady=10)

# Custom list box
custom_list_label = tk.Label(window, text="Your Selected Movies:")
custom_list_label.pack()
custom_list_box = tk.Listbox(window, height=10, width=60, bg="lightyellow")
custom_list_box.pack(pady=10)

# Fetch movies function
def fetch_movies():
    global current_page, paginated_movies
    selected_genre = genre_var.get()
    language = language_var.get().strip()

    if selected_genre not in genres:
        results_box.delete(0, tk.END)
        results_box.insert(tk.END, "Invalid genre selected.")
        return

    genre_id = genres[selected_genre]
    results_box.delete(0, tk.END)
    results_box.insert(tk.END, f"Fetching movies for Genre: {selected_genre}, Language: {language}...")

    movies = discover_movies_by_genre_and_language(genre_id, language)

    if movies:
        # Sort movies by popularity in descending order
        movies = sorted(movies, key=lambda x: x.get('popularity', 0), reverse=True)
        
        # Paginate movies into chunks of 20
        paginated_movies = [movies[i:i + 10] for i in range(0, len(movies), 10)]
        current_page = 0
        display_page()
    else:
        results_box.delete(0, tk.END)
        results_box.insert(tk.END, "No movies found for the selected criteria.")

# Function to display the current page
def display_page():
    global current_page
    results_box.delete(0, tk.END)
    if not paginated_movies:
        results_box.insert(tk.END, "No movies to display.")
        return

    movies_on_page = paginated_movies[current_page]
    for movie in movies_on_page:
        title = movie.get("title", "Unknown Title")
        release_date = movie.get("release_date", "N/A")
        results_box.insert(tk.END, f"{title} (Release Date: {release_date})")

# Navigate to the next page
def next_page():
    global current_page
    if paginated_movies and current_page < len(paginated_movies) - 1:
        current_page += 1
        display_page()

# Navigate to the previous page
def previous_page():
    global current_page
    if paginated_movies and current_page > 0:
        current_page -= 1
        display_page()

# Add movie to custom list
def add_to_custom_list():
    selected_movie = results_box.get(tk.ACTIVE)
    if selected_movie and selected_movie not in custom_movie_list:
        custom_movie_list.append(selected_movie)
        custom_list_box.insert(tk.END, selected_movie)

# Remove movie from custom list
def remove_from_custom_list():
    selected_movie = custom_list_box.get(tk.ACTIVE)
    if selected_movie in custom_movie_list:
        custom_movie_list.remove(selected_movie)
        custom_list_box.delete(tk.ANCHOR)

# Buttons
fetch_button = ttk.Button(window, text="Fetch Movies", command=fetch_movies)
fetch_button.pack(pady=5)

prev_button = ttk.Button(window, text="Previous Page", command=previous_page)
prev_button.pack(pady=5)

next_button = ttk.Button(window, text="Next Page", command=next_page)
next_button.pack(pady=5)

add_button = ttk.Button(window, text="Add to List", command=add_to_custom_list)
add_button.pack(pady=5)

remove_button = ttk.Button(window, text="Remove from List", command=remove_from_custom_list)
remove_button.pack(pady=5)

# Start the GUI loop
window.mainloop()


