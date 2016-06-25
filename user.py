from utilities import sorter
# from show import Show
# from validity import Validity


class User:
    def __init__(self, row, ratings):
        self.user_id = int(row['UserID'])
        self.age = int(row['Age'])
        self.sex = row['Sex']
        self.occupation = row['Occupation']
        self.ratings = sorted(ratings, key=sorter, reverse=True)
        self.highest_rated = self.find_highest_rated(self.ratings)

    def __str__(self):
        return str("{}: Age: {}; Sex: {}; Occupation: {}; Ratings: {}".format(self.user_id, self.age, self.sex, self.occupation, self.ratings))

    def __repr__(self):
        return str(self)

    def find_highest_rated(self, ratings):
        return sorted(ratings, key=sorter, reverse=True)

    @staticmethod
    def get_user_to_look_up(user_dict):
        user_id = input("Enter a User ID to look up. User IDs range from 1 to 943.\n>")
        Show.clear()
        if Interface.is_valid_user_id_input(user_dict, user_id):
            return int(user_id)
        else:
            Show.print_title_bar(Show.find_user_message)
            print(("*" * 25) + '\n' + "Enter a valid choice.\n" + ("*" * 25) + '\n')
            return User.get_user_to_look_up(user_dict,
                                            Show.find_user_message)

    @staticmethod
    def display_user_ratings(user_dict, user_id, id_to_title, user_look_up_message, number_to_show=15, sort=0, greeting="Welcome to Movie Heaven!"):
        user = user_dict[user_id]
        print("User {} ({}, {}, {}) has rated {} movies. Showing 1 - {}: \n".format(user_id, user.age, user.sex, user.occupation, len(user.ratings), number_to_show))

        ratings = user.ratings

        if sort == 1:
            new_ratings = []
            for i in ratings:
                new_ratings.append((id_to_title[i[0]], i[1]))
            ratings = sorted(new_ratings)

        if sort == 0:
            for i, rating in enumerate(ratings[:number_to_show]):
                print("{}. {}: {}".format(i + 1, id_to_title[rating[0]], rating[1]))
        else:
            for i, rating in enumerate(ratings[:number_to_show]):
                print("{}. {}: {}".format(i + 1, rating[0], rating[1]))

        print('\n' + '*' * 30)

        option = input("\nFrom here, you can:\n\n1) See more ratings\n2) Toggle sort by movie title or rating\n3) Return to the main menu\n>")

        if Interface.is_valid_three_track_input(option):
            if int(option) == 1:
                Show.clear()
                Show.print_title_bar(user_look_up_message)
                number_to_show = Show.get_number_to_show(
                    len(ratings), user_look_up_message
                )
                Show.display_user_ratings(user_dict, user_id, id_to_title,
                                             number_to_show, sort)
            if int(option) == 2:
                Show.clear()
                if sort == 1:
                    sort = 0
                else:
                    sort = 1
                print("Sort: ", sort)
                Show.print_title_bar(Show.user_look_up_message)
                User.display_user_ratings(
                    user_dict, user_id, id_to_title, user_look_up_message,
                    number_to_show, sort
                )
            else:
                Show.clear()
                Show.print_title_bar("Hello Again!")
                return ''
