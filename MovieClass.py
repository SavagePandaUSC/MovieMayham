from storage import search_movies, save_movie, delete, get_id

class Movie:
    def __init__(self, line):
        self.title = line[0]
        self.director = line[1]
        self.release_date = line[2]
        self.runtime = line[3]
        self.watch_date = line[4]
        self.genre = line[5]
        self.id = line[6]
    def remove_movie(self):
        """Removes this movie from the saved_movies.txt file based on its ID."""
        file_path='saved_movies.txt'
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Filter out the line with the matching movie ID
            updated_lines = [line for line in lines if line.split(',')[7].strip() != self.id]

            with open(file_path, 'w') as file:
                file.writelines(updated_lines)
            
            print(f"Movie '{self.title}' successfully removed.")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred while removing the movie: {e}")
def make_movie_objects():
    holder = {}
    with open('saved_movies.txt', 'r') as file:
        lines = file.readlines()
        for l in lines:
            l = l.split(',')
            holder[l[6]] = Movie(l) #holder[l][7] is the movie's ID number
    return holder

#test: 
# make_movie_objects()
# print(holder['13355'].title)


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