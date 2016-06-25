from interface import Interface


class Movie:
    def __init__(self, row, ratings):
        self.id = int(row['MovieID'])
        self.title = row['MovieTitle']
        self.ratings = sorted(ratings, key=self.sorter, reverse=True)
        self.average = self.find_average_rating(ratings)
        self.number_of_ratings = len(ratings)
        self.url = row['URL']
        self.genres = self.set_genre_list(row)

    def __str__(self):
        return "{}: {}".format(self.id, self.title)

    def __repr__(self):
        return str(self)

    def find_average_rating(self, ratings):
        total = sum([t[1] for t in ratings])
        return float("%.2f" % (total / len(ratings)))

    def set_genre_list(self, row):
        self.genres = []
        for key in row:
            if row[key] == '1' and key != 'MovieID':
                self.genres.append(key)
        return self.genres

    def sorter(self, val):
        return val[1]

    @staticmethod
    def display_movie_info(movie_dict, movie_id, movie_title):
        choice = input("Would you like to:\n\n1) See general information about this movie\n2) See ratings for this movie\n>")
        Interface.clear()
        Interface.print_title_bar(movie_title)
        if Interface.is_valid_two_track_input(choice):
            Interface.print_title_bar(movie_title)
            if int(choice) == 1:
                Movie.show_general_movie_info(movie_dict, movie_id,
                                              movie_title)
            else:
                Movie.show_movie_ratings_info(movie_dict, movie_id,
                                              movie_title)
        else:

            print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
            return Movie.display_movie_info(movie_dict, movie_id, movie_title)

    @staticmethod
    def show_general_movie_info(movie_dict, movie_id, movie_title):
        movie = movie_dict[movie_id]
        genres = movie.genres
        print("ID: {}\nAverage Rating: {}\nGenres: {}\nIMDB URL: {}".format(
            movie_id, movie.average, ', '.join(genres), movie.url)
        )
        print('\n' + '*' * 30)

        option = input("\nFrom here, you can:\n\n1) See ratings details\n2) Return to the main menu\n>")

        if Interface.is_valid_two_track_input(option):
            if int(option) == 1:
                Interface.clear()
                Interface.print_title_bar(movie_title)
                Movie.show_movie_ratings_info(movie_dict, movie_id,
                                              movie_title)
            else:
                Interface.clear()
                Interface.print_title_bar("Hello Again!")
                return ''
        else:
            Interface.clear()
            Interface.print_title_bar(movie_title)
            print(("*" * 25) + '\n' + "Enter a valid option.\n" + ("*" * 25) + '\n\n')
            return Movie.show_general_movie_info(movie_dict, movie_id,
                                                 movie_title)

    @staticmethod
    def search_for_movies(movie_dict, search_for_movie_message):
        movie = input('Enter all or part of a movie title to search:\n>')
        movie = movie.lower()

        print("\nMovies containing those words:\n")
        for key in movie_dict:
            if movie in movie_dict[key].title.lower():
                print(str(movie_dict[key]))

        print('\n' + '*' * 30)

        choice = input("\nDo you want to:\n1) Enter a code you see\n2) Search again\n>")

        if Interface.is_valid_two_track_input(choice):
            if int(choice) == 1:
                print('')
                return Interface.get_movie_id(search_for_movie_message)
            else:
                Interface.clear()
                Interface.print_title_bar(Interface.search_for_movie_message)
                return Movie.search_for_movies(movie_dict,
                                               search_for_movie_message)
        else:
            Interface.clear()
            Interface.print_title_bar(Interface.search_for_movie_message)
            print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
            return Movie.search_for_movies(movie_dict,
                                           search_for_movie_message)

    def show_movie_ratings_info(movie_dict, movie_id, movie_title,
                                number_to_show=10):
        movie = movie_dict[movie_id]
        print("ID: {}\tTotal ratings: {}\tAverage Rating: {}\n\nTop {} ratings:".format(movie_id, len(movie.ratings), movie.average, number_to_show))
        for i, item in enumerate(movie.ratings[:number_to_show]):
            print("{}. User {} gave it a {}".format((i + 1), item[0], item[1]))
        print('\n' + '*' * 30)

        option = input("\nFrom here, you can:\n\n1) See more ratings\n2) See general movie information\n3) Return to the main menu\n>")

        if Interface.is_valid_three_track_input(option):
            if int(option) == 1:
                Interface.clear()
                Interface.print_title_bar(movie_title)
                number_to_show = Interface.get_number_to_show(len(movie.ratings), movie_title)
                Movie.show_movie_ratings_info(movie_dict, movie_id,
                                              movie_title, number_to_show)
            if int(option) == 2:
                Interface.clear()
                Interface.print_title_bar(movie_title)
                Movie.show_general_movie_info(movie_dict, movie_id, movie_title, greeting)
            else:
                Interface.clear()
                Interface.print_title_bar("Hello Again!")
                return ''
        else:
            Interface.clear()
            Interface.print_title_bar(movie_title)
            print(("*" * 25) + '\n' + "Enter a valid option.\n" + ("*" * 25) + '\n\n')
            return Movie.show_movie_ratings_info(movie_dict, movie_id, movie_title)
