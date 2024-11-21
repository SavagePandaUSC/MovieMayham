#test
class Movie:
    def __init__(self, title, director, year_released, length, when_watched, rating, genre):
        self._title = title
        self._director = director
        self._year_released = year_released
        self._length = length  # in minutes
        self._when_watched = when_watched
        self._rating = rating  # scale of 1-10, or as preferred
        self._genre = genre
    def __init__(self):
        self._title = ""
        self._director = ""
        self._year_released = ""
        self._length = ""  # in minutes
        self._when_watched = ""
        self._rating = ""  # scale of 1-10, or as preferred
        self._genre = ""
    # Getter and setter for title
    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title

    # Getter and setter for director
    def get_director(self):
        return self._director

    def set_director(self, director):
        self._director = director

    # Getter and setter for year released
    def get_year_released(self):
        return self._year_released

    def set_year_released(self, year_released):
        self._year_released = year_released

    # Getter and setter for length
    def get_length(self):
        return self._length

    def set_length(self, length):
        self._length = length

    # Getter and setter for when watched
    def get_when_watched(self):
        return self._when_watched

    def set_when_watched(self, when_watched):
        self._when_watched = when_watched

    # Getter and setter for rating
    def get_rating(self):
        return self._rating

    def set_rating(self, rating):
        self._rating = rating

    # Getter and setter for genre
    def get_genre(self):
        return self._genre

    def set_genre(self, genre):
        self._genre = genre