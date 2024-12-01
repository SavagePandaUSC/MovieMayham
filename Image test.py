import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# API Configuration
API_KEY = "2fc9ee028a312888352de489e536da81"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"  # URL for poster images

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
    total_pages = min(data.get("total_pages", 1), 10)  # Limit to 10 pages for efficiency

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
movie_list = []  # List to store movie data

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

# Image displa
poster_label = tk.Label(window, text="Poster will appear here", bg="gray", width=50, height=25)
poster_label.pack(pady=10)

# Fetch movies function
def fetch_movies():
    global movie_list
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
        # Sort movies by popularity and limit to top 20
        movies = sorted(movies, key=lambda x: x.get('popularity', 0), reverse=True)[:20]
        movie_list = movies  # Store movies for poster retrieval

        results_box.delete(0, tk.END)
        for movie in movies:
            title = movie.get("title", "Unknown Title")
            release_date = movie.get("release_date", "N/A")
            results_box.insert(tk.END, f"{title} (Release Date: {release_date})")
    else:
        results_box.delete(0, tk.END)
        results_box.insert(tk.END, "No movies found for the selected criteria.")

# Function to display poster
def display_poster(event):
    selected_index = results_box.curselection()
    if not selected_index:
        return

    selected_movie = movie_list[selected_index[0]]
    poster_path = selected_movie.get("poster_path", None)
    if poster_path:
        full_url = f"{IMAGE_BASE_URL}{poster_path}"
        response = requests.get(full_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image = Image.open(image_data)

            # Define the desired output dimensions (e.g., 300x450)
            #desired_width = 300
            #desired_height = 450
            #image = image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)

            # Convert the resized image for Tkinter
            poster_image = ImageTk.PhotoImage(image)
            poster_label.config(image=poster_image)
            poster_label.image = poster_image  # Keep a reference to avoid garbage collection
        else:
            poster_label.config(image="", text="Failed to load poster.")
    else:
        poster_label.config(image="", text="No poster available.")


# Bind selection to display poster
results_box.bind("<<ListboxSelect>>", display_poster)

# Fetch movies button
fetch_button = ttk.Button(window, text="Fetch Movies", command=fetch_movies)
fetch_button.pack(pady=5)

# Start the GUI loop
window.mainloop()

