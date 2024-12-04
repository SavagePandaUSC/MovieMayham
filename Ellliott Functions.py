import tkinter as tk
from tkinter import ttk
import requests
from concurrent.futures import ThreadPoolExecutor

API_KEY = "2fc9ee028a312888352de489e536da81"
BASE_URL = "https://api.themoviedb.org/3"
def get_genres(is_tv):
    """Fetches the list of genres and their IDs code is for tv but ."""
    url = f"{BASE_URL}/genre/{'tv' if is_tv else 'movie'}/list"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    genres = response.json().get("genres", [])
    return {genre["name"]: genre["id"] for genre in genres}

def genre_filter(content, selected_genre):
    GENRE_MAP = {
    #movie genras
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
    """
    Filters content (movies or TV shows) based on the selected genre.
    """
    filtered_content = []
    for item in content.get('results', []):
        genres = [GENRE_MAP.get(genre_id, "Unknown") for genre_id in item.get('genre_ids', [])]
        if selected_genre.capitalize() in genres:
            filtered_content.append(item)
    if filtered_content == []:
        return "No movies found"
    else:
        return filtered_content

def language_filter(content, selected_language):
    """Filter by langauge"""
    filtered_content = []
    for item in content.get('results', []):
        if item.get('original_language', '').lower() == selected_language.lower():
            filtered_content.append(item)
    if filtered_content == []:
        return "No movies found"
    else:
        return filtered_content

def search_movies(movie_name):
    """Uses the API and finds a movies based on a given name and returns all of its relevant information"""

    url = f"{BASE_URL}/search/movie"
    paramiters = {"api_key": API_KEY, "query": movie_name}
    response = requests.get(url, params=paramiters)
    if response.status_code == 200:
        return response.json()  

if __name__ == "__main__":
    movies = search_movies("Batman")
    filtered_movies = language_filter(movies, "en")
    print(filtered_movies)


