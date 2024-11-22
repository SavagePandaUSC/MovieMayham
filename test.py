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

def search_movies(movie_name, genre_id=None):
    """Searches movies by name and optionally filters by genre ID."""
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        movie_data = response.json()
        if genre_id:
            # Filter results by genre ID
            filtered_movies = [
                movie for movie in movie_data.get("results", [])
                if genre_id in movie.get("genre_ids", [])
            ]
            movie_data["results"] = filtered_movies

        return movie_data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def correct_title(movie_title):
    """Capitalizes each word in the movie title."""
    words = movie_title.split()
    corrected_title = " ".join(word.capitalize() for word in words)
    return corrected_title

def main():
    genres = get_genres()
    if not genres:
        print("Could not retrieve genres. Exiting...")
        return

    print("Available genres:")
    for genre_name in genres:
        print(f"- {genre_name.capitalize()}")

    movie_name = input("\nEnter the name of the movie: ")
    genre = input("Enter a genre to filter by (optional): ").lower()

    corrected_title = correct_title(movie_name)
    genre_id = genres.get(genre) if genre else None

    movie_data = search_movies(corrected_title, genre_id)

    if movie_data:
        if movie_data.get("results"):
            print("\nMovies found:")
            for movie in movie_data["results"]:
                print(f"Title: {movie['title']}, Release Date: {movie.get('release_date', 'N/A')}")
        else:
            print("No movies found for that search term or genre.")
    else:
        print("An error occurred while fetching movie data.")

if __name__ == "__main__":
    main()

