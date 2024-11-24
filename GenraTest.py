import requests
from concurrent.futures import ThreadPoolExecutor

API_KEY = "2fc9ee028a312888352de489e536da81"
BASE_URL = "https://api.themoviedb.org/3"

def get_genres():
    """Fetches the list of genres and their IDs."""
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["name"].lower(): genre["id"] for genre in genres}
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

    # Use ThreadPoolExecutor to fetch pages in parallel
    movies = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_page, genre_id, language, page)
            for page in range(1, total_pages + 1)
        ]
        for future in futures:
            movies.extend(future.result())

    return movies

def main():
    genres = get_genres()
    if not genres:
        return

    print("Available genres:")
    for genre_name in genres:
        print(f"- {genre_name.capitalize()}")

    genre = input("Enter a genre to filter by: ").strip().lower()
    genre_id = genres.get(genre)

    if not genre_id:
        print("Invalid genre. Please try again.")
        return

    language = input("Enter the language code to filter by (e.g., 'en' for English, 'fr' for French): ").strip().lower()

    print(f"Fetching movies in the genre '{genre.capitalize()}' and language '{language}'...")
    movies = discover_movies_by_genre_and_language(genre_id, language)

    if movies:
        # Sort movies by popularity in descending order
        movies = sorted(movies, key=lambda x: x.get('popularity', 0), reverse=True)
        # Slice to get the top 20 most popular movies
        top_movies = movies[:20]
        
        print(f"\nTop 20 movies found ({len(top_movies)} total):")
        for movie in top_movies:
            print(f"Title: {movie['title']}, Release Date: {movie.get('release_date', 'N/A')}")
    else:
        print("No movies found for this genre and language.")

if __name__ == "__main__":
    main()