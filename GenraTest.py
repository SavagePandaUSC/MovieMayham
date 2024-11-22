import requests

API_KEY = "2fc9ee028a312888352de489e536da81"  # Replace with your API key
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
        print(f"Error fetching genres: {response.status_code}, {response.text}")
        return {}

def discover_movies_by_genre(genre_id):
    """Fetches movies by genre ID using the discover endpoint, handling pagination."""
    movies = []
    page = 1
    total_pages = 1  # Initialize to enter the loop

    while page <= total_pages:
        url = f"{BASE_URL}/discover/movie"
        params = {"api_key": API_KEY, "with_genres": genre_id, "page": page}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            movies.extend(data.get("results", []))
            total_pages = data.get("total_pages", 1)
            page += 1
        else:
            print(f"Error discovering movies: {response.status_code}, {response.text}")
            break

    return movies

def main():
    genres = get_genres()
    if not genres:
        print("Could not retrieve genres. Exiting...")
        return

    print("Available genres:")
    for genre_name in genres:
        print(f"- {genre_name.capitalize()}")

    genre = input("Enter a genre to filter by: ").strip().lower()
    genre_id = genres.get(genre)

    if not genre_id:
        print("Invalid genre. Please try again.")
        return

    print(f"Fetching movies in the genre: {genre.capitalize()}...")
    movies = discover_movies_by_genre(genre_id)

    if movies:
        print(f"\nMovies found ({len(movies)} total):")
        for movie in movies:
            print(f"Title: {movie['title']}, Release Date: {movie.get('release_date', 'N/A')}")
    else:
        print("No movies found in this genre.")

if __name__ == "__main__":
    main()
