from storage import search_movies, save_movie, delete, get_id

class Movie:
    def __init__(self, line):
        self.title = line[0]
        self.director = line[1]
        self.release_date = line[2]
        self.runtime = line[3]
        self.watch_date = line[4]
        self.rating = line[5]
        self.genre = line[6]
        self.id = line[7]

holder = {}
with open('saved_movies.txt', 'r') as file:
    lines = file.readlines()
    for l in lines:
        holder[l[:',']] = Movie(l)

print(holder)


"""
example for reference:
info = [movie_data['title'], director, movie_data['release_date'], 
movie_data['runtime'], watch_date, rating, movie_data['genres'][0].get('name'), movie_data['id']]

Scooby-Doo! Pirates Ahoy!, #title
Chuck Sheetz, #director
2006-09-19, #release date
71, #runtime
11, #watchdate?
10-10-1010, #rating?
Fantasy, #genre
13355, #id
"""