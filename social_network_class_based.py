import datetime

class Person:
    """Represents a person in a social network.
    
    Attributes:
        id: An integer used to identify the person.
        name: A string representing the name of the person.
        date_of_birth: A date object representing the person's date of birth.
        friends: A list of people who are friends with the person.
        history: A list representing the user's posts.
    """
    def __init__(self,this_id: int, name: str, date_of_birth: datetime.date):
        """Initializes Person class with given attributes, and creates an empty list for friends and history"""
        self.id = this_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.friends = []
        self.history = []
        

    def birthday_within_X_days_of_Y(self, days: int, comparison_date: datetime.date) -> bool: 
        """Checks if the comparison date falls within the number of days of the given birthday.

        Args:
            self: The person's birthday to be checked.
            days: The number of days between the comparison_date and birthday.
            comparison_date: The date to be compared.


        Returns: 
            True if the birthday falls within days of comparison_date, and False otherwise.
        """
        # iterates through the previous year, same year, and next year of the comparison date 
        # checks if any of their dates are within the specified number of days
        for i in range(-1, 2):
            if abs((comparison_date - self.date_of_birth.replace(year = comparison_date.year + i)).days) <= days:
                return True
        return False

    
    def make_friendship(self, other_person):
        """Adds the two ID's to each other's friends list.

        Args:
            self: The first person class.
            other_person: The second person class.

        Returns:
            None
        """
        # checks that the two people are not the same
        if self.id != other_person.id:
            # adds other_person's ID to self's friends list, unless already there, and vice versa
            if other_person.id not in self.friends:
                self.friends.append(other_person.id)
            if self.id not in other_person.friends:
                other_person.friends.append(self.id)


    def end_friendship(self, other_person):
        """Removes the IDs of self and the other person from each other's friends list.

        Args:
            self: The first person class.
            other person: The second person class.

        Returns: 
            None
        """
        # if person Y's ID is in person X's friend list, remove person Y from person X's friends, and vice versa
        if other_person.id in self.friends:
            del self.friends[self.friends.index(other_person.id)]
        if self.id in other_person.friends:
            del other_person.friends[other_person.friends.index(self.id)]

    def find_my_friend(self, other_person) -> int:
        """Checks if person X is in Y's friends list and finds the index.

        Args:
            self: The person class whose friends list is being checked.
            other_person: The person class to be checked for.
        
        Returns: 
            The index of other_person in self's friends list, or None if not found.
        """
        # if in person Y's friends list, returns the index of X's ID
        if other_person.id in self.friends:
            return self.friends.index(other_person.id)
        return None

    def make_post(self, content: str, tagged: list) -> tuple:
        """Appends a new post based on the parameters to the owner's post history.

        Args: 
            self: The person class representing the owner of the post.
            content: The content of the post as a string.
            tagged: The integer IDs of users to be tagged.

        Returns: 
            The post (represented as a tuple) created based on the content, owner ID, and tagged users.
        """
        i = 0
        # loops through the list of tagged people
        while i < len(tagged):
            # deletes the tagged person if not in the owner's friends list
            if tagged[i] not in self.friends:
                del tagged[i]
            # if the tagged person is in the friends list, check the next tagged person
            else:
                i += 1
        # creates the post as a tuple of the content, owner ID, and tagged users
        post = (content, self.id, tagged)
        # adds the post to the owner's history and returns it
        self.history.append(post)
        return post
    
    def __str__(self):
        """Creates a string representation of the person.
        
        Args:
            self: The person class whose details will be converted to a string.
        Returns:
            The person's class details formatted as a string.
        """
        friends_str = str(self.friends)[1:-1]
        # returns class attributes as a formatted string
        return(f"{self.id} ({self.name}, {self.date_of_birth}) --> {friends_str}")



