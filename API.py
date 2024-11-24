import requests

API_KEY = "2fc9ee028a312888352de489e536da81"
BASE_URL = "https://api.themoviedb.org/3"

def search_movies(movie_name):
    """Uses the API and finds a movies based on a given name and returns all of its relevant information"""

    movie_name = correct(movie_name)

    url = f"{BASE_URL}/search/movie"
    paramiters = {"api_key": API_KEY, "query": movie_name}
    response = requests.get(url, params=paramiters)
    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def correct(movie_title):
    """corrects the title of a movie so it can properly query the API (passed paramater should be a string)"""
    
    movie_title = movie_title.lower()

    lowercase_words = [
    "a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into", "nor", 
    "of", "on", "or", "so", "the", "to", "up", "with", "yet", "about", "above", 
    "after", "along", "among", "around", "before", "behind", "below", "beneath", 
    "beside", "between", "beyond", "during", "except", "inside", "near", "outside", 
    "over", "past", "since", "through", "under", "until", "upon", "within", "without"]

    change = movie_title.split(' ')

    # first word capitlization
    change[0] = change[0].capitalize()

    # corrects the rest of the title
    index = 1
    for i in change[1:]:
        if i in lowercase_words:
            index += 1
        else:
            change[index] = change[index].capitalize()
            index += 1


    # reconnecting movie title
    return " ".join(change)  


def save(movie_data, movie_title):
    """saves the relevant movie data to a txt file (passed parameter should be the dictionary for a movie and then its title)"""

    # create the required file if it doesn't exist
    with open('saved_movies.txt', 'a') as blank:
        pass

    # checks to see if movie is already saved
    with open('saved_movies.txt', 'r') as check:

        for line in check:
            
            if  movie_title in line or  movie_data.get('release_date', '') in line:
                print('This movie is already saved')
                return None

    
    # appends the file to save movie details
    with open('saved_movies.txt', 'a') as file:

        # write the movies details into the txt file
        info = ['original_title', 'release_date', 'id']

        for i in info:
            file.write(str(movie_data[i]) + ', ')
        
        file.write('\n')

def delete(title):
    """deletes a given movie"""

    # corrects the title so it will match with what is in the directory
    title = correct(title)

    # reads the entirety of the file and saves it
    with open('saved_movies.txt', 'r') as file:
        lines = file.readlines()
    
    # checks to see if the given title is in the directory
    if title not in lines:
        print(title + ' is not in the directory')
        return None

    # removes the given movies
    with open('saved_movies.txt', 'w') as file:
        for line in lines:
            if title not in line:
                file.write(line)