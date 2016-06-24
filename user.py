
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

    def sorter(self, val):
        return val[1]