class SocialNetwork: 
    """A group that represents all the person classes. 
    
    Attributes:
        people: A dictionary representing the person classes.
        posts: A list of posts made by the person classes ordered by date of creation.
    """
    def __init__(self, people_friendship_data: list, post_history: list):
        """Initializes the SocialNetwork class with the given attributes."""
        def process_person_data(dict_of_people: dict, person_data: list) -> int:
            """Checks whether the ID in person_data is in dict_of_people, and if not, creates a new person based on the data.

            Args:
                dict_of_people: The dictionaries of people using ID as key.
                person_data: The details of the person.
            
            Returns:
                The integer ID in dict_of_people, or the new ID created if not found.
            """
            # splits the string to to separate the name and date of birth
            person_data = person_data.split(",")
            id_in_dict = None
            # iterates the given dictionaries
            for i in dict_of_people:
                # checks if any names from the dictionary match the name given
                if dict_of_people[i].name == person_data[0]:
                    id_in_dict = i
                    break
            # if no match was found, create a new person and return its ID
            if not id_in_dict:
                return self.add_person(person_data[0], datetime.date.fromisoformat(person_data[1]))
            # if a match was found, just return the ID
            else:
                return id_in_dict
        

        # creates an empty dictionary for the people atrribute
        self.people = {}
        # iterates the list of strings
        for i in people_friendship_data:
            # splits the strings by an arrow
            line = i.split("<->")
            # checks if 2 people were in the line
            if len(line) == 2:
                friend_ids = []
                # each friend's data is processed and both are appended to the list
                for j in line:
                    friend_ids.append(process_person_data(self.people, j))
                # the two IDs are added to each other's friends list
                self.people[friend_ids[0]].make_friendship(self.people[friend_ids[1]])
            else:
                # only one person in the line, so data is only processed
                process_person_data(self.people, line[0])
        # assigns the given post_history to the posts attribute
        self.posts = post_history


    def add_person(self, name: str, date_of_birth: datetime.date) -> int:
        """Adds a new person with a new ID according to the details input.

        Args:
            self: The SocialNetwork class to add a person to.
            name: The string name of the new person to be added.
            date_of_birth: The date of birth of the new person to be added.

        Returns:
            The new integer ID, which is the current highest ID + 1, or 1 if the dictionary was empty.
        """
        # obtains a list of IDs
        id_keys = list(self.people.keys())
        # if not empty
        if len(id_keys):
            # sorts the list in reverse order to obtain the highest ID
            id_keys.sort(reverse = True)
            # creates a new ID which is the highest ID + 1
            new_id = int(id_keys[0]) + 1
            # initializes a new person class to be added to the people attribute of SocialNetwork
            self.people[new_id] = Person(new_id, name, date_of_birth)
            # returns the new ID
            return new_id
        # if empty, initialize a new person class with ID 1 to be added to the people attribute of SocialNetwork
        else:
            self.people[1] = Person(1, name, date_of_birth)
            return 1

    def get_person_by_id(self, find_id: int) -> dict:
        """Finds the ID in the dictionary and returns it.

        Args:
            self: The SocialNetwork class to search for the ID.
            find_id: The ID to be searched for.
        
        Returns: 
            The dictionary belonging to the ID, or None if not found.
        """
        # if find_id is in the people attribute, returns the index of the ID
        if find_id in self.people:
            return self.people[find_id]
        return None
    
    def make_birthday_posts(self, from_person_id: int, comparison_date: datetime.date, days: int = 7):
        """Creates a birthday post by from_person_id for friends' birthdays within days of comparison_date.
    
        Args:
            self: The SocialNetwork to check for birthdays.
            from_person_id: The ID of the person making birthday posts for their friends.
            comparison_date: The date to be compared.
            days: The number of days to be compared with the date, which is optional and set as 7 by default. 
        
        Returns:
            None
        """
        # obtains the person from the people attribute
        person = self.people[from_person_id]
        # creates a list of friends of the person
        list_of_friends = person.friends
        # iterates the list of friends
        for i in list_of_friends:
            # checks if the birthday is within 7 days of comparison_date
            if self.people[i].birthday_within_X_days_of_Y(days, comparison_date):
                # creates a birthday post if within the range
                new_post = self.people[from_person_id].make_post(f"Happy birthday {self.people[i].name}! Hope you have a good one!", [i])
                # appends the post to the posts attribute of SocialNetwork
                self.posts.append(new_post)


    def __str__(self):
        """Constructs and returns a string representation of the entire network."""
        network = ""
        # iterates every element in the people attribute
        for i in range(1, len(self.people) + 1):
            # adds the people converted to a string
            network += str(self.people[i])
            # adds a new line
            network += "\n"
        # returns the network
        return network 

if __name__ == "__main__":
    # creates a list to store the user input
    people_data = []

    # accepts user input and appends it to the list until input stops
    data = input()
    while data:
        people_data.append(data)
        data = input()

    # initializes SocialNetwork class based on the input
    network = SocialNetwork(people_data, [])

    # prints out the network and begins simulating birthday posts
    print(network)
    print("Now simulating a year's worth of birthday posts...")

    # date is 1st January on the curent year
    current_year = datetime.date.today().year
    date = datetime.date(current_year, 1, 1)

    while date.year == current_year:
        # iterates every person in the network
        for i in network.people:
            poster = network.people[i]
            # iterates every friend of this person
            network.make_birthday_posts(poster.id, date, 0)
        # continues to the next day
        date += datetime.timedelta(days = 1)
    # prints all posts in the posts attribute of the network
    for j in range(len(network.posts)):
        print(network.posts[j])
