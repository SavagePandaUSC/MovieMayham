import requests

# Replace with your API key
API_KEY = "2fc9ee028a312888352de489e536da81"
BASE_URL = "https://api.themoviedb.org/3"

def search_movies(movie_name):
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # Returns the movie data in JSON
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
def correct(movie_title):
    change = movie_title.split(' ')
    change[0] = change[0].capitalize()
    new_title = " ".join(change)
    return new_title

# Get user input
movie_name = input("Enter the name of the movie: ")

# Correct user input
movie_name = correct(movie_name)
print(movie_name)

# Query the API with the user's input
movie_data = search_movies(movie_name)

# Check and display results
if movie_data:
    if movie_data['results']:  # If there are any results
        for movie in movie_data['results']:
            print(f"Title: {movie['title']}, Release Date: {movie.get('release_date', 'N/A')}")
    else:
        print("No movies found for that search term.")