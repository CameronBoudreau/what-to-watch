import csv
import os

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



class Movie:
    def __init__(self, row):
        self.id = row['MovieID']
        self.title = row['MovieTitle']

    def __str__(self):
        return str("{}: {}".format(self.id, self.title))


class User:
    pass


class Rating:
    pass


def get_user_choice():
    choice = input("Would you like to:\n(1)See ratings for a specific movie?\n\n OR \n\n(2)Have a movie recommended for you\n\n> ")
    check_get_user_choice(choice)


def check_get_user_choice(choice):
    if choice != any(1,2):
        print("Please choose a valid option. (1 or 2)")
        return get_user_choice()


def get_movie_choice():
    movie_choice = input("Please enter the ID of the movie you want to check: ")
    check_get_movie_choice(movie_choice)


def check_get_movie_choice(movie_choice):
    if choice < 0 or choice > 1682:
        print("Enter a valid ID. See README.md for a list of movies and IDs")


def get_movie_list():
    with open('u.item', encoding='latin_1') as f:
        movie_list = []
        reader = csv.DictReader(f, fieldnames=['MovieID', 'MovieTitle'], delimiter='|')
        for row in reader:
            movie_list.append(Movie(row))
    return movie_list


def main():
    clear()
    movie_list = get_movie_list()
    print(movie_list)
    print("Hello! Welcome to movie heaven.")
    choice = get_user_choice()

    # Get ratings
    if choice == 1:
        movie_id = get_movie_choice()
        get_movie_ratings(movie_id)

    # Get recommendations
    else:

    find_average_rating(movie_id)

    get_name_by_id(movie_id)

    get_all_ratings_by_user(user)


    
if __name__ == '__main__':
    main()
