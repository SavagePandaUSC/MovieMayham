API_KEY = "2fc9ee028a312888352de489e536da81"
BASE_URL = "https://api.themoviedb.org/3"
def get_genres(is_tv):
    """Fetches the list of genres and their IDs code is for tv but ."""
    url = f"{BASE_URL}/genre/{'tv' if is_tv else 'movie'}/list"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["name"]: genre["id"] for genre in genres}
    else:
        return {} (edited)
