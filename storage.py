import requests
import tkinter as tk
from tkinter import ttk, messagebox
from FilterFunctions import genre_filter

API_KEY = "2fc9ee028a312888352de489e536da81"
BASE_URL = "https://api.themoviedb.org/3"

def search_movies(movie_name, genre=None, year=None, language=None, page=1):
    """Uses the API and finds a movies based on a given name and returns all of its relevant information"""

    movie_name = correct(movie_name)

    url = f"{BASE_URL}/search/movie"
    paramiters = {"api_key": API_KEY, "query": movie_name, "with_genres": genre, "primary_release_year": year, "language": language, "page": page}
    response = requests.get(url, params=paramiters)
    if(genre != None):
       response= genre_filter(response.json(), "animation")
       return response.json()
    else:
        print(type(response))
        return response.json()
        
    #if response.status_code == 200:
    
    
    
def search_movie_by_id(movie_id):
    """"Uses the API to search for a specific movie by using its id"""

    url = f"{BASE_URL}/movie/{movie_id}"
    paramiters = {'api_key': API_KEY}
    response = requests.get(url, params=paramiters)
    return response.json()


def get_id(data):
    """Recieves the data for a selected film and returns its id"""

    return data['id']


def get_director_by_id(id):
    """Return the name of a director for a movie using the movie id"""

    url = f"{BASE_URL}/movie/{id}/credits"
    paramiters = {'api_key': API_KEY}
    response = requests.get(url, params=paramiters)
    
    if response.status_code == 200:
        credits = response.json()
        # Filter crew members to find the director
        director = [member['name'] for member in credits['crew'] if member['job'] == 'Director']
        return director[0]
 


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


def save_movie(id, rating, watch_date):
    """saves the relevant movie data to a txt file (passed parameter should be the id for a movie)
    (saves in order: title, director, year_released, length, when_watched, rating, genre, id)"""

    #recieves the data and director of a movie using its id
    movie_data = search_movie_by_id(id)
    director = get_director_by_id(id)

    # create the required file if it doesn't exist
    with open('saved_movies.txt', 'a') as blank:
        pass

    # checks to see if movie is already saved
    with open('saved_movies.txt', 'r') as file:

        for line in file:
            
            if  movie_data['id'] in line:
                print('This movie is already saved')
                return None
            
    # appends the file to save movie details
    with open('saved_movies.txt', 'a') as file:

        # queries the user for unique information (possibly could be changed a query user function)
        ### watch_date = [input('Year you watched it: ')]
        ### watch_date += [input('Month you watched it: ')]
        ### watch_date += [input('Day of month you watched it: ')]
        
        ### watch_date = '-'.join(watch_date)

        ### rating = rate()


        info = [movie_data['original_title'], director, movie_data['release_date'], movie_data['runtime'], watch_date, rating, movie_data['genres'][0].get('name'), movie_data['id']]

        # writes the information into the file
        for i in info:
            file.write(str(i) + ',')
        
        file.write('\n')
    
    messagebox.showinfo("Success", "Movies Saved!")


def save_show(id):
    pass


def delete(title):
    """deletes a given movie"""

    # corrects the title so it will match with what is in the directory
    title = correct(title)

    # reads the entirety of the file and stores it in a variable
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


def rateCheck(integer):
    """This function takes an inputed rating checks if its acceotable and returns it in string format"""

    if integer < 1 or integer > 10:
        print('Your scoring must be between 1 and 10')
        rateCheck(integer)
    
    return str(integer)


def watchDate(year, month, day):
    """formats a watch date after recieving a year, month, day. (They should be in int form)"""

    if year < 1900 or year > 2024 or year.isDecimal():
        print("Unacceptable date!") 
        return None
    elif month < 1 or month > 12 or month.isDecimal():
        print("Unacceptable date!") 
        return None
    elif day < 1 or day > 31 or day.isDecimal():
        print("Unacceptable date!") 
        return None


    date = [year, month, day]


    return '-'.join(date)


if __name__ == "__main__":
   
   data = search_movies(
    "Batman",       # Movie title to search for
    "Animation",                 # Genre ID for "Action" (from genre_map)
    2022,            # Release year
    "en",                # Language code for English
    1                    # First page of results
 )
   print(data)